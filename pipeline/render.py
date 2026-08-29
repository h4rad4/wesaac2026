from pathlib import Path

import fitz

def render_slides(pdf, dpi, dest):
    """Render each PDF page to a PNG in ``dest``; returns the paths in order."""
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    zoom = fitz.Matrix(dpi / 72, dpi / 72)

    paths = []
    with fitz.open(str(pdf)) as document:
        for index, page in enumerate(document):
            image_path = dest / f"p{index + 1:03d}.png"
            page.get_pixmap(matrix=zoom, alpha=False).save(image_path)
            paths.append(image_path)
    return paths
