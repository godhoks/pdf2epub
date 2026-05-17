# PDF2EPUB Converter

**v1.0.0** · 🌐 [English](README.md) · [繁體中文](README.zh-Hant.md) · [简体中文](README.zh-Hans.md)

[![Download .exe](https://img.shields.io/badge/Download-PDF2EPUB.exe-blue?style=for-the-badge&logo=windows)](https://github.com/godhoks/pdf2epub/releases/latest/download/PDF2EPUB.exe)

A simple desktop GUI tool that converts PDF files to EPUB format. Output EPUBs ship without bundled styles, letting your reader (Kobo, etc.) apply its own typography.

> Windows users: click the badge above to download the latest standalone `.exe`. You still need [Calibre](https://calibre-ebook.com/download) installed.

## Features

- Converts text-based and scanned PDFs (OCR via Calibre)
- Drag-and-drop GUI built with CustomTkinter
- Preserves images and chapter structure from the source PDF
- No bundled CSS — reader controls typography
- Interface available in Traditional Chinese, Simplified Chinese, and English

## Prerequisite

Install [Calibre](https://calibre-ebook.com/download) (free). The converter shells out to Calibre's `ebook-convert`.

## Install & Run (from source)

```bash
pip install -r requirements.txt
python main.py
```

## Build a Standalone .exe

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "PDF2EPUB" --icon icon.ico --add-data "icon.ico;." --collect-all customtkinter --collect-all tkinterdnd2 main.py
```

Output: `dist/PDF2EPUB.exe`. Recipients still need Calibre installed.

## Project Structure

```
pdf2epub/
├── main.py          # Entry point
├── gui.py           # CustomTkinter window + i18n
├── converter.py     # Calibre wrapper
├── make_icon.py     # Generates icon.ico
├── icon.ico
├── requirements.txt
└── tests/
    └── test_converter.py
```

## Dependencies

- `customtkinter` — modern GUI
- `pypdf` — PDF metadata reading
- `tkinterdnd2` — drag-and-drop
- `Pillow` — icon generation
- Calibre (system install) — conversion engine

## License

MIT — see [LICENSE](LICENSE).
