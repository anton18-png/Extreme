import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import os
import subprocess
import glob

class OptimizationTab:
    """Класс для вкладки оптимизации — фреймы вместо вкладок"""

    def __init__(self, parent, config):
        self.parent = parent
        self.config = config

        self.tweaks_path = r"tweaks"

        self.nvidia_path = os.path.join(self.tweaks_path, "Драйверы", "Оптимизация Nvidia")
        self.amd_path = os.path.join(self.tweaks_path, "Драйверы", "Оптимизация Amd")
        self.intel_path = os.path.join(self.tweaks_path, "Драйверы", "Оптимизация Intel")
        self.directx_path = os.path.join(self.tweaks_path, "Драйверы", "DirectX", "Оптимизация DirectX")
        self.opengl_path = os.path.join(self.tweaks_path, "Драйверы", "DirectX", "Оптимизация OpenGL")
        self.svchost_path = os.path.join(self.tweaks_path, "Драйверы", "Порог разделения svchost")
        self.win32_path = os.path.join(self.tweaks_path, "Драйверы", "Разделение приоритетов Win32")
        self.services_path = os.path.join(self.tweaks_path, "Драйверы", "Службы")

        self.nvidia_files = self.get_files_from_folder(self.nvidia_path)
        self.amd_files = self.get_files_from_folder(self.amd_path)
        self.intel_files = self.get_files_from_folder(self.intel_path)
        self.directx_files = self.get_files_from_folder(self.directx_path)
        self.opengl_files = self.get_files_from_folder(self.opengl_path)
        self.svchost_files = self.get_files_from_folder(self.svchost_path)
        self.win32_files = self.get_files_from_folder(self.win32_path)
        self.services_files = self.get_files_from_folder(self.services_path)

        self.nvidia_vars = {}
        self.amd_vars = {}
        self.intel_vars = {}
        self.directx_vars = {}
        self.opengl_vars = {}

        self.colors = {
            "bg": "#1a1e24",
            "card_bg": "#252a33",
            "card_hover": "#2f3540",
            "accent": "#4a9eff",
            "danger": "#ff5f56",
            "success": "#27c93f",
            "warning": "#ffbd2e",
            "text": "#ffffff",
            "text_secondary": "#8f9aaa",
            "nvidia_green": "#76b900",
            "amd_red": "#ed1c24",
            "intel_blue": "#0071c5"
        }

        self._columns = self.config.getint("Columns", "default", fallback=3)
        self._display_mode = self.config.get("General", "checkbox_display_mode", fallback="regular")

        self.setup_ui()

    def get_files_from_folder(self, folder_path):
        if not os.path.exists(folder_path):
            return []
        all_files = []
        for ext in ['*.bat', '*.cmd', '*.exe', '*.ps1']:
            all_files.extend(glob.glob(os.path.join(folder_path, ext)))
        return [os.path.basename(f) for f in all_files]

    def setup_ui(self):
        main = ttk.Frame(self.parent)
        main.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Верхняя панель с глобальными кнопками
        top_actions = ttk.Frame(main)
        top_actions.pack(fill=X, pady=(0, 10))

        select_all_btn = ttk.Button(
            top_actions,
            text="Выбрать все твики",
            bootstyle="primary-outline",
            command=self.select_all_tweaks,
            width=22
        )
        select_all_btn.pack(side=LEFT, padx=(0, 5))

        deselect_all_btn = ttk.Button(
            top_actions,
            text="Снять все",
            bootstyle="secondary-outline",
            command=self.deselect_all_tweaks,
            width=15
        )
        deselect_all_btn.pack(side=LEFT, padx=(0, 5))

        # Тело — скроллируемая область с фреймами (горизонтально)
        canvas = ttk.Canvas(main, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main, orient="horizontal", command=canvas.xview)
        scrollable = ttk.Frame(canvas)

        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(xscrollcommand=scrollbar.set)

        canvas.pack(side="top", fill="both", expand=True)
        scrollbar.pack(side="bottom", fill="x")

        def on_mousewheel(event):
            if event.num == 5 or event.delta == -120:
                canvas.xview_scroll(1, "units")
            elif event.num == 4 or event.delta == 120:
                canvas.xview_scroll(-1, "units")
        canvas.bind("<MouseWheel>", on_mousewheel)
        canvas.bind("<Button-4>", on_mousewheel)
        canvas.bind("<Button-5>", on_mousewheel)
        scrollable.bind("<MouseWheel>", on_mousewheel)
        scrollable.bind("<Button-4>", on_mousewheel)
        scrollable.bind("<Button-5>", on_mousewheel)

        def bind_mw(w):
            for child in w.winfo_children():
                child.bind("<MouseWheel>", on_mousewheel)
                child.bind("<Button-4>", on_mousewheel)
                child.bind("<Button-5>", on_mousewheel)
                if hasattr(child, 'winfo_children'):
                    bind_mw(child)

        # Фреймы-секции внутри scrollable (слева направо)
        self.create_vendor_frame(scrollable, "NVIDIA", self.nvidia_files, self.nvidia_vars,
                                 self.nvidia_path, self.colors["nvidia_green"])
        self.create_vendor_frame(scrollable, "AMD", self.amd_files, self.amd_vars,
                                 self.amd_path, self.colors["amd_red"])
        self.create_vendor_frame(scrollable, "Intel", self.intel_files, self.intel_vars,
                                 self.intel_path, self.colors["intel_blue"])
        self.create_vendor_frame(scrollable, "DirectX", self.directx_files, self.directx_vars,
                                 self.directx_path, self.colors["accent"])
        self.create_vendor_frame(scrollable, "OpenGL", self.opengl_files, self.opengl_vars,
                                 self.opengl_path, self.colors["warning"])

        bind_mw(scrollable)

        # Нижняя панель — выпадающие списки + кнопка Применить
        bottom_frame = ttk.Frame(main)
        bottom_frame.pack(fill=X, pady=(10, 0))

        dropdowns_frame = ttk.Frame(bottom_frame)
        dropdowns_frame.pack(side=LEFT, fill=X, expand=True)
        self.create_dropdown_row(dropdowns_frame)

        apply_btn = ttk.Button(
            bottom_frame,
            text="Применить выбранные",
            bootstyle="success-outline",
            command=self.apply_selected_tweaks,
            width=22
        )
        apply_btn.pack(side=RIGHT, padx=(10, 0))

    def create_vendor_frame(self, parent, label, files, vars_dict, folder_path, accent_color):
        frame = ttk.Labelframe(parent, text=f" {label} ", padding=10)
        frame.pack(side=LEFT, fill=Y, padx=(0, 10), anchor=N)

        section_header = ttk.Frame(frame)
        section_header.pack(fill=X, pady=(0, 5))

        select_section_var = ttk.BooleanVar(value=False)

        def on_section_select():
            val = select_section_var.get()
            for var in vars_dict.values():
                var.set(val)

        select_section_cb = ttk.Checkbutton(
            section_header,
            text="Выбрать всё",
            variable=select_section_var,
            bootstyle="primary-round-toggle",
            command=on_section_select
        )
        select_section_cb.pack(side=LEFT)

        grid_frame = ttk.Frame(frame)
        grid_frame.pack(fill=X)

        row = 0
        col = 0
        for file in sorted(files):
            display_name = file.replace(".bat", "").replace(".cmd", "").replace(".exe", "").replace(".ps1", "")
            var = ttk.BooleanVar(value=False)
            vars_dict[file] = var

            cb = ttk.Checkbutton(
                grid_frame,
                text=display_name,
                variable=var,
                style="Custom.TCheckbutton"
            )
            cb.grid(row=row, column=col, sticky=W, padx=5, pady=2)

            col += 1
            if col >= self._columns:
                col = 0
                row += 1

    def create_dropdown_row(self, parent):
        frames = []
        for i in range(3):
            frame = ttk.Frame(parent, bootstyle="secondary")
            frame.pack(side=LEFT, fill=X, expand=True, padx=(0, 5))
            frames.append(frame)

        # SvcHostSplitThreshold
        svchost_label = ttk.Label(
            frames[0],
            text="Порог разделения svchost",
            font=("Segoe UI", 9, "bold"),
            foreground=self.colors["accent"]
        )
        svchost_label.pack(anchor=W, padx=5, pady=(5, 0))

        svchost_desc = ttk.Label(
            frames[0],
            text="Set SvcHost split threshold",
            font=("Segoe UI", 7),
            foreground=self.colors["text_secondary"]
        )
        svchost_desc.pack(anchor=W, padx=5)

        self.svchost_combo = ttk.Combobox(
            frames[0],
            values=["Выберите файл..."] + sorted(self.svchost_files),
            state="readonly",
            width=25
        )
        self.svchost_combo.set("Выберите файл...")
        self.svchost_combo.pack(padx=5, pady=5, fill=X)

        # Win32 Priority Separation
        win32_label = ttk.Label(
            frames[1],
            text="Разделение приоритетов Win32",
            font=("Segoe UI", 9, "bold"),
            foreground=self.colors["accent"]
        )
        win32_label.pack(anchor=W, padx=5, pady=(5, 0))

        win32_desc = ttk.Label(
            frames[1],
            text="Set Win32 priority separation (Hex)",
            font=("Segoe UI", 7),
            foreground=self.colors["text_secondary"]
        )
        win32_desc.pack(anchor=W, padx=5)

        self.win32_combo = ttk.Combobox(
            frames[1],
            values=["Выберите файл..."] + sorted(self.win32_files),
            state="readonly",
            width=25
        )
        self.win32_combo.set("Выберите файл...")
        self.win32_combo.pack(padx=5, pady=5, fill=X)

        # Services
        services_label = ttk.Label(
            frames[2],
            text="Службы",
            font=("Segoe UI", 9, "bold"),
            foreground=self.colors["accent"]
        )
        services_label.pack(anchor=W, padx=5, pady=(5, 0))

        services_desc = ttk.Label(
            frames[2],
            text="Select service configuration",
            font=("Segoe UI", 7),
            foreground=self.colors["text_secondary"]
        )
        services_desc.pack(anchor=W, padx=5)

        self.services_combo = ttk.Combobox(
            frames[2],
            values=["Выберите файл..."] + sorted(self.services_files),
            state="readonly",
            width=25
        )
        self.services_combo.set("Выберите файл...")
        self.services_combo.pack(padx=5, pady=5, fill=X)

    def select_all_tweaks(self):
        for vars_dict in [self.nvidia_vars, self.amd_vars, self.intel_vars, self.directx_vars, self.opengl_vars]:
            for var in vars_dict.values():
                var.set(True)

    def deselect_all_tweaks(self):
        for vars_dict in [self.nvidia_vars, self.amd_vars, self.intel_vars, self.directx_vars, self.opengl_vars]:
            for var in vars_dict.values():
                var.set(False)

    def run_script(self, script_path):
        try:
            if not os.path.exists(script_path):
                return False
            if script_path.endswith('.ps1'):
                subprocess.run(['powershell.exe', '-ExecutionPolicy', 'Bypass', '-File', script_path], shell=True)
            else:
                subprocess.call(f'Utils\\launcher.exe "{script_path}"', shell=True)
            return True
        except Exception as e:
            print(f"Ошибка при запуске {script_path}: {e}")
            return False

    def apply_selected_tweaks(self):
        selected_tweaks = []

        for file, var in self.nvidia_vars.items():
            if var.get():
                selected_tweaks.append(os.path.join(self.nvidia_path, file))
        for file, var in self.amd_vars.items():
            if var.get():
                selected_tweaks.append(os.path.join(self.amd_path, file))
        for file, var in self.intel_vars.items():
            if var.get():
                selected_tweaks.append(os.path.join(self.intel_path, file))
        for file, var in self.directx_vars.items():
            if var.get():
                selected_tweaks.append(os.path.join(self.directx_path, file))
        for file, var in self.opengl_vars.items():
            if var.get():
                selected_tweaks.append(os.path.join(self.opengl_path, file))

        if hasattr(self, 'svchost_combo') and self.svchost_combo.get() != "Выберите файл...":
            selected_tweaks.append(os.path.join(self.svchost_path, self.svchost_combo.get()))
        if hasattr(self, 'win32_combo') and self.win32_combo.get() != "Выберите файл...":
            selected_tweaks.append(os.path.join(self.win32_path, self.win32_combo.get()))
        if hasattr(self, 'services_combo') and self.services_combo.get() != "Выберите файл...":
            selected_tweaks.append(os.path.join(self.services_path, self.services_combo.get()))

        if not selected_tweaks:
            messagebox.showinfo("Информация", "Не выбрано ни одного твика")
            return

        count = len(selected_tweaks)
        if messagebox.askyesno("Подтверждение", f"Применить {count} выбранных твиков?"):
            success = 0
            for tweak in selected_tweaks:
                if self.run_script(tweak):
                    success += 1
            messagebox.showinfo("Результат", f"✅ {success}/{count} выполнено")


def create_optimization_tab(parent, config):
    tab_frame = ttk.Frame(parent)
    optimization_tab = OptimizationTab(tab_frame, config)
    return tab_frame
