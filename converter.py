import shutil
import os
import subprocess
from typing import Callable
from pypdf import PdfReader


class CalibreNotFoundError(Exception):
    pass


CALIBRE_DEFAULT_PATHS = [
    r"C:\Program Files\Calibre2\ebook-convert.exe",
    r"C:\Program Files (x86)\Calibre2\ebook-convert.exe",
]


def find_calibre() -> str:
    path = shutil.which("ebook-convert")
    if path:
        return path
    for p in CALIBRE_DEFAULT_PATHS:
        if os.path.exists(p):
            return p
    raise CalibreNotFoundError(
        "找不到 Calibre。請安裝：https://calibre-ebook.com/download"
    )


def read_pdf_metadata(pdf_path: str) -> dict:
    try:
        reader = PdfReader(pdf_path)
        meta = reader.metadata
        return {
            "title": (meta.title or "") if meta else "",
            "author": (meta.author or "") if meta else "",
        }
    except Exception:
        return {"title": "", "author": ""}


def build_command(
    calibre_path: str,
    input_pdf: str,
    output_epub: str,
    title: str,
    author: str,
    language: str,
) -> list:
    return [
        calibre_path, input_pdf, output_epub,
        "--title", title,
        "--authors", author,
        "--language", language,
        "--chapter-mark", "pagebreak",
        "--extra-css", "",
        "--base-font-size", "0",
        "--font-size-mapping", "0,0,0,0,0,0",
    ]


def run_conversion(command: list, on_log: Callable[[str], None]) -> bool:
    creationflags = getattr(subprocess, 'CREATE_NO_WINDOW', 0)
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        creationflags=creationflags,
    )
    while True:
        line = process.stdout.readline()
        if not line:
            break
        on_log(line.decode("utf-8", errors="replace").strip())
    process.wait()
    return process.returncode == 0
