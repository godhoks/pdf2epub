# PDF2EPUB 轉換器

**v1.0.0** · 🌐 [English](README.md) · [繁體中文](README.zh-Hant.md) · [简体中文](README.zh-Hans.md)

[![下載 .exe](https://img.shields.io/badge/下載-PDF2EPUB.exe-blue?style=for-the-badge&logo=windows)](https://github.com/godhoks/pdf2epub/releases/latest/download/PDF2EPUB.exe)

簡單的桌面 GUI 工具，將 PDF 轉成 EPUB。輸出的 EPUB 不含內建樣式，由閱讀器（如 Kobo）自行套用。

> Windows 使用者：點上方按鈕直接下載最新的獨立 `.exe`。仍需安裝 [Calibre](https://calibre-ebook.com/download)。

## 功能

- 支援純文字 PDF 與掃描版 PDF（透過 Calibre OCR）
- CustomTkinter GUI，支援拖曳
- 保留 PDF 圖片與章節結構
- 不嵌入 CSS，閱讀器掌控排版
- 介面支援繁體中文、簡體中文、英文

## 前置需求

安裝 [Calibre](https://calibre-ebook.com/download)（免費）。轉換引擎依賴其 `ebook-convert`。

## 安裝與執行（原始碼）

```bash
pip install -r requirements.txt
python main.py
```

## 打包成獨立 .exe

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "PDF2EPUB" --icon icon.ico --add-data "icon.ico;." --collect-all customtkinter --collect-all tkinterdnd2 main.py
```

輸出於 `dist/PDF2EPUB.exe`。仍需安裝 Calibre。

## 專案結構

```
pdf2epub/
├── main.py          # 程式入口
├── gui.py           # CustomTkinter 視窗 + 多語系
├── converter.py     # Calibre 包裝層
├── make_icon.py     # 產生 icon.ico
├── icon.ico
├── requirements.txt
└── tests/
    └── test_converter.py
```

## 相依套件

- `customtkinter` — 現代感 GUI
- `pypdf` — 讀取 PDF metadata
- `tkinterdnd2` — 拖曳支援
- `Pillow` — 圖示生成
- Calibre（系統安裝）— 轉換引擎

## 授權

MIT — 詳見 [LICENSE](LICENSE)。
