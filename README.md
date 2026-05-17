# PDF → EPUB 轉換器

將 PDF 檔案轉換為 EPUB 電子書格式的桌面工具，輸出樣式由閱讀器（如 Kobo）自行套用。

## 功能

- 支援純文字 PDF 與掃描版 PDF（OCR）
- GUI 介面，支援拖曳
- 保留 PDF 圖片
- 自動偵測章節結構，保留原有目錄
- 輸出 EPUB 不含內建樣式
- 支援繁體中文、簡體中文、English

## 前置需求

安裝 [Calibre](https://calibre-ebook.com/download)（免費），轉換引擎依賴其 `ebook-convert`。

## 安裝與執行

```bash
pip install -r requirements.txt
python main.py
```

## 打包成 .exe

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "PDF2EPUB轉換器" --collect-all customtkinter --collect-all tkinterdnd2 main.py
```

輸出在 `dist/PDF2EPUB轉換器.exe`。

## 專案結構

```
pdf2epub/
├── main.py          # 程式入口
├── gui.py           # CustomTkinter 視窗
├── converter.py     # 呼叫 Calibre 邏輯
├── requirements.txt
└── tests/
    └── test_converter.py
```

## 相依套件

- `customtkinter` — 現代感 GUI
- `pypdf` — 讀取 PDF metadata
- `tkinterdnd2` — 拖曳支援
- Calibre（系統安裝）— 轉換引擎
