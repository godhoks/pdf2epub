import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from unittest.mock import patch
from converter import find_calibre, CalibreNotFoundError


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
