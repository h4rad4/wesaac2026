import json
import re
import shutil
import tempfile
import time
from copy import deepcopy
from pathlib import Path

from langchain_core.callbacks import BaseCallbackHandler

from pipeline.cache import CachingProvider
from pipeline.compose import SINGLE_PASS_CHARS, compose_lecture
from pipeline.graph import generate_lecture
from pipeline.llm import OpenRouterProvider
from pipeline.pdf import save_pdf
from pipeline.render import render_slides

ROOT = Path(__file__).resolve().parent
COURSE = "Introduction to Computational Thinking and Data Science"
EXPERIMENTS = ROOT / "results" / "experiments"

AGENTS = ["professor", "critic", "researcher", "writer"]

MAX_CONSECUTIVE_ERRORS = 5

class RunAborted(RuntimeError):
    pass

def lectures():
    slides = ROOT / "data" / COURSE / "static_resources"
    pdfs = list(slides.glob("*MIT6_0002F16_lec*.pdf"))
    return sorted(pdfs, key=lambda pdf: int(re.search(r"lec(\d+)", pdf.name).group(1)))

def lecture_name(pdf):
    return re.search(r"(lec\d+)", pdf.name).group(1)

def results_dir(model, out_suffix=""):
    return EXPERIMENTS / (model.replace("/", "_") + out_suffix)

class _TokenCounter(BaseCallbackHandler):

    def __init__(self, totals, role):
        self.totals = totals
        self.role = role

    def on_llm_end(self, response, **kwargs):
        input_tokens = output_tokens = None

        try:
            usage = getattr(response.generations[0][0].message, "usage_metadata", None) or {}
            input_tokens = usage.get("input_tokens")
            output_tokens = usage.get("output_tokens")
        except Exception:
            pass

        if input_tokens is None:
            raw_usage = (response.llm_output or {}).get("token_usage", {})
            input_tokens = raw_usage.get("prompt_tokens", 0)
            output_tokens = raw_usage.get("completion_tokens", 0)

        role_totals = self.totals.setdefault(
            self.role, {"calls": 0, "input_tokens": 0, "output_tokens": 0}
        )
        role_totals["calls"] += 1
        role_totals["input_tokens"] += input_tokens or 0
        role_totals["output_tokens"] += output_tokens or 0

class InstrumentedProvider(CachingProvider):

    def __init__(self, totals, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.totals = totals

    def llm(self, role, **kwargs):
        callbacks = kwargs.pop("callbacks", []) + [_TokenCounter(self.totals, role)]
        return super().llm(role, callbacks=callbacks, **kwargs)

def _total(per_agent, field):
    return sum(role_totals.get(field, 0) for role_totals in per_agent.values())

def load_done_windows(windows_dir, n_slides, window_size):
    """Resume at window granularity -- any persisted window with a
    non-empty discourse is reused as-is. Boundaries must match the current
    slicing (same window_size / max_slides), otherwise they are ignored."""
    done = {}
    for path in sorted(windows_dir.glob("slides*.json")):
        m = re.fullmatch(r"slides(\d+)-(\d+)\.json", path.name)
        if not m:
            continue
        first, last = int(m.group(1)), int(m.group(2))
        if (first - 1) % window_size or last > n_slides:
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if isinstance(data, dict) and isinstance(data.get("discourse"), str) and data["discourse"].strip():
            done[first] = data
    return done

async def process_deck(pdf, model, dpi=150, max_slides=None,
                       critic_model="", out_suffix="",
                       window_size=5, language="en",
                       window_concurrency=None,
                       resume_windows=True):
    models = {role: model for role in AGENTS} | {"default": model}
    if critic_model:
        models["critic"] = critic_model

    usage = {}
    provider = InstrumentedProvider(usage, models)

    out_dir = results_dir(model, out_suffix) / lecture_name(pdf)
    windows_dir = out_dir / "windows"
    windows_dir.mkdir(parents=True, exist_ok=True)
    log_path = out_dir / "log.txt"
    log_path.write_text("", encoding="utf-8")

    def log(line):
        print(line, flush=True)
        with log_path.open("a", encoding="utf-8") as file:
            file.write(line + "\n")

    per_window = []
    seen_tokens = {}
    consecutive_errors = 0

    def on_window(src, meta):
        nonlocal seen_tokens, consecutive_errors
        agents = {
            role: {f: v - seen_tokens.get(role, {}).get(f, 0) for f, v in totals.items()}
            for role, totals in usage.items()
        }
        seen_tokens = deepcopy(usage)
        first, last = meta["first"], meta["last"]
        (windows_dir / f"slides{first:03d}-{last:03d}.json").write_text(
            json.dumps(src, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        per_window.append({**meta, "llm_calls": _total(agents, "calls"), "agents": agents})
        log(
            f"  slides {first:>3}-{last:<3}: {meta['status'] or 'ERROR':9} "
            f"attempts={meta['attempts']} terms={len(meta['search_terms'])} "
            f"calls={_total(agents, 'calls')} time={meta['time_s']}s"
            + (f" !! {meta['error']}" if meta["error"] else "")
        )
        consecutive_errors = consecutive_errors + 1 if meta["error"] else 0
        if consecutive_errors >= MAX_CONSECUTIVE_ERRORS:
            log(f"  ABORTING {lecture_name(pdf)}: {consecutive_errors} windows failed in a row")
            raise RunAborted(
                f"{lecture_name(pdf)} aborted after {MAX_CONSECUTIVE_ERRORS} consecutive failures"
            )

    log(f"=== {lecture_name(pdf)} | model={model} | {pdf.name} ===")
    deck_t0 = time.perf_counter()
    render_dir = tempfile.mkdtemp(prefix=f"{lecture_name(pdf)}_")
    images = render_slides(pdf, dpi, render_dir)
    if max_slides:
        images = images[:max_slides]

    done_windows = load_done_windows(windows_dir, len(images), window_size) if resume_windows else {}
    if done_windows:
        log(f"  resuming: {len(done_windows)} cached window(s) loaded from windows/")

    windows_t0 = time.perf_counter()
    aborted = False
    try:
        final = await generate_lecture(
            provider, images, window_size, language=language,
            on_window=on_window, done_windows=done_windows,
            window_concurrency=window_concurrency,
        )
    except RunAborted:
        final, aborted = {}, True
    shutil.rmtree(render_dir, ignore_errors=True)

    lecture_md = final.get("lecture") or ""
    n_sections = writer_time = 0
    if lecture_md:
        writer_time = round(
            time.perf_counter() - windows_t0 - sum(w["time_s"] for w in per_window), 2
        )
        (out_dir / "lecture.md").write_text(lecture_md + "\n", encoding="utf-8")
        n_sections = sum(1 for ln in lecture_md.splitlines() if ln.startswith("## "))
        log(f"  WRITER: {len(per_window)} windows -> {n_sections} sections, {writer_time}s -> lecture.md")

    total_time = round(time.perf_counter() - deck_t0, 2)
    per_window.sort(key=lambda w: w["first"])
    stats = {
        "model": model,
        "critic_model": critic_model or model,
        "lecture": lecture_name(pdf),
        "pdf": str(pdf.relative_to(ROOT)),
        "window_size": window_size,
        "n_slides": sum(w["n_slides"] for w in per_window),
        "n_windows": len(per_window),
        "aborted": aborted,
        "n_sections": n_sections,
        "writer_time_s": writer_time,
        "total_llm_calls": _total(usage, "calls"),
        "total_input_tokens": _total(usage, "input_tokens"),
        "total_output_tokens": _total(usage, "output_tokens"),
        "total_terms": sum(len(w["search_terms"]) for w in per_window),
        "total_time_s": total_time,
        "per_agent": usage,
        "per_window": per_window,
    }
    (out_dir / "stats.json").write_text(json.dumps(stats, indent=2, ensure_ascii=False), encoding="utf-8")
    if aborted:
        raise RunAborted(f"{lecture_name(pdf)} aborted after {MAX_CONSECUTIVE_ERRORS} consecutive failures")
    log(
        f"  DONE {lecture_name(pdf)}: {stats['n_slides']} slides in {stats['n_windows']} windows, "
        f"{stats['total_llm_calls']} calls, {total_time}s"
    )
    return stats

def summarize(model, out_suffix=""):
    base = results_dir(model, out_suffix)
    stats_files = sorted(
        base.glob("lec*/stats.json"),
        key=lambda f: int(re.search(r"lec(\d+)", f.parent.name).group(1)),
    )
    decks = [json.loads(f.read_text(encoding="utf-8")) for f in stats_files]
    summary = {
        "model": model,
        "n_lectures": len(decks),
        "total_llm_calls": sum(d["total_llm_calls"] for d in decks),
        "total_input_tokens": sum(d["total_input_tokens"] for d in decks),
        "total_output_tokens": sum(d["total_output_tokens"] for d in decks),
        "total_terms": sum(d.get("total_terms", 0) for d in decks),
        "total_time_s": round(sum(d["total_time_s"] for d in decks), 2),
        "lectures": [
            {k: d[k] for k in ("lecture", "n_slides", "n_windows", "total_llm_calls", "total_time_s")}
            for d in decks
        ],
    }
    base.mkdir(parents=True, exist_ok=True)
    (base / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    return summary

async def unify(lecture_dir, model):
    windows = [
        json.loads(p.read_text(encoding="utf-8"))
        for p in sorted((lecture_dir / "windows").glob("slides*.json"))
    ]
    windows = [w for w in windows if (w.get("discourse") or "").strip()]
    if not windows:
        print(f"  {lecture_dir.name}: no non-empty windows, skipping")
        return {}

    usage = {}
    provider = InstrumentedProvider(usage, {"default": model})

    t0 = time.perf_counter()

    total_chars = sum(
        len(w["discourse"]) + len(w.get("wikipedia_data") or "") for w in windows
    )
    mode = "single" if total_chars <= SINGLE_PASS_CHARS else "chunked"

    lecture_md = await compose_lecture(provider, windows)
    n_sections = sum(1 for ln in lecture_md.splitlines() if ln.startswith("## "))

    (lecture_dir / "lecture.md").write_text(lecture_md + "\n", encoding="utf-8")
    unify_stats = {
        "model": model,
        "lecture": lecture_dir.name,
        "mode": mode,
        "lecture_title": next(
            (ln[2:].strip() for ln in lecture_md.splitlines() if ln.startswith("# ")),
            "Untitled",
        ),
        "n_windows_in": len(windows),
        "n_sections": n_sections,
        "llm_calls": _total(usage, "calls"),
        "total_input_tokens": _total(usage, "input_tokens"),
        "total_output_tokens": _total(usage, "output_tokens"),
        "time_s": round(time.perf_counter() - t0, 2),
        "per_stage": usage,
    }
    (lecture_dir / "unify_stats.json").write_text(
        json.dumps(unify_stats, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(
        f"  {lecture_dir.name} [{mode}]: {len(windows)} windows -> {n_sections} sections, "
        f"{unify_stats['llm_calls']} calls, {unify_stats['time_s']}s -> lecture.md"
    )
    return unify_stats

def unified_lectures(model, out_suffix=""):
    base = results_dir(model, out_suffix)
    return sorted(p for p in base.glob("lec*") if (p / "windows").is_dir())

def export_pdfs(model="", skip_done=False):
    base = results_dir(model) if model else EXPERIMENTS
    mds = sorted(base.glob("lec*/lecture.md")) if model else sorted(base.glob("*/lec*/lecture.md"))
    if not mds:
        print(f"No lecture.md under {base}")
        return {"ok": 0, "failed": 0, "skipped": 0}

    ok = failed = skipped = 0
    for md in mds:
        out = md.with_suffix(".pdf")
        if skip_done and out.exists():
            skipped += 1
            continue
        try:
            save_pdf(md.read_text(encoding="utf-8"), out)
            ok += 1
            print(f"  {md.parent.parent.name}/{md.parent.name} -> {out.name}")
        except Exception as e:
            failed += 1
            print(f"  !! {md.parent.parent.name}/{md.parent.name}: {type(e).__name__}: {e}")
    print(f"\n{ok} PDFs written, {failed} failed, {skipped} skipped.")
    return {"ok": ok, "failed": failed, "skipped": skipped}
