from typing import Optional
import tempfile
from pathlib import Path
from app.rag.config import rag_settings


def render_page_to_image(page, dpi: Optional[int] = None) -> str:
    resolution = dpi or 200
    pix = page.get_pixmap(dpi=resolution)
    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    tmp_path = tmp.name
    pix.save(tmp_path)
    tmp.close()
    return tmp_path
