import asyncio
import tempfile
import time

from .compose import compose_lecture
from .nodes import MAX_ATTEMPTS, make_agents
from .render import render_slides

DEFAULT_WINDOW_SIZE = 5
DEFAULT_DPI = 150
WINDOW_CONCURRENCY = 4

async def process_window(agents, slide_images, first_slide):
    """One window: professor -> critic loop -> researcher."""
    history = []
    discourse = await agents["professor"](slide_images, first_slide)
    attempts = 1
    while True:
        status, feedback = await agents["critic"](slide_images, first_slide, discourse, history)
        history.append({"discourse": discourse, "feedback": feedback})
        if status == "APPROVED" or attempts >= MAX_ATTEMPTS:
            break
        discourse = await agents["professor"](slide_images, first_slide, feedback)
        attempts += 1

    research = await agents["researcher"](discourse)
    return {
        "first": first_slide,
        "last": first_slide + len(slide_images) - 1,
        "discourse": discourse,
        "status": status,
        "attempts": attempts,
        **research,
    }

async def generate_lecture(
    provider,
    slide_images,
    window_size=DEFAULT_WINDOW_SIZE,
    language="en",
    on_window=None,
    done_windows=None,
    window_concurrency=None,
):
    """Run every slide window concurrently, then write the lecture.

    Returns {"windows": [...], "lecture": markdown}. Failed windows yield a
    dict with an empty discourse; compose_lecture skips them. on_window(result,
    meta) is called once per window and may raise to abort the whole run.
    """
    agents = make_agents(provider, language)
    images = [str(path) for path in slide_images]
    semaphore = asyncio.Semaphore(max(1, window_concurrency or WINDOW_CONCURRENCY))
    done = done_windows or {}

    async def one(cursor):
        chunk = images[cursor : cursor + window_size]
        first_slide = cursor + 1
        meta = {
            "first": first_slide,
            "last": first_slide + len(chunk) - 1,
            "n_slides": len(chunk),
        }

        cached = done.get(first_slide)
        if cached is not None:
            result = cached
            meta.update({"status": "CACHED", "attempts": 0, "search_terms": [],
                         "time_s": 0.0, "error": None})
        else:
            started = time.perf_counter()
            async with semaphore:
                try:
                    result = await process_window(agents, chunk, first_slide)
                    error = None
                except Exception as failure:
                    result = {
                        "first": first_slide,
                        "last": first_slide + len(chunk) - 1,
                        "discourse": "",
                    }
                    error = f"{type(failure).__name__}: {failure}"
            meta.update({
                "status": result.get("status"),
                "attempts": result.get("attempts"),
                "search_terms": result.get("search_terms") or [],
                "time_s": round(time.perf_counter() - started, 2),
                "error": error,
            })

        if on_window:
            on_window(result, meta)
        return result

    cursors = range(0, len(images), window_size)
    windows = sorted(await asyncio.gather(*(one(c) for c in cursors)),
                     key=lambda w: w["first"])
    lecture = await compose_lecture(provider, windows)
    return {"windows": windows, "lecture": lecture}

async def run_deck(provider, pdf, dpi=DEFAULT_DPI, window_size=DEFAULT_WINDOW_SIZE,
                   max_slides=None, language="en", on_window=None,
                   window_concurrency=None):
    """Render a PDF and produce the full study text; returns the markdown."""
    failures = []

    def track(result, meta):
        if meta.get("error"):
            failures.append(f"slides {meta['first']}-{meta['last']}: {meta['error']}")
        if on_window:
            on_window(result, meta)

    with tempfile.TemporaryDirectory() as image_dir:
        images = render_slides(pdf, dpi, image_dir)[:max_slides]
        if not images:
            raise RuntimeError(f"run_deck: no slides rendered from {pdf}")
        final = await generate_lecture(provider, images, window_size,
                                       language=language, on_window=track,
                                       window_concurrency=window_concurrency)

    lecture = final["lecture"]
    if not lecture.strip():
        if failures:
            summary = "\n  ".join(failures[:5])
            more = f"\n  ...and {len(failures) - 5} more" if len(failures) > 5 else ""
            raise RuntimeError(
                f"run_deck produced no lecture: all {len(failures)} window(s) failed:\n"
                f"  {summary}{more}"
            )
        raise RuntimeError(
            "run_deck produced no lecture: windows completed but the writer returned empty output"
        )
    return lecture
