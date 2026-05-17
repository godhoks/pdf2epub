import os
import threading
import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD
from converter import find_calibre, build_command, run_conversion, read_pdf_metadata, CalibreNotFoundError

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

EPUB_LANG_MAP = {
    "繁體中文": "zh-Hant",
    "簡體中文": "zh-Hans",
    "English": "en",
}

T = {
    "zh-Hant": {
        "title": "PDF → EPUB 轉換器",
        "input_label": "📄 輸入 PDF",
        "input_ph": "拖曳 PDF 至此，或點右側瀏覽",
        "browse_pdf": "瀏覽",
        "output_label": "📁 輸出資料夾",
        "output_ph": "預設：與 PDF 同資料夾",
        "select": "選擇",
        "meta_label": "📝 書籍資訊",
        "title_lbl": "書名：",
        "author_lbl": "作者：",
        "lang_lbl": "語言：",
        "ui_lang_lbl": "介面語言：",
        "convert": "開始轉換",
        "converting": "轉換中...",
        "open_folder": "📂 開啟檔案位置",
        "no_pdf": "⚠️ 請先選擇有效的 PDF 檔案",
        "no_calibre": "❌ 未偵測到 Calibre，請先安裝：https://calibre-ebook.com/download\n   安裝後重新啟動此程式",
        "done": "✅ 完成！儲存至：",
        "failed": "❌ 轉換失敗，請查看上方 log",
    },
    "zh-Hans": {
        "title": "PDF → EPUB 转换器",
        "input_label": "📄 输入 PDF",
        "input_ph": "拖拽 PDF 至此，或点右侧浏览",
        "browse_pdf": "浏览",
        "output_label": "📁 输出文件夹",
        "output_ph": "默认：与 PDF 同文件夹",
        "select": "选择",
        "meta_label": "📝 书籍信息",
        "title_lbl": "书名：",
        "author_lbl": "作者：",
        "lang_lbl": "语言：",
        "ui_lang_lbl": "界面语言：",
        "convert": "开始转换",
        "converting": "转换中...",
        "open_folder": "📂 打开文件位置",
        "no_pdf": "⚠️ 请先选择有效的 PDF 文件",
        "no_calibre": "❌ 未检测到 Calibre，请先安装：https://calibre-ebook.com/download\n   安装后重新启动此程序",
        "done": "✅ 完成！保存至：",
        "failed": "❌ 转换失败，请查看上方 log",
    },
    "en": {
        "title": "PDF → EPUB Converter",
        "input_label": "📄 Input PDF",
        "input_ph": "Drag PDF here or click Browse",
        "browse_pdf": "Browse",
        "output_label": "📁 Output Folder",
        "output_ph": "Default: same folder as PDF",
        "select": "Select",
        "meta_label": "📝 Book Info",
        "title_lbl": "Title:",
        "author_lbl": "Author:",
        "lang_lbl": "Language:",
        "ui_lang_lbl": "UI Language:",
        "convert": "Convert",
        "converting": "Converting...",
        "open_folder": "📂 Open File Location",
        "no_pdf": "⚠️ Please select a valid PDF file",
        "no_calibre": "❌ Calibre not found. Please install: https://calibre-ebook.com/download\n   Restart the app after installation.",
        "done": "✅ Done! Saved to: ",
        "failed": "❌ Conversion failed. Check log above.",
    },
}

UI_LANG_OPTIONS = ["繁體中文", "簡體中文", "English"]
UI_LANG_CODE = {"繁體中文": "zh-Hant", "簡體中文": "zh-Hans", "English": "en"}


class App(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self):
        super().__init__()
        self.TkdndVersion = TkinterDnD._require(self)
        self.ui_lang = "zh-Hant"
        self.geometry("520x620")
        self.resizable(False, False)
        self._build_ui()
        self._check_calibre()

    def _t(self, key):
        return T[self.ui_lang][key]

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        pad = {"padx": 20, "pady": (10, 4)}

        # 介面語言切換
        f0 = ctk.CTkFrame(self, fg_color="transparent")
        f0.grid(row=0, column=0, sticky="ew", padx=20, pady=(8, 0))
        self.ui_lang_lbl = ctk.CTkLabel(f0, text="🌐")
        self.ui_lang_lbl.grid(row=0, column=0, padx=(0, 6))
        self.ui_lang_var = ctk.StringVar(value="繁體中文")
        ctk.CTkOptionMenu(f0, variable=self.ui_lang_var, values=UI_LANG_OPTIONS,
                          width=130, command=self._on_ui_lang_change).grid(row=0, column=1, sticky="w")

        # 輸入 PDF
        self.input_lbl = ctk.CTkLabel(self, text=self._t("input_label"), anchor="w")
        self.input_lbl.grid(row=1, column=0, sticky="ew", **pad)
        f1 = ctk.CTkFrame(self)
        f1.grid(row=2, column=0, sticky="ew", padx=20)
        f1.grid_columnconfigure(0, weight=1)
        self.input_entry = ctk.CTkEntry(f1, placeholder_text=self._t("input_ph"))
        self.input_entry.grid(row=0, column=0, sticky="ew", padx=(6, 4), pady=6)
        self.browse_pdf_btn = ctk.CTkButton(f1, text=self._t("browse_pdf"), width=64, command=self._browse_pdf)
        self.browse_pdf_btn.grid(row=0, column=1, padx=(0, 6), pady=6)

        # 輸出資料夾
        self.output_lbl = ctk.CTkLabel(self, text=self._t("output_label"), anchor="w")
        self.output_lbl.grid(row=3, column=0, sticky="ew", **pad)
        f2 = ctk.CTkFrame(self)
        f2.grid(row=4, column=0, sticky="ew", padx=20)
        f2.grid_columnconfigure(0, weight=1)
        self.output_entry = ctk.CTkEntry(f2, placeholder_text=self._t("output_ph"))
        self.output_entry.grid(row=0, column=0, sticky="ew", padx=(6, 4), pady=6)
        self.select_btn = ctk.CTkButton(f2, text=self._t("select"), width=64, command=self._browse_output)
        self.select_btn.grid(row=0, column=1, padx=(0, 6), pady=6)

        # 書籍資訊
        self.meta_lbl = ctk.CTkLabel(self, text=self._t("meta_label"), anchor="w")
        self.meta_lbl.grid(row=5, column=0, sticky="ew", **pad)
        f3 = ctk.CTkFrame(self)
        f3.grid(row=6, column=0, sticky="ew", padx=20)
        f3.grid_columnconfigure(1, weight=1)
        self.title_lbl = ctk.CTkLabel(f3, text=self._t("title_lbl"))
        self.title_lbl.grid(row=0, column=0, padx=10, pady=5)
        self.title_entry = ctk.CTkEntry(f3)
        self.title_entry.grid(row=0, column=1, sticky="ew", padx=(0, 10), pady=5)
        self.author_lbl = ctk.CTkLabel(f3, text=self._t("author_lbl"))
        self.author_lbl.grid(row=1, column=0, padx=10, pady=5)
        self.author_entry = ctk.CTkEntry(f3)
        self.author_entry.grid(row=1, column=1, sticky="ew", padx=(0, 10), pady=5)
        self.lang_lbl = ctk.CTkLabel(f3, text=self._t("lang_lbl"))
        self.lang_lbl.grid(row=2, column=0, padx=10, pady=5)
        self.epub_lang_var = ctk.StringVar(value="繁體中文")
        ctk.CTkOptionMenu(f3, variable=self.epub_lang_var, values=list(EPUB_LANG_MAP.keys())).grid(
            row=2, column=1, sticky="w", padx=(0, 10), pady=5)

        # 轉換按鈕
        self.convert_btn = ctk.CTkButton(self, text=self._t("convert"), height=40, command=self._start_conversion)
        self.convert_btn.grid(row=7, column=0, padx=20, pady=14, sticky="ew")

        # 進度條
        self.progress = ctk.CTkProgressBar(self)
        self.progress.set(0)
        self.progress.grid(row=8, column=0, padx=20, sticky="ew")

        # Log 區域
        self.log_box = ctk.CTkTextbox(self, height=120, state="disabled")
        self.log_box.grid(row=9, column=0, padx=20, pady=(6, 10), sticky="ew")

        # 拖曳
        self.input_entry.drop_target_register(DND_FILES)
        self.input_entry.dnd_bind("<<Drop>>", self._on_drop)

        self.title(self._t("title"))

    def _on_ui_lang_change(self, choice):
        self.ui_lang = UI_LANG_CODE[choice]
        self.title(self._t("title"))
        self.input_lbl.configure(text=self._t("input_label"))
        self.input_entry.configure(placeholder_text=self._t("input_ph"))
        self.browse_pdf_btn.configure(text=self._t("browse_pdf"))
        self.output_lbl.configure(text=self._t("output_label"))
        self.output_entry.configure(placeholder_text=self._t("output_ph"))
        self.select_btn.configure(text=self._t("select"))
        self.meta_lbl.configure(text=self._t("meta_label"))
        self.title_lbl.configure(text=self._t("title_lbl"))
        self.author_lbl.configure(text=self._t("author_lbl"))
        self.lang_lbl.configure(text=self._t("lang_lbl"))
        if self.convert_btn.cget("state") == "normal":
            self.convert_btn.configure(text=self._t("convert"))

    def _check_calibre(self):
        try:
            find_calibre()
        except CalibreNotFoundError:
            self._log(self._t("no_calibre"))
            self.convert_btn.configure(state="disabled")

    def _browse_pdf(self):
        from tkinter import filedialog
        path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if path:
            self._set_pdf_path(path)

    def _browse_output(self):
        from tkinter import filedialog
        path = filedialog.askdirectory()
        if path:
            self.output_entry.delete(0, "end")
            self.output_entry.insert(0, path)

    def _on_drop(self, event):
        path = event.data.strip("{}")
        if path.lower().endswith(".pdf"):
            self._set_pdf_path(path)

    def _set_pdf_path(self, path: str):
        self.input_entry.delete(0, "end")
        self.input_entry.insert(0, path)
        meta = read_pdf_metadata(path)
        self.title_entry.delete(0, "end")
        self.title_entry.insert(0, meta["title"])
        self.author_entry.delete(0, "end")
        self.author_entry.insert(0, meta["author"])

    def _log(self, text: str):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", text + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def _start_conversion(self):
        input_path = self.input_entry.get().strip()
        if not input_path or not os.path.exists(input_path):
            self._log(self._t("no_pdf"))
            return

        output_dir = self.output_entry.get().strip() or os.path.dirname(input_path)
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(output_dir, base_name + ".epub")

        try:
            calibre = find_calibre()
        except CalibreNotFoundError as e:
            self._log(f"❌ {e}")
            return

        cmd = build_command(
            calibre_path=calibre,
            input_pdf=input_path,
            output_epub=output_path,
            title=self.title_entry.get().strip(),
            author=self.author_entry.get().strip(),
            language=EPUB_LANG_MAP[self.epub_lang_var.get()],
        )

        self.convert_btn.configure(state="disabled", text=self._t("converting"))
        self.progress.start()
        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.configure(state="disabled")

        def worker():
            success = run_conversion(cmd, on_log=lambda line: self.after(0, self._log, line))
            self.after(0, self._on_done, success, output_path)

        threading.Thread(target=worker, daemon=True).start()

    def _on_done(self, success: bool, output_path: str):
        self.progress.stop()
        self.progress.set(1.0 if success else 0)
        self.convert_btn.configure(state="normal", text=self._t("convert"))
        if success:
            self._log(f"{self._t('done')}{output_path}")
            output_dir = os.path.dirname(output_path)
            ctk.CTkButton(
                self, text=self._t("open_folder"),
                command=lambda: os.startfile(output_dir)
            ).grid(row=10, column=0, padx=20, pady=(0, 10), sticky="ew")
        else:
            self._log(self._t("failed"))
