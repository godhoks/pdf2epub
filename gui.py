import os
import threading
import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD
from converter import find_calibre, build_command, run_conversion, read_pdf_metadata, CalibreNotFoundError

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

LANGUAGE_MAP = {
    "繁體中文": "zh-Hant",
    "簡體中文": "zh-Hans",
    "English": "en",
}


class App(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self):
        super().__init__()
        self.TkdndVersion = TkinterDnD._require(self)
        self.title("PDF → EPUB 轉換器")
        self.geometry("520x580")
        self.resizable(False, False)
        self._build_ui()
        self._check_calibre()

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        pad = {"padx": 20, "pady": (10, 4)}

        # 輸入 PDF
        ctk.CTkLabel(self, text="📄 輸入 PDF", anchor="w").grid(row=0, column=0, sticky="ew", **pad)
        f1 = ctk.CTkFrame(self)
        f1.grid(row=1, column=0, sticky="ew", padx=20)
        f1.grid_columnconfigure(0, weight=1)
        self.input_entry = ctk.CTkEntry(f1, placeholder_text="拖曳 PDF 至此，或點右側瀏覽")
        self.input_entry.grid(row=0, column=0, sticky="ew", padx=(6, 4), pady=6)
        ctk.CTkButton(f1, text="瀏覽", width=64, command=self._browse_pdf).grid(row=0, column=1, padx=(0, 6), pady=6)

        # 輸出資料夾
        ctk.CTkLabel(self, text="📁 輸出資料夾", anchor="w").grid(row=2, column=0, sticky="ew", **pad)
        f2 = ctk.CTkFrame(self)
        f2.grid(row=3, column=0, sticky="ew", padx=20)
        f2.grid_columnconfigure(0, weight=1)
        self.output_entry = ctk.CTkEntry(f2, placeholder_text="預設：與 PDF 同資料夾")
        self.output_entry.grid(row=0, column=0, sticky="ew", padx=(6, 4), pady=6)
        ctk.CTkButton(f2, text="選擇", width=64, command=self._browse_output).grid(row=0, column=1, padx=(0, 6), pady=6)

        # 書籍資訊
        ctk.CTkLabel(self, text="📝 書籍資訊", anchor="w").grid(row=4, column=0, sticky="ew", **pad)
        f3 = ctk.CTkFrame(self)
        f3.grid(row=5, column=0, sticky="ew", padx=20)
        f3.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(f3, text="書名：").grid(row=0, column=0, padx=10, pady=5)
        self.title_entry = ctk.CTkEntry(f3)
        self.title_entry.grid(row=0, column=1, sticky="ew", padx=(0, 10), pady=5)
        ctk.CTkLabel(f3, text="作者：").grid(row=1, column=0, padx=10, pady=5)
        self.author_entry = ctk.CTkEntry(f3)
        self.author_entry.grid(row=1, column=1, sticky="ew", padx=(0, 10), pady=5)
        ctk.CTkLabel(f3, text="語言：").grid(row=2, column=0, padx=10, pady=5)
        self.language_var = ctk.StringVar(value="繁體中文")
        ctk.CTkOptionMenu(f3, variable=self.language_var, values=list(LANGUAGE_MAP.keys())).grid(row=2, column=1, sticky="w", padx=(0, 10), pady=5)

        # 轉換按鈕
        self.convert_btn = ctk.CTkButton(self, text="開始轉換", height=40, command=self._start_conversion)
        self.convert_btn.grid(row=6, column=0, padx=20, pady=14, sticky="ew")

        # 進度條
        self.progress = ctk.CTkProgressBar(self)
        self.progress.set(0)
        self.progress.grid(row=7, column=0, padx=20, sticky="ew")

        # Log 區域
        self.log_box = ctk.CTkTextbox(self, height=120, state="disabled")
        self.log_box.grid(row=8, column=0, padx=20, pady=(6, 10), sticky="ew")

        # 拖曳
        self.input_entry.drop_target_register(DND_FILES)
        self.input_entry.dnd_bind("<<Drop>>", self._on_drop)

    def _check_calibre(self):
        try:
            find_calibre()
        except CalibreNotFoundError:
            self._log("❌ 未偵測到 Calibre，請先安裝：https://calibre-ebook.com/download")
            self._log("   安裝後重新啟動此程式")
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
            self._log("⚠️ 請先選擇有效的 PDF 檔案")
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
            language=LANGUAGE_MAP[self.language_var.get()],
        )

        self.convert_btn.configure(state="disabled", text="轉換中...")
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
        self.convert_btn.configure(state="normal", text="開始轉換")
        if success:
            self._log(f"✅ 完成！儲存至：{output_path}")
            output_dir = os.path.dirname(output_path)
            ctk.CTkButton(
                self, text="📂 開啟檔案位置",
                command=lambda: os.startfile(output_dir)
            ).grid(row=9, column=0, padx=20, pady=(0, 10), sticky="ew")
        else:
            self._log("❌ 轉換失敗，請查看上方 log")
