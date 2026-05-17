import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from unittest.mock import patch
from converter import find_calibre, CalibreNotFoundError


def test_find_calibre_via_which():
    with patch('shutil.which', return_value='C:/Program Files/Calibre2/ebook-convert.exe'):
        result = find_calibre()
    assert result == 'C:/Program Files/Calibre2/ebook-convert.exe'


def test_find_calibre_not_found_raises():
    with patch('shutil.which', return_value=None), \
         patch('os.path.exists', return_value=False):
        with pytest.raises(CalibreNotFoundError):
            find_calibre()
