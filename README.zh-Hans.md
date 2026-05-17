# PDF2EPUB 转换器

**v1.0.0** · 🌐 [English](README.md) · [繁體中文](README.zh-Hant.md) · [简体中文](README.zh-Hans.md)

简单的桌面 GUI 工具，将 PDF 转换为 EPUB。输出的 EPUB 不含内建样式，由阅读器（如 Kobo）自行套用。

## 功能

- 支持纯文本 PDF 与扫描版 PDF（通过 Calibre OCR）
- CustomTkinter GUI，支持拖拽
- 保留 PDF 图片与章节结构
- 不嵌入 CSS，阅读器掌控排版
- 界面支持繁体中文、简体中文、英文

## 前置需求

安装 [Calibre](https://calibre-ebook.com/download)（免费）。转换引擎依赖其 `ebook-convert`。

## 安装与运行（源代码）

```bash
pip install -r requirements.txt
python main.py
```

## 打包成独立 .exe

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "PDF2EPUB" --icon icon.ico --add-data "icon.ico;." --collect-all customtkinter --collect-all tkinterdnd2 main.py
```

输出于 `dist/PDF2EPUB.exe`。对方仍需安装 Calibre。

## 项目结构

```
pdf2epub/
├── main.py          # 程序入口
├── gui.py           # CustomTkinter 窗口 + 多语言
├── converter.py     # Calibre 封装层
├── make_icon.py     # 生成 icon.ico
├── icon.ico
├── requirements.txt
└── tests/
    └── test_converter.py
```

## 依赖

- `customtkinter` — 现代感 GUI
- `pypdf` — 读取 PDF metadata
- `tkinterdnd2` — 拖拽支持
- `Pillow` — 图标生成
- Calibre（系统安装）— 转换引擎

## 许可证

MIT — 详见 [LICENSE](LICENSE)。
