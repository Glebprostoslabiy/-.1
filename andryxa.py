import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import datetime
import json
import os
import zipfile
from tkinter import scrolledtext

# -------------------- Конфигурация --------------------
FILENAME_NOTES = "notes.json"
FILENAME_SETTINGS = "settings.json"
BACKUP_DIR = "backups"


# -------------------- Тема оформления --------------------
class ThemeManager:
    """Управление темами оформления - 12 уникальных тем"""
    themes = {
        "🌙 Темная элегантность": {
            "bg": "#0A0A0A", "fg": "#FFFFFF", "accent": "#6C63FF",
            "secondary": "#1F1F1F", "hover": "#2A2A2A", "button": "#2A2A2A",
            "button_text": "#FFFFFF", "entry": "#1F1F1F", "select": "#6C63FF"
        },
        "🖤 Черный минимализм": {
            "bg": "#000000", "fg": "#FFFFFF", "accent": "#888888",
            "secondary": "#111111", "hover": "#222222", "button": "#111111",
            "button_text": "#FFFFFF", "entry": "#111111", "select": "#888888"
        },
        "💜 Фиолетовая магия": {
            "bg": "#1A0B2E", "fg": "#E9D5FF", "accent": "#C084FC",
            "secondary": "#2D1B4A", "hover": "#3D2B5A", "button": "#2D1B4A",
            "button_text": "#E9D5FF", "entry": "#2D1B4A", "select": "#C084FC"
        },
        "💙 Океанская глубина": {
            "bg": "#0A1929", "fg": "#E0E0E0", "accent": "#00B4FF",
            "secondary": "#132F4C", "hover": "#1E3A5F", "button": "#132F4C",
            "button_text": "#FFFFFF", "entry": "#132F4C", "select": "#00B4FF"
        },
        "💚 Изумрудный лес": {
            "bg": "#0A2F2A", "fg": "#D0F0E8", "accent": "#2DD4BF",
            "secondary": "#1E4A40", "hover": "#2E6A5A", "button": "#1E4A40",
            "button_text": "#D0F0E8", "entry": "#1E4A40", "select": "#2DD4BF"
        },
        "🤍 Белая чистота": {
            "bg": "#FFFFFF", "fg": "#1A1A1A", "accent": "#6C63FF",
            "secondary": "#F5F5F5", "hover": "#E8E8E8", "button": "#F0F0F0",
            "button_text": "#1A1A1A", "entry": "#FFFFFF", "select": "#6C63FF"
        },
        "☀️ Светлая свежесть": {
            "bg": "#F8F9FA", "fg": "#212529", "accent": "#4361EE",
            "secondary": "#E9ECEF", "hover": "#DEE2E6", "button": "#E9ECEF",
            "button_text": "#212529", "entry": "#FFFFFF", "select": "#4361EE"
        },
        "🌸 Розовая мечта": {
            "bg": "#FFE4E8", "fg": "#5D3A3A", "accent": "#FF6B9D",
            "secondary": "#FFD0D8", "hover": "#FFC0CB", "button": "#FFD0D8",
            "button_text": "#5D3A3A", "entry": "#FFF0F2", "select": "#FF6B9D"
        },
        "🍊 Оранжевый закат": {
            "bg": "#FFF3E0", "fg": "#4A2A00", "accent": "#FF9800",
            "secondary": "#FFE0B2", "hover": "#FFCC80", "button": "#FFE0B2",
            "button_text": "#4A2A00", "entry": "#FFFFFF", "select": "#FF9800"
        },
        "🌿 Мятная свежесть": {
            "bg": "#E8F5E9", "fg": "#1B5E20", "accent": "#4CAF50",
            "secondary": "#C8E6C9", "hover": "#A5D6A7", "button": "#C8E6C9",
            "button_text": "#1B5E20", "entry": "#FFFFFF", "select": "#4CAF50"
        },
        "🎨 Акварель": {
            "bg": "#E8EAF6", "fg": "#1A237E", "accent": "#7986CB",
            "secondary": "#C5CAE9", "hover": "#9FA8DA", "button": "#C5CAE9",
            "button_text": "#1A237E", "entry": "#FFFFFF", "select": "#7986CB"
        },
        "🔥 Красное пламя": {
            "bg": "#FFEBEE", "fg": "#B71C1C", "accent": "#F44336",
            "secondary": "#FFCDD2", "hover": "#EF9A9A", "button": "#FFCDD2",
            "button_text": "#B71C1C", "entry": "#FFFFFF", "select": "#F44336"
        }
    }

    current_theme = "🌙 Темная элегантность"

    @classmethod
    def get_colors(cls):
        return cls.themes.get(cls.current_theme, cls.themes["🌙 Темная элегантность"])

    @classmethod
    def apply_theme_to_widget(cls, widget):
        colors = cls.get_colors()
        try:
            widget_type = type(widget).__name__
            if widget_type in ["Frame", "LabelFrame", "Toplevel"]:
                widget.configure(bg=colors["bg"])
            elif widget_type == "Label":
                widget.configure(bg=colors["bg"], fg=colors["fg"])
            elif widget_type == "Button":
                widget.configure(bg=colors["button"], fg=colors["button_text"],
                                 activebackground=colors["hover"], relief=tk.FLAT, cursor="hand2")
            elif widget_type in ["Entry", "Text"]:
                widget.configure(bg=colors["entry"], fg=colors["fg"],
                                 insertbackground=colors["accent"], relief=tk.FLAT)
            elif widget_type == "Listbox":
                widget.configure(bg=colors["entry"], fg=colors["fg"],
                                 selectbackground=colors["select"], relief=tk.FLAT)
            for child in widget.winfo_children():
                cls.apply_theme_to_widget(child)
        except:
            pass


# -------------------- Работа с данными --------------------
class DataManager:
    @staticmethod
    def load_notes():
        try:
            with open(FILENAME_NOTES, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return [{
                "id": 1, "title": "Добро пожаловать! 🎉",
                "content": "# Добро пожаловать!\n\nЭто современный блокнот с поддержкой **Markdown**.\n\n## Возможности:\n- *Курсив*\n- **Жирный текст**\n- `Код`\n- [Ссылки](https://example.com)\n\nНаслаждайтесь использованием! ✨",
                "created": datetime.datetime.now().isoformat(),
                "reminder": None, "pinned": False
            }]

    @staticmethod
    def save_notes(notes):
        with open(FILENAME_NOTES, "w", encoding="utf-8") as f:
            json.dump(notes, f, ensure_ascii=False, indent=2)

    @staticmethod
    def load_settings():
        try:
            with open(FILENAME_SETTINGS, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {"theme": "🌙 Темная элегантность", "font_size": 11, "auto_save": True}

    @staticmethod
    def save_settings(settings):
        with open(FILENAME_SETTINGS, "w", encoding="utf-8") as f:
            json.dump(settings, f)


# -------------------- Экспорт/Импорт --------------------
class ExportImportManager:
    @staticmethod
    def export_note_to_md(note, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# {note['title']}\n\n")
            f.write(f"*Создано: {note['created']}*\n\n")
            f.write(f"---\n\n")
            f.write(note['content'])
        return True

    @staticmethod
    def export_all_notes_to_zip(notes, filename):
        with zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            json_data = json.dumps(notes, ensure_ascii=False, indent=2)
            zipf.writestr("backup_notes.json", json_data)
            for note in notes:
                safe_title = "".join(c for c in note['title'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
                md_content = f"# {note['title']}\n\n*Создано: {note['created']}*\n\n---\n\n{note['content']}"
                zipf.writestr(f"{safe_title}.md", md_content)
        return True

    @staticmethod
    def import_from_md(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        lines = content.split('\n')
        title = "Импортированная заметка"
        body = content
        if lines and lines[0].startswith('# '):
            title = lines[0].replace('# ', '').strip()
            for i, line in enumerate(lines):
                if line == '---':
                    body = '\n'.join(lines[i + 1:])
                    break
        return {
            "id": None, "title": title, "content": body.strip(),
            "created": datetime.datetime.now().isoformat(),
            "reminder": None, "pinned": False
        }

    @staticmethod
    def import_from_json(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def create_backup():
        if not os.path.exists(BACKUP_DIR):
            os.makedirs(BACKUP_DIR)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(BACKUP_DIR, f"backup_{timestamp}.zip")
        with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            if os.path.exists(FILENAME_NOTES):
                zipf.write(FILENAME_NOTES, "notes.json")
            if os.path.exists(FILENAME_SETTINGS):
                zipf.write(FILENAME_SETTINGS, "settings.json")
        return backup_file

    @staticmethod
    def restore_from_backup(backup_file):
        with zipfile.ZipFile(backup_file, 'r') as zipf:
            zipf.extractall(".")
        return True


# -------------------- Анимация запуска --------------------
class SplashAnimation:
    def __init__(self, root, callback):
        self.root = root
        self.callback = callback
        self.splash = tk.Toplevel(root)
        self.splash.overrideredirect(True)

        width = self.splash.winfo_screenwidth()
        height = self.splash.winfo_screenheight()
        self.splash.geometry(f"{width}x{height}+0+0")

        self.canvas = tk.Canvas(self.splash, highlightthickness=0, bg="#0A0A0A")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Градиентный фон
        for i in range(height):
            r = int(10 + (i / height) * 50)
            g = int(10 + (i / height) * 20)
            b = int(50 + (i / height) * 150)
            self.canvas.create_line(0, i, width, i, fill=f"#{r:02x}{g:02x}{b:02x}", width=1)

        # Логотип
        self.canvas.create_text(width // 2, height // 2 - 50, text="📝", font=("Segoe UI", 100), fill="#6C63FF")
        self.canvas.create_text(width // 2, height // 2 + 20, text="Заметки", font=("Segoe UI", 48, "bold"),
                                fill="white")
        self.canvas.create_text(width // 2, height // 2 + 80, text="Ваш личный блокнот", font=("Segoe UI", 16),
                                fill="#AAAAAA")

        self.fade_in()

    def fade_in(self):
        alpha = 0.0

        def increase():
            nonlocal alpha
            if alpha < 1.0:
                alpha += 0.05
                try:
                    self.splash.attributes("-alpha", alpha)
                except:
                    pass
                self.splash.after(50, increase)
            else:
                self.splash.after(2000, self.fade_out)

        increase()

    def fade_out(self):
        alpha = 1.0

        def decrease():
            nonlocal alpha
            if alpha > 0:
                alpha -= 0.05
                try:
                    self.splash.attributes("-alpha", alpha)
                except:
                    pass
                self.splash.after(50, decrease)
            else:
                self.splash.destroy()
                self.callback()

        decrease()


# -------------------- Главное приложение --------------------
class NotesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Заметки - Ваш личный блокнот")
        self.root.geometry("1400x800")
        self.root.minsize(1000, 600)

        self.settings = DataManager.load_settings()
        self.notes = DataManager.load_notes()
        self.current_note = None
        self.current_filter = ""
        self.auto_save = self.settings.get("auto_save", True)

        ThemeManager.current_theme = self.settings.get("theme", "🌙 Темная элегантность")

        self.create_ui()
        self.apply_theme()

        if self.notes:
            self.notes.sort(key=lambda x: (not x.get("pinned", False), x["title"].lower()))
            self.load_note(self.notes[0])

        self.check_reminders()
        if self.auto_save:
            self.start_auto_save()

    def create_ui(self):
        main_container = tk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.create_top_bar(main_container)

        content_frame = tk.Frame(main_container)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=15)

        self.create_sidebar(content_frame)
        self.create_editor(content_frame)
        self.create_status_bar()

    def create_top_bar(self, parent):
        top_frame = tk.Frame(parent, height=60)
        top_frame.pack(fill=tk.X)
        top_frame.pack_propagate(False)

        title_frame = tk.Frame(top_frame)
        title_frame.pack(side=tk.LEFT)
        tk.Label(title_frame, text="📝", font=("Segoe UI", 28)).pack(side=tk.LEFT)
        tk.Label(title_frame, text="Заметки", font=("Segoe UI", 24, "bold")).pack(side=tk.LEFT, padx=5)

        # Поиск
        search_frame = tk.Frame(top_frame)
        search_frame.pack(side=tk.LEFT, padx=40)
        self.search_var = tk.StringVar()
        self.search_var.trace_add('write', lambda *args: self.search_notes())

        tk.Label(search_frame, text="🔍", font=("Segoe UI", 14)).pack(side=tk.LEFT)
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=("Segoe UI", 11), width=35)
        self.search_entry.pack(side=tk.LEFT, padx=8)
        self.search_entry.insert(0, "Поиск заметок...")
        self.search_entry.bind("<FocusIn>", lambda e: self.search_entry.delete(0,
                                                                               tk.END) if self.search_entry.get() == "Поиск заметок..." else None)
        self.search_entry.bind("<FocusOut>", lambda e: self.search_entry.insert(0,
                                                                                "Поиск заметок...") if not self.search_entry.get() else None)

        # Кнопки - сохраняем ссылки для меню
        btn_frame = tk.Frame(top_frame)
        btn_frame.pack(side=tk.RIGHT)

        self.btn_export = self.create_button(btn_frame, "📤 Экспорт", self.show_export_menu)
        self.btn_export.pack(side=tk.LEFT, padx=5)

        self.btn_import = self.create_button(btn_frame, "📥 Импорт", self.show_import_menu)
        self.btn_import.pack(side=tk.LEFT, padx=5)

        self.btn_backup = self.create_button(btn_frame, "💾 Резервное копирование", self.show_backup_menu)
        self.btn_backup.pack(side=tk.LEFT, padx=5)

        self.btn_new = self.create_button(btn_frame, "➕ Создать", self.new_note)
        self.btn_new.pack(side=tk.LEFT, padx=5)

        self.btn_settings = self.create_button(btn_frame, "⚙️ Настройки", self.open_settings)
        self.btn_settings.pack(side=tk.LEFT, padx=5)

    def create_button(self, parent, text, command):
        return tk.Button(parent, text=text, command=command, font=("Segoe UI", 10, "bold"), padx=15, pady=8,
                         relief=tk.FLAT, cursor="hand2")

    def create_sidebar(self, parent):
        sidebar = tk.Frame(parent, width=350)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        sidebar.pack_propagate(False)

        header = tk.Frame(sidebar)
        header.pack(fill=tk.X, pady=(0, 15))
        tk.Label(header, text="Все заметки", font=("Segoe UI", 14, "bold")).pack(side=tk.LEFT)
        self.counter_label = tk.Label(header, text=f"{len(self.notes)}", font=("Segoe UI", 12))
        self.counter_label.pack(side=tk.RIGHT)

        list_frame = tk.Frame(sidebar)
        list_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(list_frame, width=8)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.notes_listbox = tk.Listbox(list_frame, font=("Segoe UI", 11), yscrollcommand=scrollbar.set,
                                        selectmode=tk.SINGLE, relief=tk.FLAT, bd=0, highlightthickness=0)
        self.notes_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.notes_listbox.yview)

        self.notes_listbox.bind("<<ListboxSelect>>", self.on_note_select)
        self.notes_listbox.bind("<Button-3>", lambda e: self.show_context_menu(e))

        btn_panel = tk.Frame(sidebar)
        btn_panel.pack(fill=tk.X, pady=10)
        self.create_button(btn_panel, "📌 Закрепить", self.toggle_pin).pack(side=tk.LEFT, padx=2)
        self.create_button(btn_panel, "🗑️ Удалить", self.delete_note).pack(side=tk.LEFT, padx=2)
        self.create_button(btn_panel, "⏰ Напомнить", self.set_reminder).pack(side=tk.LEFT, padx=2)

    def create_editor(self, parent):
        editor = tk.Frame(parent)
        editor.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        toolbar = tk.Frame(editor, height=45)
        toolbar.pack(fill=tk.X, pady=(0, 10))
        toolbar.pack_propagate(False)

        format_group = tk.Frame(toolbar)
        format_group.pack(side=tk.LEFT)

        tools = [("B", "bold", "Жирный (Ctrl+B)"), ("I", "italic", "Курсив (Ctrl+I)"), ("`", "code", "Код"),
                 ("#", "header", "Заголовок"), ("🔗", "link", "Ссылка")]
        for text, cmd, tooltip in tools:
            btn = self.create_button(format_group, text, lambda c=cmd: self.format_text(c))
            btn.pack(side=tk.LEFT, padx=2)
            btn.bind("<Enter>", lambda e, t=tooltip: self.show_tooltip(e, t))
            btn.bind("<Leave>", self.hide_tooltip)

        self.create_button(toolbar, "💾 Сохранить (Ctrl+S)", self.save_current_note).pack(side=tk.RIGHT, padx=5)

        title_frame = tk.Frame(editor)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        tk.Label(title_frame, text="Заголовок:", font=("Segoe UI", 11, "bold")).pack(side=tk.LEFT)
        self.title_entry = tk.Entry(title_frame, font=("Segoe UI", 16, "bold"), relief=tk.FLAT, bd=1)
        self.title_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        editor_frame = tk.Frame(editor)
        editor_frame.pack(fill=tk.BOTH, expand=True)

        self.text_editor = scrolledtext.ScrolledText(editor_frame, wrap=tk.WORD,
                                                     font=("Consolas", self.settings.get("font_size", 11)), padx=15,
                                                     pady=15, undo=True, relief=tk.FLAT, bd=1)
        self.text_editor.pack(fill=tk.BOTH, expand=True)

        preview_frame = tk.Frame(editor)
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        preview_header = tk.Frame(preview_frame)
        preview_header.pack(fill=tk.X)
        tk.Label(preview_header, text="📖 Предпросмотр", font=("Segoe UI", 11, "bold")).pack(side=tk.LEFT)

        self.preview_text = scrolledtext.ScrolledText(preview_frame, wrap=tk.WORD, font=("Segoe UI", 10), height=8,
                                                      relief=tk.FLAT, bd=1)
        self.preview_text.pack(fill=tk.BOTH, expand=True)

        self.text_editor.bind("<KeyRelease>", self.update_preview)
        self.root.bind("<Control-b>", lambda e: self.format_text("bold"))
        self.root.bind("<Control-i>", lambda e: self.format_text("italic"))
        self.root.bind("<Control-s>", lambda e: self.save_current_note())

    def format_text(self, command):
        try:
            if not self.text_editor.tag_ranges("sel"):
                messagebox.showinfo("Форматирование", "Выделите текст для форматирования")
                return
            start = self.text_editor.index("sel.first")
            end = self.text_editor.index("sel.last")
            selected = self.text_editor.get(start, end)

            if command == "bold":
                formatted = f"**{selected}**"
            elif command == "italic":
                formatted = f"*{selected}*"
            elif command == "code":
                formatted = f"`{selected}`"
            elif command == "header":
                formatted = f"# {selected}"
            elif command == "link":
                url = simpledialog.askstring("Ссылка", "Введите URL:", parent=self.root)
                if not url: return
                formatted = f"[{selected}]({url})"
            else:
                return

            self.text_editor.delete(start, end)
            self.text_editor.insert(start, formatted)
            self.update_preview()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось отформатировать: {str(e)}")

    def show_tooltip(self, event, text):
        self.tooltip = tk.Toplevel()
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
        tk.Label(self.tooltip, text=text, background="#FFFFE0", relief=tk.SOLID, borderwidth=1, padx=8, pady=4,
                 font=("Segoe UI", 9)).pack()
        self.tooltip.after(2000, self.tooltip.destroy)

    def hide_tooltip(self, event):
        if hasattr(self, 'tooltip'):
            try:
                self.tooltip.destroy()
            except:
                pass

    def update_listbox(self):
        if not hasattr(self, 'notes_listbox'):
            return
        self.notes_listbox.delete(0, tk.END)
        filtered_notes = [n for n in self.notes if not self.current_filter or self.current_filter.lower() in n[
            "title"].lower() or self.current_filter.lower() in n["content"].lower()]
        filtered_notes.sort(key=lambda x: (not x.get("pinned", False), x["title"].lower()))

        for note in filtered_notes:
            prefix = "📌 " if note.get("pinned", False) else "📄 "
            if note.get("reminder"): prefix = "⏰ " + prefix
            self.notes_listbox.insert(tk.END, f"{prefix}{note['title'][:45]}")
        if hasattr(self, 'counter_label'):
            self.counter_label.config(text=f"{len(filtered_notes)}")
        self.update_status()

    def update_status(self):
        if hasattr(self, 'status_label') and hasattr(self, 'notes_listbox'):
            visible_count = len(self.notes_listbox.get(0, tk.END))
            self.status_label.config(text=f"📊 Всего заметок: {len(self.notes)} | Показано: {visible_count}")

    def search_notes(self):
        self.current_filter = self.search_entry.get()
        if self.current_filter == "Поиск заметок...": self.current_filter = ""
        self.update_listbox()

    def on_note_select(self, event):
        selection = self.notes_listbox.curselection()
        if selection:
            filtered_notes = [n for n in self.notes if not self.current_filter or self.current_filter.lower() in n[
                "title"].lower() or self.current_filter.lower() in n["content"].lower()]
            filtered_notes.sort(key=lambda x: (not x.get("pinned", False), x["title"].lower()))
            if selection[0] < len(filtered_notes):
                for note in self.notes:
                    if note["id"] == filtered_notes[selection[0]]["id"]:
                        self.load_note(note);
                        break

    def load_note(self, note):
        self.current_note = note
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, note["title"])
        self.text_editor.delete("1.0", tk.END)
        self.text_editor.insert("1.0", note["content"])
        self.update_preview()

    def save_current_note(self):
        if self.current_note:
            self.current_note["title"] = self.title_entry.get().strip() or "Без названия"
            self.current_note["content"] = self.text_editor.get("1.0", tk.END).strip()
            DataManager.save_notes(self.notes)
            self.update_listbox()
            self.status_label.config(text="✓ Заметка сохранена", fg="green")
            self.root.after(2000, lambda: self.status_label.config(fg=ThemeManager.get_colors()["fg"]))

    def new_note(self):
        new_id = max([n["id"] for n in self.notes], default=0) + 1
        new_note = {"id": new_id, "title": "Новая заметка",
                    "content": "# Новая заметка\n\nВведите текст здесь...\n\n**Жирный текст**\n*Курсив*\n`Код`",
                    "created": datetime.datetime.now().isoformat(), "reminder": None, "pinned": False}
        self.notes.append(new_note)
        DataManager.save_notes(self.notes)
        self.update_listbox()
        self.load_note(new_note)
        self.status_label.config(text="✓ Новая заметка создана", fg="green")
        self.root.after(2000, lambda: self.status_label.config(fg=ThemeManager.get_colors()["fg"]))

    def delete_note(self):
        if self.current_note and messagebox.askyesno("Удаление", "Удалить эту заметку?"):
            self.notes = [n for n in self.notes if n["id"] != self.current_note["id"]]
            DataManager.save_notes(self.notes)
            self.update_listbox()
            if self.notes:
                self.load_note(self.notes[0])
            else:
                self.new_note()

    def toggle_pin(self):
        if self.current_note:
            self.current_note["pinned"] = not self.current_note.get("pinned", False)
            DataManager.save_notes(self.notes)
            self.update_listbox()

    def set_reminder(self):
        if not self.current_note:
            messagebox.showwarning("Предупреждение", "Сначала выберите заметку")
            return
        dialog = tk.Toplevel(self.root)
        dialog.title("⏰ Напоминание")
        dialog.geometry("400x350")
        dialog.transient(self.root)
        dialog.grab_set()
        colors = ThemeManager.get_colors()
        dialog.configure(bg=colors["bg"])

        tk.Label(dialog, text="Установить напоминание", font=("Segoe UI", 16, "bold"), bg=colors["bg"],
                 fg=colors["fg"]).pack(pady=20)

        date_frame = tk.Frame(dialog, bg=colors["bg"])
        date_frame.pack(pady=10)
        tk.Label(date_frame, text="📅 Дата (ГГГГ-ММ-ДД):", font=("Segoe UI", 11), bg=colors["bg"],
                 fg=colors["fg"]).pack(side=tk.LEFT, padx=5)
        date_entry = tk.Entry(date_frame, font=("Segoe UI", 11), width=20)
        date_entry.pack(side=tk.LEFT, padx=5)

        time_frame = tk.Frame(dialog, bg=colors["bg"])
        time_frame.pack(pady=10)
        tk.Label(time_frame, text="⏰ Время (ЧЧ:ММ):", font=("Segoe UI", 11), bg=colors["bg"], fg=colors["fg"]).pack(
            side=tk.LEFT, padx=5)
        time_entry = tk.Entry(time_frame, font=("Segoe UI", 11), width=20)
        time_entry.pack(side=tk.LEFT, padx=5)

        if self.current_note.get("reminder"):
            try:
                dt = datetime.datetime.fromisoformat(self.current_note["reminder"])
                date_entry.insert(0, dt.strftime("%Y-%m-%d"))
                time_entry.insert(0, dt.strftime("%H:%M"))
            except:
                pass

        def save():
            if date_entry.get() and time_entry.get():
                try:
                    dt = datetime.datetime.strptime(f"{date_entry.get()} {time_entry.get()}", "%Y-%m-%d %H:%M")
                    self.current_note["reminder"] = dt.isoformat()
                    DataManager.save_notes(self.notes)
                    self.update_listbox()
                    dialog.destroy()
                    self.status_label.config(text="✓ Напоминание установлено", fg="green")
                except:
                    messagebox.showerror("Ошибка", "Неверный формат\nИспользуйте: ГГГГ-ММ-ДД ЧЧ:ММ")

        def remove():
            self.current_note["reminder"] = None
            DataManager.save_notes(self.notes)
            self.update_listbox()
            dialog.destroy()
            self.status_label.config(text="✓ Напоминание удалено", fg="green")

        btn_frame = tk.Frame(dialog, bg=colors["bg"])
        btn_frame.pack(pady=25)
        tk.Button(btn_frame, text="Сохранить", command=save, bg=colors["accent"], fg="white", padx=25, pady=8,
                  cursor="hand2", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=5)
        if self.current_note.get("reminder"):
            tk.Button(btn_frame, text="Удалить", command=remove, bg=colors["button"], fg=colors["button_text"], padx=25,
                      pady=8, cursor="hand2", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Отмена", command=dialog.destroy, bg=colors["button"], fg=colors["button_text"],
                  padx=25, pady=8, cursor="hand2", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=5)

    def show_context_menu(self, event):
        selection = self.notes_listbox.curselection()
        if selection:
            menu = tk.Menu(self.root, tearoff=0)
            menu.add_command(label="📌 Закрепить", command=self.toggle_pin)
            menu.add_command(label="⏰ Напоминание", command=self.set_reminder)
            menu.add_separator()
            menu.add_command(label="🗑️ Удалить", command=self.delete_note)
            menu.post(event.x_root, event.y_root)

    def update_preview(self, event=None):
        try:
            text = self.text_editor.get("1.0", tk.END)
            self.preview_text.delete("1.0", tk.END)
            for line in text.split('\n'):
                if line.startswith('# '):
                    line = f"📌 {line[2:]}\n{'-' * 40}"
                elif line.startswith('## '):
                    line = f"  📌 {line[3:]}\n{'-' * 30}"
                elif '**' in line:
                    line = line.replace('**', '')
                elif '*' in line and not line.startswith('*'):
                    line = line.replace('*', '')
                elif line.startswith('- '):
                    line = f"  • {line[2:]}"
                elif line.startswith('1. '):
                    line = f"  1. {line[3:]}"
                elif '`' in line:
                    line = line.replace('`', '"')
                self.preview_text.insert(tk.END, line + '\n')
        except:
            pass

    def create_status_bar(self):
        self.status_bar = tk.Frame(self.root)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_label = tk.Label(self.status_bar, text="Готов к работе", font=("Segoe UI", 9), padx=10, pady=5)
        self.status_label.pack(side=tk.LEFT)
        self.cursor_label = tk.Label(self.status_bar, text="", font=("Segoe UI", 9), padx=10, pady=5)
        self.cursor_label.pack(side=tk.RIGHT)
        self.text_editor.bind("<KeyRelease>", self.update_cursor_pos)
        self.text_editor.bind("<ButtonRelease>", self.update_cursor_pos)

    def update_cursor_pos(self, event=None):
        try:
            pos = self.text_editor.index(tk.INSERT)
            self.cursor_label.config(text=f"Строка: {pos.split('.')[0]}, Колонка: {pos.split('.')[1]}")
        except:
            pass

    def show_export_menu(self):
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="📄 Экспорт текущей заметки в .md", command=self.export_current_note_md)
        menu.add_separator()
        menu.add_command(label="📦 Экспорт всех заметок в ZIP (.md)", command=self.export_all_notes_zip)
        menu.post(self.btn_export.winfo_rootx(), self.btn_export.winfo_rooty() + 40)

    def show_import_menu(self):
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="📄 Импорт из .md файла", command=self.import_from_md)
        menu.add_command(label="📦 Импорт из JSON", command=self.import_from_json)
        menu.post(self.btn_import.winfo_rootx(), self.btn_import.winfo_rooty() + 40)

    def show_backup_menu(self):
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="💾 Создать резервную копию", command=self.create_backup)
        menu.add_command(label="🔄 Восстановить из резервной копии", command=self.restore_backup)
        menu.post(self.btn_backup.winfo_rootx(), self.btn_backup.winfo_rooty() + 40)

    def export_current_note_md(self):
        if not self.current_note:
            messagebox.showwarning("Предупреждение", "Нет выбранной заметки")
            return
        filename = filedialog.asksaveasfilename(defaultextension=".md", filetypes=[("Markdown files", "*.md")])
        if filename:
            ExportImportManager.export_note_to_md(self.current_note, filename)
            messagebox.showinfo("Успех", "Заметка экспортирована в .md формат")

    def export_all_notes_zip(self):
        filename = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=[("ZIP files", "*.zip")])
        if filename:
            ExportImportManager.export_all_notes_to_zip(self.notes, filename)
            messagebox.showinfo("Успех", f"Экспортировано {len(self.notes)} заметок в ZIP архив")

    def import_from_md(self):
        filename = filedialog.askopenfilename(filetypes=[("Markdown files", "*.md")])
        if filename:
            try:
                imported_note = ExportImportManager.import_from_md(filename)
                max_id = max([n["id"] for n in self.notes], default=0) + 1
                imported_note["id"] = max_id
                self.notes.append(imported_note)
                DataManager.save_notes(self.notes)
                self.update_listbox()
                messagebox.showinfo("Успех", "Заметка импортирована из .md файла")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка импорта: {str(e)}")

    def import_from_json(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filename:
            try:
                imported = ExportImportManager.import_from_json(filename)
                if isinstance(imported, list):
                    max_id = max([n["id"] for n in self.notes], default=0)
                    for note in imported:
                        max_id += 1
                        note["id"] = max_id
                        note["created"] = datetime.datetime.now().isoformat()
                        if "reminder" not in note: note["reminder"] = None
                        if "pinned" not in note: note["pinned"] = False
                        self.notes.append(note)
                    DataManager.save_notes(self.notes)
                    self.update_listbox()
                    messagebox.showinfo("Успех", f"Импортировано {len(imported)} заметок")
                else:
                    messagebox.showerror("Ошибка", "Неверный формат JSON файла")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка импорта: {str(e)}")

    def create_backup(self):
        try:
            backup_file = ExportImportManager.create_backup()
            messagebox.showinfo("Успех", f"Резервная копия создана:\n{backup_file}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка создания резервной копии: {str(e)}")

    def restore_backup(self):
        filename = filedialog.askopenfilename(filetypes=[("ZIP files", "*.zip")])
        if filename:
            try:
                ExportImportManager.restore_from_backup(filename)
                self.notes = DataManager.load_notes()
                self.settings = DataManager.load_settings()
                self.update_listbox()
                if self.notes: self.load_note(self.notes[0])
                messagebox.showinfo("Успех", "Восстановление выполнено успешно")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка восстановления: {str(e)}")

    def open_settings(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Настройки")
        dialog.geometry("550x550")
        dialog.transient(self.root)
        dialog.grab_set()
        colors = ThemeManager.get_colors()
        dialog.configure(bg=colors["bg"])

        tk.Label(dialog, text="Настройки", font=("Segoe UI", 18, "bold"), bg=colors["bg"], fg=colors["fg"]).pack(
            pady=20)

        theme_frame = tk.LabelFrame(dialog, text="Оформление (12 тем)", font=("Segoe UI", 12, "bold"), bg=colors["bg"],
                                    fg=colors["fg"])
        theme_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(theme_frame, text="Выберите тему:", bg=colors["bg"], fg=colors["fg"]).pack(pady=5)
        theme_var = tk.StringVar(value=ThemeManager.current_theme)
        theme_combo = ttk.Combobox(theme_frame, textvariable=theme_var, values=list(ThemeManager.themes.keys()),
                                   state="readonly", width=35, height=20)
        theme_combo.pack(pady=5)

        # Предпросмотр темы
        preview_frame = tk.Frame(theme_frame, bg=colors["bg"], height=100)
        preview_frame.pack(fill=tk.X, pady=10)
        preview_frame.pack_propagate(False)

        def update_preview(*args):
            for widget in preview_frame.winfo_children():
                widget.destroy()
            theme_name = theme_var.get()
            if theme_name in ThemeManager.themes:
                theme_colors = ThemeManager.themes[theme_name]
                colors_list = [
                    ("Фон", theme_colors["bg"]),
                    ("Текст", theme_colors["fg"]),
                    ("Акцент", theme_colors["accent"]),
                    ("Кнопки", theme_colors["button"])
                ]
                for name, color in colors_list:
                    color_frame = tk.Frame(preview_frame, bg=theme_colors["bg"])
                    color_frame.pack(fill=tk.X, pady=2)
                    tk.Label(color_frame, text=f"{name}:", bg=theme_colors["bg"], fg=theme_colors["fg"], width=10,
                             anchor=tk.W).pack(side=tk.LEFT)
                    color_box = tk.Frame(color_frame, bg=color, width=80, height=20, relief=tk.SUNKEN, bd=1)
                    color_box.pack(side=tk.LEFT, padx=10)
                    tk.Label(color_frame, text=color, bg=theme_colors["bg"], fg=theme_colors["fg"],
                             font=("Segoe UI", 8)).pack(side=tk.LEFT)

        theme_var.trace('w', update_preview)
        update_preview()

        font_frame = tk.LabelFrame(dialog, text="Редактор", font=("Segoe UI", 12, "bold"), bg=colors["bg"],
                                   fg=colors["fg"])
        font_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(font_frame, text="Размер шрифта:", bg=colors["bg"], fg=colors["fg"]).pack(pady=5)
        font_size = tk.Scale(font_frame, from_=8, to=20, orient=tk.HORIZONTAL, length=250, bg=colors["bg"],
                             fg=colors["fg"], troughcolor=colors["secondary"])
        font_size.set(self.settings.get("font_size", 11))
        font_size.pack(pady=5)

        auto_save_var = tk.BooleanVar(value=self.settings.get("auto_save", True))
        tk.Checkbutton(font_frame, text="Автосохранение (каждые 30 секунд)", variable=auto_save_var, bg=colors["bg"],
                       fg=colors["fg"], selectcolor=colors["bg"]).pack(pady=5)

        def apply_settings():
            ThemeManager.current_theme = theme_var.get()
            self.settings["theme"] = ThemeManager.current_theme
            self.settings["font_size"] = int(font_size.get())
            self.settings["auto_save"] = auto_save_var.get()
            DataManager.save_settings(self.settings)
            self.apply_theme()
            self.text_editor.configure(font=("Consolas", self.settings["font_size"]))
            self.auto_save = self.settings["auto_save"]
            dialog.destroy()
            self.status_label.config(text="✓ Настройки сохранены", fg="green")
            self.root.after(2000, lambda: self.status_label.config(fg=ThemeManager.get_colors()["fg"]))

        btn_frame = tk.Frame(dialog, bg=colors["bg"])
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="Применить", command=apply_settings, bg=colors["accent"], fg="white", padx=30,
                  pady=10, cursor="hand2", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Отмена", command=dialog.destroy, bg=colors["button"], fg=colors["button_text"],
                  padx=30, pady=10, cursor="hand2", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=10)

    def apply_theme(self):
        ThemeManager.apply_theme_to_widget(self.root)
        colors = ThemeManager.get_colors()
        if hasattr(self, 'status_bar'):
            self.status_bar.configure(bg=colors["bg"])
            self.status_label.configure(bg=colors["bg"], fg=colors["fg"])
            self.cursor_label.configure(bg=colors["bg"], fg=colors["fg"])
        self.update_preview()

    def check_reminders(self):
        try:
            now = datetime.datetime.now()
            for note in self.notes:
                if note.get("reminder"):
                    remind_time = datetime.datetime.fromisoformat(note["reminder"])
                    if remind_time <= now:
                        result = messagebox.askyesno("Напоминание",
                                                     f"📌 {note['title']}\n\n{note['content'][:150]}\n\nОткрыть заметку?")
                        if result: self.load_note(note)
                        note["reminder"] = None
                        DataManager.save_notes(self.notes)
                        self.update_listbox()
        except:
            pass
        self.root.after(60000, self.check_reminders)

    def start_auto_save(self):
        def auto_save():
            if self.auto_save and self.current_note:
                self.save_current_note()
            self.root.after(30000, auto_save)

        self.root.after(30000, auto_save)


# -------------------- Запуск --------------------
def main():
    root = tk.Tk()
    root.withdraw()

    def start_app():
        app = NotesApp(root)
        root.deiconify()

    splash = SplashAnimation(root, start_app)
    root.mainloop()


if __name__ == "__main__":
    main()