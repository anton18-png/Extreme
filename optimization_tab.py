import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import os
import subprocess
import glob

class OptimizationTab:
    """Класс для вкладки оптимизации в стиле SapphireTool"""
    
    def __init__(self, parent, config):
        self.parent = parent
        self.config = config
        
        # Базовый путь к tweaks
        self.tweaks_path = r"C:\Apps\Extreme\tweaks"
        
        # Пути к папкам
        self.nvidia_path = os.path.join(self.tweaks_path, "Драйверы", "Оптимизация Nvidia")
        self.amd_path = os.path.join(self.tweaks_path, "Драйверы", "Оптимизация Amd")
        self.intel_path = os.path.join(self.tweaks_path, "Драйверы", "Оптимизация Intel")
        self.directx_path = os.path.join(self.tweaks_path, "Драйверы", "DirectX", "Оптимизация DirectX")
        self.opengl_path = os.path.join(self.tweaks_path, "Драйверы", "DirectX", "Оптимизация OpenGL")
        self.svchost_path = os.path.join(self.tweaks_path, "Драйверы", "Порог разделения svchost")
        self.win32_path = os.path.join(self.tweaks_path, "Драйверы", "Разделение приоритетов Win32")
        self.services_path = os.path.join(self.tweaks_path, "Драйверы", "Службы")
        
        # Получаем списки файлов
        self.nvidia_files = self.get_files_from_folder(self.nvidia_path)
        self.amd_files = self.get_files_from_folder(self.amd_path)
        self.intel_files = self.get_files_from_folder(self.intel_path)
        self.directx_files = self.get_files_from_folder(self.directx_path)
        self.opengl_files = self.get_files_from_folder(self.opengl_path)
        self.svchost_files = self.get_files_from_folder(self.svchost_path)
        self.win32_files = self.get_files_from_folder(self.win32_path)
        self.services_files = self.get_files_from_folder(self.services_path)
        
        # Переменные для чекбоксов
        self.nvidia_vars = {}
        self.amd_vars = {}
        self.intel_vars = {}
        self.directx_vars = {}
        self.opengl_vars = {}
        
        # Цветовая схема
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
        
        self.setup_ui()
    
    def get_files_from_folder(self, folder_path):
        """Получает список файлов из папки"""
        if not os.path.exists(folder_path):
            return []
        
        all_files = []
        for ext in ['*.bat', '*.cmd', '*.exe', '*.ps1']:
            all_files.extend(glob.glob(os.path.join(folder_path, ext)))
        
        return [os.path.basename(f) for f in all_files]
    
    def setup_ui(self):
        """Настройка компактного UI в стиле SapphireTool"""
        
        # Главный контейнер
        main = ttk.Frame(self.parent)
        main.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # ========== ВЕРХНЯЯ ПАНЕЛЬ С ВКЛАДКАМИ ==========
        notebook = ttk.Notebook(main)
        notebook.pack(fill=BOTH, expand=True)
        
        # Вкладка NVIDIA
        nvidia_frame = ttk.Frame(notebook)
        notebook.add(nvidia_frame, text="NVIDIA")
        self.create_nvidia_compact(nvidia_frame)
        
        # Вкладка AMD
        amd_frame = ttk.Frame(notebook)
        notebook.add(amd_frame, text="AMD")
        self.create_amd_compact(amd_frame)
        
        # Вкладка Intel
        intel_frame = ttk.Frame(notebook)
        notebook.add(intel_frame, text="Intel")
        self.create_intel_compact(intel_frame)
        
        # Вкладка DirectX
        directx_frame = ttk.Frame(notebook)
        notebook.add(directx_frame, text="DirectX")
        self.create_directx_compact(directx_frame)
        
        # Вкладка OpenGL
        opengl_frame = ttk.Frame(notebook)
        notebook.add(opengl_frame, text="OpenGL")
        self.create_opengl_compact(opengl_frame)
        
        # ========== НИЖНЯЯ ПАНЕЛЬ ==========
        bottom_frame = ttk.Frame(main)
        bottom_frame.pack(fill=X, pady=(10, 0))
        
        # Левая часть - выпадающие списки
        dropdowns_frame = ttk.Frame(bottom_frame)
        dropdowns_frame.pack(side=LEFT, fill=X, expand=True)
        
        # Создаем строку с выпадающими списками
        self.create_dropdown_row(dropdowns_frame)
        
        # Правая часть - кнопка
        apply_btn = ttk.Button(
            bottom_frame,
            text="Применить выбранные",
            bootstyle="success-outline",
            command=self.apply_selected_tweaks,
            width=20
        )
        apply_btn.pack(side=RIGHT, padx=(10, 0))
    
    def create_nvidia_compact(self, parent):
        """Компактная вкладка NVIDIA"""
        
        # Основной контейнер с прокруткой
        canvas = ttk.Canvas(parent, highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable = ttk.Frame(canvas)
        
        scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Компактная сетка 3 колонки
        row = 0
        col = 0
        
        for file in sorted(self.nvidia_files):
            # Очищаем название
            display_name = file.replace(".bat", "").replace(".cmd", "").replace(".exe", "").replace(".ps1", "")
            
            # Создаем переменную
            var = ttk.BooleanVar(value=False)
            self.nvidia_vars[file] = var
            
            # Чекбокс
            cb = ttk.Checkbutton(
                scrollable,
                text=display_name,
                variable=var,
                bootstyle="primary-toolbutton"
            )
            cb.grid(row=row, column=col, sticky=W, padx=5, pady=2)
            
            # Переход к следующей колонке
            col += 1
            if col > 2:  # 3 колонки
                col = 0
                row += 1
    
    def create_amd_compact(self, parent):
        """Компактная вкладка AMD"""
        
        canvas = ttk.Canvas(parent, highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable = ttk.Frame(canvas)
        
        scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        row = 0
        col = 0
        
        for file in sorted(self.amd_files):
            display_name = file.replace(".bat", "").replace(".cmd", "").replace(".exe", "").replace(".ps1", "")
            
            var = ttk.BooleanVar(value=False)
            self.amd_vars[file] = var
            
            cb = ttk.Checkbutton(
                scrollable,
                text=display_name,
                variable=var,
                bootstyle="primary-toolbutton"
            )
            cb.grid(row=row, column=col, sticky=W, padx=5, pady=2)
            
            col += 1
            if col > 2:
                col = 0
                row += 1
    
    def create_intel_compact(self, parent):
        """Компактная вкладка Intel"""
        
        canvas = ttk.Canvas(parent, highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable = ttk.Frame(canvas)
        
        scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        row = 0
        col = 0
        
        for file in sorted(self.intel_files):
            display_name = file.replace(".bat", "").replace(".cmd", "").replace(".exe", "").replace(".ps1", "")
            
            var = ttk.BooleanVar(value=False)
            self.intel_vars[file] = var
            
            cb = ttk.Checkbutton(
                scrollable,
                text=display_name,
                variable=var,
                bootstyle="primary-toolbutton"
            )
            cb.grid(row=row, column=col, sticky=W, padx=5, pady=2)
            
            col += 1
            if col > 2:
                col = 0
                row += 1
    
    def create_directx_compact(self, parent):
        """Компактная вкладка DirectX"""
        
        canvas = ttk.Canvas(parent, highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable = ttk.Frame(canvas)
        
        scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        row = 0
        col = 0
        
        for file in sorted(self.directx_files):
            display_name = file.replace(".bat", "").replace(".cmd", "").replace(".exe", "").replace(".ps1", "")
            
            var = ttk.BooleanVar(value=False)
            self.directx_vars[file] = var
            
            cb = ttk.Checkbutton(
                scrollable,
                text=display_name,
                variable=var,
                bootstyle="primary-toolbutton"
            )
            cb.grid(row=row, column=col, sticky=W, padx=5, pady=2)
            
            col += 1
            if col > 2:
                col = 0
                row += 1
    
    def create_opengl_compact(self, parent):
        """Компактная вкладка OpenGL"""
        
        canvas = ttk.Canvas(parent, highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable = ttk.Frame(canvas)
        
        scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        row = 0
        col = 0
        
        for file in sorted(self.opengl_files):
            display_name = file.replace(".bat", "").replace(".cmd", "").replace(".exe", "").replace(".ps1", "")
            
            var = ttk.BooleanVar(value=False)
            self.opengl_vars[file] = var
            
            cb = ttk.Checkbutton(
                scrollable,
                text=display_name,
                variable=var,
                bootstyle="primary-toolbutton"
            )
            cb.grid(row=row, column=col, sticky=W, padx=5, pady=2)
            
            col += 1
            if col > 2:
                col = 0
                row += 1
    
    def create_dropdown_row(self, parent):
        """Создание строки с выпадающими списками"""
        
        # Создаем фреймы для каждого dropdown
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
    
    def run_script(self, script_path):
        """Запуск скрипта"""
        try:
            if not os.path.exists(script_path):
                return False
                
            if script_path.endswith('.ps1'):
                subprocess.run(['powershell.exe', '-ExecutionPolicy', 'Bypass', '-File', script_path], shell=True)
            else:
                # subprocess.run([script_path], shell=True)
                subprocess.call(f'Utils\\launcher.exe "{script_path}"', shell=True)
            return True
        except Exception as e:
            print(f"Ошибка при запуске {script_path}: {e}")
            return False
    
    def apply_selected_tweaks(self):
        """Применение выбранных твиков"""
        
        selected_tweaks = []
        
        # NVIDIA
        for file, var in self.nvidia_vars.items():
            if var.get():
                selected_tweaks.append(os.path.join(self.nvidia_path, file))
        
        # AMD
        for file, var in self.amd_vars.items():
            if var.get():
                selected_tweaks.append(os.path.join(self.amd_path, file))
        
        # Intel
        for file, var in self.intel_vars.items():
            if var.get():
                selected_tweaks.append(os.path.join(self.intel_path, file))
        
        # DirectX
        for file, var in self.directx_vars.items():
            if var.get():
                selected_tweaks.append(os.path.join(self.directx_path, file))
        
        # OpenGL
        for file, var in self.opengl_vars.items():
            if var.get():
                selected_tweaks.append(os.path.join(self.opengl_path, file))
        
        # Выпадающие списки
        if hasattr(self, 'svchost_combo') and self.svchost_combo.get() != "Выберите файл...":
            selected_tweaks.append(os.path.join(self.svchost_path, self.svchost_combo.get()))
        
        if hasattr(self, 'win32_combo') and self.win32_combo.get() != "Выберите файл...":
            selected_tweaks.append(os.path.join(self.win32_path, self.win32_combo.get()))
        
        if hasattr(self, 'services_combo') and self.services_combo.get() != "Выберите файл...":
            selected_tweaks.append(os.path.join(self.services_path, self.services_combo.get()))
        
        if not selected_tweaks:
            messagebox.showinfo("Информация", "Не выбрано ни одного твика")
            return
        
        # Короткое подтверждение
        count = len(selected_tweaks)
        if messagebox.askyesno("Подтверждение", f"Применить {count} выбранных твиков?"):
            success = 0
            for tweak in selected_tweaks:
                if self.run_script(tweak):
                    success += 1
            
            messagebox.showinfo("Результат", f"✅ {success}/{count} выполнено")


def create_optimization_tab(parent, config):
    """Создание вкладки оптимизация"""
    tab_frame = ttk.Frame(parent)
    optimization_tab = OptimizationTab(tab_frame, config)
    return tab_frame