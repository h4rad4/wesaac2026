import asyncio
import base64
import json
import logging
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote

import httpx
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import StructuredTool

from . import prompts

log = logging.getLogger("pipeline")

MAX_ATTEMPTS = 3
MAX_PAGES = 5
MAX_RESEARCH_STEPS = 8
ARTICLE_CHARS = 8000
WIKIPEDIA_USER_AGENT = "automated-agent/0.1 (research; https://github.com/; bot@example.org)"

_http_client = None

def _shared_client():
    global _http_client
    if _http_client is None or _http_client.is_closed:
        _http_client = httpx.AsyncClient(
            timeout=30, follow_redirects=True, headers={"User-Agent": WIKIPEDIA_USER_AGENT}
        )
    return _http_client

async def _wiki_get(path, language, **params):
    url = f"https://{language}.wikipedia.org/w/rest.php/v1/{path}"
    response = await _shared_client().get(url, params=params)
    response.raise_for_status()
    return response.text

def _clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return re.sub(r"\[\s*\d+\s*\]", "", text).strip()

class _ArticleParser(HTMLParser):
    """Extracts the paragraphs and figures from a Wikipedia article page."""

    def __init__(self):
        super().__init__()
        self.paragraphs = []
        self.figures = []
        self._paragraph_depth = 0
        self._current_figure = None
        self._inside_caption = False

    def handle_starttag(self, tag, attrs):
        if tag == "p":
            self._paragraph_depth += 1
        elif tag == "figure":
            self._current_figure = {"url": "", "caption": ""}
        elif tag == "img" and self._current_figure is not None and not self._current_figure["url"]:
            attributes = dict(attrs)
            best_url = attributes.get("src", "")
            best_multiplier = 1.0
            for candidate in attributes.get("srcset", "").split(","):
                parts = candidate.split()
                if len(parts) != 2 or not parts[1].endswith("x"):
                    continue
                try:
                    multiplier = float(parts[1][:-1])
                except ValueError:
                    continue
                if multiplier > best_multiplier:
                    best_url, best_multiplier = parts[0], multiplier
            if best_url.startswith("//"):
                best_url = "https:" + best_url
            self._current_figure["url"] = best_url
        elif tag == "figcaption" and self._current_figure is not None:
            self._inside_caption = True

    def handle_endtag(self, tag):
        if tag == "p" and self._paragraph_depth:
            self._paragraph_depth -= 1
        elif tag == "figcaption":
            self._inside_caption = False
        elif tag == "figure":
            if self._current_figure and self._current_figure["url"]:
                self.figures.append(self._current_figure)
            self._current_figure = None

    def handle_data(self, text):
        if self._inside_caption and self._current_figure is not None:
            self._current_figure["caption"] += text
        elif self._paragraph_depth:
            self.paragraphs.append(text)

def parse_page(html, title, key, language):
    parser = _ArticleParser()
    parser.feed(html)

    prose = _clean_text(" ".join(parser.paragraphs))[:ARTICLE_CHARS]
    text_block = f"## {title}\n{prose}" if prose else ""
    article_url = f"https://{language}.wikipedia.org/wiki/{quote(key, safe='')}"

    figures = [
        {
            "url": figure["url"],
            "caption": _clean_text(figure["caption"]),
            "article": title,
            "article_url": article_url,
        }
        for figure in parser.figures
    ]
    return text_block, figures

_parts_cache = {}
_PARTS_CACHE_MAX = 16

def slide_parts(slide_paths, first_slide):
    cache_key = (tuple(slide_paths), first_slide)
    if cache_key in _parts_cache:
        return _parts_cache[cache_key]

    parts = []
    for offset, path in enumerate(slide_paths):
        data = Path(path).read_bytes()
        mime = "image/jpeg" if Path(path).suffix.lower() in {".jpg", ".jpeg"} else "image/png"
        encoded = base64.b64encode(data).decode()
        parts.append({"type": "text", "text": f"SLIDE {first_slide + offset}:"})
        parts.append({"type": "image_url", "image_url": {"url": f"data:{mime};base64,{encoded}"}})

    if len(_parts_cache) >= _PARTS_CACHE_MAX:
        _parts_cache.pop(next(iter(_parts_cache)))
    _parts_cache[cache_key] = parts
    return parts

def make_agents(provider, language="en"):
    """The three per-window agents as plain async functions."""

    async def professor(slide_paths, first_slide, feedback=""):
        content = [
            {"type": "text", "text": "The consecutive slides of this window follow, in order:"},
            *slide_parts(slide_paths, first_slide),
            {
                "type": "text",
                "text": (
                    "\nCRITIQUE OF THE PREVIOUS ATTEMPT:\n"
                    + (feedback or "— (first attempt, no critique yet)")
                ),
            },
        ]
        reply = await provider.llm("professor", max_tokens=4096).ainvoke(
            [SystemMessage(prompts.PROFESSOR), HumanMessage(content=content)]
        )
        return reply.content.strip()

    async def critic(slide_paths, first_slide, discourse, history):
        dialogue_so_far = ""
        if history:
            rounds = "\n\n".join(
                f"ATTEMPT {number}:\n{round_['discourse']}\n\nYOUR CRITIQUE OF IT:\n{round_['feedback']}"
                for number, round_ in enumerate(history, start=1)
            )
            dialogue_so_far = (
                "DIALOGUE SO FAR — your earlier critiques and the attempts they judged. Stay "
                "consistent with them: do not contradict your own prior feedback, do not punish a "
                "change you asked for, and do not raise a brand-new demand the earlier attempts "
                f"already satisfied.\n{rounds}\n\n"
            )

        content = [
            {"type": "text", "text": "The slides of this window follow, in order:"},
            *slide_parts(slide_paths, first_slide),
            {"type": "text", "text": f"\n{dialogue_so_far}CURRENT DISCOURSE:\n{discourse}"},
        ]
        reply = await provider.llm("critic", max_tokens=1024).ainvoke(
            [SystemMessage(prompts.CRITIC), HumanMessage(content=content)]
        )

        verdict = re.match(r"\s*\**\s*(APPROVED|REJECTED)\b", reply.content, re.IGNORECASE)
        status = verdict.group(1).upper() if verdict else "REJECTED"
        feedback = re.sub(
            r"^\s*\**\s*(APPROVED|REJECTED)\b\s*\**\s*[:.-]?\s*",
            "", reply.content, count=1, flags=re.IGNORECASE,
        ).strip()
        return status, feedback

    async def researcher(discourse):
        article_texts = []
        figures = []
        fetched_keys = set()
        seen_figure_urls = set()
        titles_by_key = {}
        searched_terms = []

        async def search_wiki(term):
            searched_terms.append(term)
            try:
                response = await _wiki_get("search/page", language, q=term, limit=6)
                candidates = json.loads(response)["pages"]
            except Exception as error:
                log.warning("wikipedia search %r failed: %s", term, error)
                return "[]"

            for candidate in candidates:
                titles_by_key[candidate["key"]] = candidate.get("title") or candidate["key"]

            return json.dumps(
                [
                    {
                        "key": candidate["key"],
                        "title": titles_by_key[candidate["key"]],
                        "summary": re.sub(
                            r"<[^>]+>",
                            "",
                            candidate.get("excerpt") or candidate.get("description") or "",
                        )[:200],
                    }
                    for candidate in candidates
                ]
            )

        async def fetch_wiki(key):
            if len(fetched_keys) >= MAX_PAGES:
                return "page limit reached; stop fetching and finish."
            if key in fetched_keys:
                return "already fetched that page."
            fetched_keys.add(key)

            try:
                html = await _wiki_get(f"page/{quote(key, safe='')}/html", language)
            except Exception as error:
                log.warning("wikipedia fetch %r failed: %s", key, error)
                return f"could not fetch '{key}'; try another candidate."

            title = titles_by_key.get(key, key.replace("_", " "))
            text_block, page_figures = parse_page(html, title, key, language)
            if text_block:
                article_texts.append(text_block)

            kept = 0
            for figure in page_figures:
                if figure["url"] in seen_figure_urls:
                    continue
                seen_figure_urls.add(figure["url"])
                figures.append(figure)
                kept += 1

            return f"Fetched '{title}': {len(text_block)} chars of prose, {kept} figure(s) kept."

        tools = {
            "search_wiki": StructuredTool.from_function(
                coroutine=search_wiki,
                name="search_wiki",
                description=(
                    "Search Wikipedia for a concept; returns candidate pages as JSON "
                    "(key, title, summary)."
                ),
            ),
            "fetch_wiki": StructuredTool.from_function(
                coroutine=fetch_wiki,
                name="fetch_wiki",
                description=(
                    "Fetch a candidate page by its `key` (from search_wiki), grounding "
                    "the material on its text and figures."
                ),
            ),
        }

        llm = provider.llm("researcher").bind_tools(list(tools.values()))
        messages = [
            SystemMessage(prompts.RESEARCHER),
            HumanMessage(f"PROFESSOR DISCOURSE:\n{discourse}"),
        ]

        for _ in range(MAX_RESEARCH_STEPS):
            reply = await llm.ainvoke(messages)
            messages.append(reply)

            requested_calls = getattr(reply, "tool_calls", None) or []
            if not requested_calls:
                break

            async def run_tool(call):
                tool = tools.get(call["name"])
                if tool is None:
                    return f"unknown tool {call['name']}"
                return await tool.ainvoke(call["args"])

            results = await asyncio.gather(*(run_tool(call) for call in requested_calls))
            for call, result in zip(requested_calls, results):
                messages.append(ToolMessage(content=str(result), tool_call_id=call["id"]))

        return {
            "search_terms": searched_terms,
            "wikipedia_data": "\n\n".join(article_texts),
            "images": figures,
        }

    return {"professor": professor, "critic": critic, "researcher": researcher}
