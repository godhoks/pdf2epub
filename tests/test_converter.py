import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from unittest.mock import patch, MagicMock
from converter import find_calibre, CalibreNotFoundError, read_pdf_metadata


def test_find_calibre_via_which():
    expected = r"C:\Program Files\Calibre2\ebook-convert.exe"
    with patch('shutil.which', return_value=expected):
        result = find_calibre()
    assert result == expected


def test_find_calibre_via_default_paths():
    with patch('shutil.which', return_value=None), \
         patch('os.path.exists', side_effect=lambda p: p == r"C:\Program Files\Calibre2\ebook-convert.exe"):
        result = find_calibre()
    assert result == r"C:\Program Files\Calibre2\ebook-convert.exe"


def test_find_calibre_not_found_raises():
    with patch('shutil.which', return_value=None), \
         patch('os.path.exists', return_value=False):
        with pytest.raises(CalibreNotFoundError):
            find_calibre()


def test_read_pdf_metadata_returns_title_and_author():
    mock_reader = MagicMock()
    mock_reader.metadata.title = "測試書名"
    mock_reader.metadata.author = "測試作者"

    with patch('converter.PdfReader', return_value=mock_reader):
        result = read_pdf_metadata("dummy.pdf")

    assert result["title"] == "測試書名"
    assert result["author"] == "測試作者"


def test_read_pdf_metadata_empty_returns_empty_strings():
    mock_reader = MagicMock()
    mock_reader.metadata.title = None
    mock_reader.metadata.author = None

    with patch('converter.PdfReader', return_value=mock_reader):
        result = read_pdf_metadata("dummy.pdf")

    assert result["title"] == ""
    assert result["author"] == ""


def test_build_command_contains_required_flags():
    from converter import build_command

    cmd = build_command(
        calibre_path="ebook-convert",
        input_pdf="in.pdf",
        output_epub="out.epub",
        title="書名",
        author="作者",
        language="zh-Hant",
    )
    assert cmd[:3] == ["ebook-convert", "in.pdf", "out.epub"]
    assert "--title" in cmd and "書名" in cmd
    assert "--authors" in cmd and "作者" in cmd
    assert "--language" in cmd and "zh-Hant" in cmd
    assert "--extra-css" in cmd


def test_build_command_no_styles():
    from converter import build_command

    cmd = build_command("ebook-convert", "a.pdf", "a.epub", "", "", "en")
    idx = cmd.index("--extra-css")
    assert cmd[idx + 1] == ""
    assert "--base-font-size" in cmd
    idx2 = cmd.index("--base-font-size")
    assert cmd[idx2 + 1] == "0"
