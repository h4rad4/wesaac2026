from langchain_core.messages import HumanMessage, SystemMessage

from . import prompts

SINGLE_PASS_CHARS = 30000
WRITER_MAX_TOKENS = 16384

def split_into_passes(windows):
    """Group windows into writer passes of at most SINGLE_PASS_CHARS each."""
    passes = []
    current = []
    current_length = 0
    for window in windows:
        length = len(window.get("discourse", "")) + len(window.get("wikipedia_data") or "")
        if current and current_length + length > SINGLE_PASS_CHARS:
            passes.append(current)
            current = []
            current_length = 0
        current.append(window)
        current_length += length
    if current:
        passes.append(current)
    return passes

def deduplicate_figures(windows):
    """Drop figures that repeat across windows (same image, different size)."""
    seen_urls = set()
    result = []
    for window in windows:
        kept = []
        for figure in window.get("figures") or []:
            parts = figure["url"].split("/")
            identity = parts[-2] if "thumb" in parts and len(parts) >= 2 else figure["url"]
            if identity not in seen_urls:
                seen_urls.add(identity)
                kept.append(figure)
        result.append({**window, "figures": kept})
    return result

def build_writer_prompt(batch, pass_number, total_passes):
    source = "\n\n---\n\n".join(
        f"[window slides {window['first']}-{window['last']}]\n"
        f"DISCOURSE:\n{window['discourse']}\n\n"
        f"WIKIPEDIA DATA:\n{window.get('wikipedia_data') or '—'}"
        for window in batch
    )
    available = [figure for window in batch for figure in (window.get("figures") or [])]
    gallery = (
        "\n".join(
            f"- url: {figure['url']}\n  caption: {figure['caption']}\n"
            f"  from_article: {figure['article']} ({figure['article_url']})"
            for figure in available
        )
        or "—"
    )

    note = ""
    if pass_number > 0:
        note = (
            f" — continuation part {pass_number + 1}/{total_passes}: write only the `##` sections "
            "for these windows, with NO top-level `#` title"
        )
    return (
        f"LECTURE SOURCE (per window){note}:\n{source}\n\n"
        f"AVAILABLE FIGURES:\n{gallery}"
    )

def drop_repeated_title(markdown):
    """Continuation passes may still open with a `#` title; remove it."""
    lines = markdown.splitlines()
    while lines and (lines[0].startswith("# ") or not lines[0].strip()):
        lines.pop(0)
    return "\n".join(lines).strip()

async def compose_lecture(provider, windows):
    windows = [window for window in windows if (window.get("discourse") or "").strip()]
    if not windows:
        return ""

    windows = deduplicate_figures(windows)
    passes = split_into_passes(windows)

    written = []
    for number, batch in enumerate(passes):
        prompt = build_writer_prompt(batch, number, len(passes))
        messages = [SystemMessage(prompts.WRITER), HumanMessage(prompt)]

        reply = await provider.llm("writer", max_tokens=WRITER_MAX_TOKENS).ainvoke(messages)
        body = reply.content.strip() if isinstance(reply.content, str) else str(reply.content).strip()

        if not body:
            print(f"  [writer] empty reply -- retrying once", flush=True)
            reply = await provider.llm("writer", max_tokens=WRITER_MAX_TOKENS).ainvoke(messages)
            body = reply.content.strip() if isinstance(reply.content, str) else str(reply.content).strip()

        if number:
            body = drop_repeated_title(body)
        written.append(body)

    return "\n\n".join(written)
