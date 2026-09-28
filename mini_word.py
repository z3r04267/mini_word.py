import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font, colorchooser
import os

class MiniWord:
    def __init__(self, root):
        self.root = root
        self.root.title("Мини-Word")
        self.root.geometry("900x700")

        self.current_file = None
        self.text_widget = None
        self.font_family = tk.StringVar(value="Arial")
        self.font_size = tk.IntVar(value=14)
        self.font_bold = tk.BooleanVar(value=False)
        self.font_italic = tk.BooleanVar(value=False)
        self.text_color = "black"
        self.bg_color = "white"

        self.create_menu()
        self.create_toolbar()
        self.create_text_area()
        self.create_statusbar()
        self.bind_shortcuts()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    # ---------- МЕНЮ ----------
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Новый", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Открыть", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Сохранить", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Сохранить как", command=self.save_as_file, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.on_closing)

        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Правка", menu=edit_menu)
        edit_menu.add_command(label="Отменить", command=self.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Повторить", command=self.redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Вырезать", command=self.cut, accelerator="Ctrl+X")
        edit_menu.add_command(label="Копировать", command=self.copy, accelerator="Ctrl+C")
        edit_menu.add_command(label="Вставить", command=self.paste, accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="Найти и заменить", command=self.find_replace)

        format_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Формат", menu=format_menu)
        format_menu.add_command(label="Жирный", command=self.toggle_bold, accelerator="Ctrl+B")
        format_menu.add_command(label="Курсив", command=self.toggle_italic, accelerator="Ctrl+I")
        format_menu.add_separator()
        format_menu.add_command(label="Цвет текста", command=self.choose_text_color)
        format_menu.add_command(label="Цвет фона", command=self.choose_bg_color)

        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Вид", menu=view_menu)
        view_menu.add_command(label="Тёмная тема", command=lambda: self.set_theme("dark"))
        view_menu.add_command(label="Светлая тема", command=lambda: self.set_theme("light"))

    # ---------- ПАНЕЛЬ ИНСТРУМЕНТОВ ----------
    def create_toolbar(self):
        toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Шрифт
        tk.Label(toolbar, text="Шрифт:").pack(side=tk.LEFT, padx=2)
        fonts = list(font.families())
        font_menu = ttk.Combobox(toolbar, textvariable=self.font_family, values=fonts, width=20, state="readonly")
        font_menu.pack(side=tk.LEFT, padx=2)
        font_menu.bind("<<ComboboxSelected>>", lambda e: self.apply_font())

        # Размер
        tk.Label(toolbar, text="Размер:").pack(side=tk.LEFT, padx=2)
        size_spin = tk.Spinbox(toolbar, from_=8, to=72, textvariable=self.font_size, width=4, command=self.apply_font)
        size_spin.pack(side=tk.LEFT, padx=2)

        # Жирный / Курсив
        tk.Checkbutton(toolbar, text="Ж", variable=self.font_bold, command=self.toggle_bold,
                       font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=2)
        tk.Checkbutton(toolbar, text="К", variable=self.font_italic, command=self.toggle_italic,
                       font=("Arial", 10, "italic")).pack(side=tk.LEFT, padx=2)

        # Цвет
        tk.Button(toolbar, text="Текст", command=self.choose_text_color).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text="Фон", command=self.choose_bg_color).pack(side=tk.LEFT, padx=2)

        # Выравнивание
        tk.Button(toolbar, text="⬅", command=lambda: self.align("left")).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text="⬌", command=lambda: self.align("center")).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text="➡", command=lambda: self.align("right")).pack(side=tk.LEFT, padx=2)

    # ---------- ТЕКСТОВОЕ ПОЛЕ ----------
    def create_text_area(self):
        self.text_widget = tk.Text(self.root, wrap=tk.WORD, undo=True, font=("Arial", 14))
        self.text_widget.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

    # ---------- СТАТУС-БАР ----------
    def create_statusbar(self):
        self.status = tk.Label(self.root, text="Готов", anchor="w", bd=1, relief=tk.SUNKEN)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    # ---------- ГОРЯЧИЕ КЛАВИШИ ----------
    def bind_shortcuts(self):
        self.root.bind("<Control-n>", lambda e: self.new_file())
        self.root.bind("<Control-o>", lambda e: self.open_file())
        self.root.bind("<Control-s>", lambda e: self.save_file())
        self.root.bind("<Control-S>", lambda e: self.save_as_file())
        self.root.bind("<Control-b>", lambda e: self.toggle_bold())
        self.root.bind("<Control-i>", lambda e: self.toggle_italic())
        self.root.bind("<Control-z>", lambda e: self.undo())
        self.root.bind("<Control-y>", lambda e: self.redo())

    # ---------- ДЕЙСТВИЯ ----------
    def new_file(self):
        self.text_widget.delete("1.0", tk.END)
        self.current_file = None
        self.root.title("Мини-Word — Новый документ")

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if path:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            self.text_widget.delete("1.0", tk.END)
            self.text_widget.insert("1.0", content)
            self.current_file = path
            self.root.title(f"Мини-Word — {os.path.basename(path)}")

    def save_file(self):
        if self.current_file:
            with open(self.current_file, "w", encoding="utf-8") as f:
                f.write(self.text_widget.get("1.0", tk.END))
            self.status.config(text=f"Сохранено: {os.path.basename(self.current_file)}")
        else:
            self.save_as_file()

    def save_as_file(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text files", "*.txt")])
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.text_widget.get("1.0", tk.END))
            self.current_file = path
            self.root.title(f"Мини-Word — {os.path.basename(path)}")
            self.status.config(text=f"Сохранено: {os.path.basename(path)}")

    def undo(self):
        try:
            self.text_widget.edit_undo()
        except:
            pass

    def redo(self):
        try:
            self.text_widget.edit_redo()
        except:
            pass

    def cut(self):
        self.text_widget.event_generate("<<Cut>>")

    def copy(self):
        self.text_widget.event_generate("<<Copy>>")

    def paste(self):
        self.text_widget.event_generate("<<Paste>>")

    def toggle_bold(self):
        self.font_bold.set(not self.font_bold.get())
        self.apply_font()

    def toggle_italic(self):
        self.font_italic.set(not self.font_italic.get())
        self.apply_font()

    def apply_font(self):
        weight = "bold" if self.font_bold.get() else "normal"
        slant = "italic" if self.font_italic.get() else "roman"
        self.text_widget.config(font=(self.font_family.get(), self.font_size.get(), weight, slant))

    def choose_text_color(self):
        color = colorchooser.askcolor(title="Цвет текста")[1]
        if color:
            self.text_widget.config(fg=color)
            self.text_color = color

    def choose_bg_color(self):
        color = colorchooser.askcolor(title="Цвет фона")[1]
        if color:
            self.text_widget.config(bg=color)
            self.bg_color = color

    def align(self, direction):
        self.text_widget.tag_configure("align", justify=direction)
        self.text_widget.tag_add("align", "1.0", tk.END)

    def find_replace(self):
        find_win = tk.Toplevel(self.root)
        find_win.title("Найти и заменить")
        find_win.geometry("400x200")

        tk.Label(find_win, text="Найти:").pack(pady=5)
        find_entry = tk.Entry(find_win, width=40)
        find_entry.pack()

        tk.Label(find_win, text="Заменить на:").pack(pady=5)
        replace_entry = tk.Entry(find_win, width=40)
        replace_entry.pack()

        def do_replace():
            find_text = find_entry.get()
            replace_text = replace_entry.get()
            content = self.text_widget.get("1.0", tk.END)
            new_content = content.replace(find_text, replace_text)
            self.text_widget.delete("1.0", tk.END)
            self.text_widget.insert("1.0", new_content)
            find_win.destroy()

        tk.Button(find_win, text="Заменить всё", command=do_replace).pack(pady=10)

    def set_theme(self, theme):
        if theme == "dark":
            self.root.configure(bg="#1e1e2e")
            self.text_widget.configure(bg="#2a2a3a", fg="white", insertbackground="white")
            self.status.configure(bg="#1e1e2e", fg="#888")
        else:
            self.root.configure(bg="#f0f0f0")
            self.text_widget.configure(bg="white", fg="black", insertbackground="black")
            self.status.configure(bg="#f0f0f0", fg="black")

    def on_closing(self):
        if messagebox.askyesno("Выход", "Сохранить перед выходом?"):
            self.save_file()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MiniWord(root)
    root.mainloop()
