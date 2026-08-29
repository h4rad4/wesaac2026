import re
import shutil
import subprocess
import tempfile
import urllib.request
from pathlib import Path
from urllib.parse import urlsplit

import fitz

UA = "automated-agent/0.1 (educational research)"

MARKDOWN_IMAGE = re.compile(r"!\[((?:[^\[\]]|\[[^\]]*\])*)\]\(\s*(\S+?)\s*\)")

HEADER = r"""\usepackage{graphicx}
\setkeys{Gin}{width=0.8\linewidth,keepaspectratio}
\usepackage{caption}
\captionsetup{labelformat=empty,justification=centering,font=it}
\usepackage{float}
\makeatletter
\renewcommand*{\fps@figure}{H}
\makeatother
"""

class PdfUnavailable(RuntimeError):
    pass

def _close_stray_math(markdown):
    """Close inline math left open by truncated LLM output.

    A line with an odd number of unescaped ``$`` means an unterminated formula;
    closing it keeps pandoc/XeTeX from pairing the delimiter with a later one
    and blowing up with 'Missing $ inserted'. Display math ($$...$$) and fenced
    code blocks are left untouched.
    """
    lines = markdown.split("\n")
    in_fence = False
    for index, line in enumerate(lines):
        stripped = line.lstrip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        without_display = re.sub(r"\$\$.*?\$\$", "", line)
        without_display = re.sub(r"^\$\$|\$\$$", "", without_display)
        dollars = len(re.findall(r"(?<!\\)\$", without_display))
        if dollars % 2 == 1:
            lines[index] = line.rstrip() + "$"
    return "\n".join(lines)

def save_pdf(markdown, out):
    if not (shutil.which("pandoc") and shutil.which("tectonic")):
        raise PdfUnavailable("PDF export needs `pandoc` and `tectonic` on PATH (see README).")
    if not markdown.strip():
        raise PdfUnavailable("PDF export received empty Markdown; generate or load `md` first.")

    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)

    def tighten(match):
        inner = match.group(1)
        return f"${inner.strip()}$" if re.search(r"[\\_^{}]", inner) else match.group(0)

    prepared = re.sub(r"(?<!\$)\$([^$\n]+?)\$(?!\$)", tighten, markdown)
    prepared = _close_stray_math(prepared)

    with tempfile.TemporaryDirectory() as workdir:
        workdir = Path(workdir)
        generated = workdir / "material.pdf"
        downloaded = 0

        def localize(match):
            nonlocal downloaded
            caption, url = match.group(1), match.group(2)
            if not url.lower().startswith(("http://", "https://")):
                return match.group(0)

            downloaded += 1
            destination = workdir / f"img{downloaded}.png"
            try:
                request = urllib.request.Request(url, headers={"User-Agent": UA})
                with urllib.request.urlopen(request, timeout=30) as response:
                    content_type = response.headers.get("Content-Type", "").split(";")[0].strip()
                    data = response.read()
                if not (content_type.startswith("image/") or "svg" in content_type):
                    return ""
                file_type = content_type.split("/")[-1].split("+")[0]
                if not file_type:
                    file_type = Path(urlsplit(url).path).suffix.lstrip(".")
                document = fitz.open(stream=data, filetype=file_type)
                document[0].get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False).save(destination)
            except Exception:
                return ""

            return f"\n\n![{caption}]({destination})\n\n"

        (workdir / "material.md").write_text(
            MARKDOWN_IMAGE.sub(localize, prepared), encoding="utf-8"
        )
        (workdir / "header.tex").write_text(HEADER, encoding="utf-8")

        command = [
            "pandoc",
            str(workdir / "material.md"),
            "-f", "markdown+tex_math_single_backslash",
            "-o", str(generated),
            "--pdf-engine=tectonic",
            "-H", str(workdir / "header.tex"),
            "-V", "geometry:margin=1in",
            "-V", "linkcolor:blue",
        ]
        try:
            subprocess.run(
                command, check=True, capture_output=True, text=True,
                encoding="utf-8", errors="replace",
            )
        except subprocess.CalledProcessError as error:
            details = (error.stderr or error.stdout or str(error)).strip()
            raise PdfUnavailable(f"PDF export failed:\n{details}") from error

        generated.replace(out)

    return out
