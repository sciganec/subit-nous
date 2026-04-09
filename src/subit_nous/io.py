"""Multimodal input: read files and convert to SUBIT archetypes."""

from pathlib import Path
from typing import Union, Optional

from .core import text_to_subit


def read_file(filepath: Union[str, Path]) -> Optional[str]:
    """
    Read text from a file.
    Supports .txt, .md, .py, .json, .csv, etc. (any text-based format).
    Returns None if file cannot be read as text.
    """
    path = Path(filepath)
    if not path.is_file():
        return None

    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return None


def file_to_subit(
    filepath: Union[str, Path],
    chunk_size: int = 1000,
    pdf_page: int = 0,
    image_api_key: Optional[str] = None,
) -> Optional[int]:
    """
    Convert any supported file (text, PDF, image) into an 8‑bit archetype.

    Args:
        filepath: Path to the file.
        chunk_size: For text files, characters to read.
        pdf_page: For PDF, which page to extract (0‑based).
        image_api_key: Optional Claude API key for image analysis.
                       If None, images are skipped (return None).

    Returns:
        Archetype ID (0–255) or None if unsupported / error.
    """
    path = Path(filepath)
    ext = path.suffix.lower()

    # Text files
    if ext in {".txt", ".md", ".py", ".json", ".yaml", ".yml", ".csv", ".xml", ".html", ".css", ".js"}:
        text = read_file(path)
        if text:
            return text_to_subit(text, chunk_size)
        return None

    # PDF (optional dependency)
    if ext == ".pdf":
        try:
            import PyPDF2
        except ImportError:
            return None
        try:
            with open(path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                if pdf_page < len(reader.pages):
                    page_text = reader.pages[pdf_page].extract_text()
                    if page_text:
                        return text_to_subit(page_text, chunk_size)
        except Exception:
            pass
        return None

    # Images (optional, requires API key)
    if ext in {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}:
        if not image_api_key:
            return None
        try:
            import base64
            import requests
            from PIL import Image
        except ImportError:
            return None

        try:
            with open(path, "rb") as f:
                img_data = base64.b64encode(f.read()).decode()
            # Simple heuristic without API: use average color brightness as fallback
            if not image_api_key or image_api_key == "fallback":
                img = Image.open(path)
                img.thumbnail((100, 100))
                avg = sum(img.convert("L").getdata()) / (img.size[0] * img.size[1])
                # Map brightness to archetype (very crude)
                if avg < 64:
                    return 0b00000000  # META (dark)
                elif avg < 128:
                    return 0b01010101  # MESO
                elif avg < 192:
                    return 0b10101010  # MICRO
                else:
                    return 0b11111111  # MACRO
            # Real API call (Claude Vision) – simplified
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": image_api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json"
                },
                json={
                    "model": "claude-3-opus-20240229",
                    "max_tokens": 100,
                    "messages": [{
                        "role": "user",
                        "content": [
                            {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": img_data}},
                            {"type": "text", "text": "Classify this image into one of four archetypes (MICRO,MACRO,MESO,META). Return only the 8‑bit number as 8 binary digits, e.g., 10101010."}
                        ]
                    }]
                },
                timeout=10
            )
            if response.status_code == 200:
                bits_str = response.json()["content"][0]["text"].strip()
                return int(bits_str, 2)
        except Exception:
            pass
        return None

    # Unsupported
    return None