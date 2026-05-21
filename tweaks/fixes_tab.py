import tkinter as tk
from tkinter import ttk
import os
import subprocess
import configparser
import sys

# Используем logger из main.py вместо создания нового экземпляра
main_module = sys.modules.get('__main__')
if main_module and hasattr(main_module, 'logger'):
    logger = main_module.logger
else:
    from logger import Logger
    logger = Logger()

# Импортируем классы чекбоксов из main.py
# Эти классы будут импортированы динамически при создании вкладки

def create_fixes_tab(tab_control):
    # Создаем вкладку для исправлений
    fixes_tab = ttk.Frame(tab_control)
    tab_control.add(fixes_tab, text='Исправления')
    
    # Создаем основной контейнер
    main_container = ttk.Frame(fixes_tab)
    main_container.pack(fill='both', expand=True, padx=10, pady=10)
    
    # Создаем горизонтальный контейнер для левой и правой частей
    horizontal_container = ttk.Frame(main_container)
    horizontal_container.pack(fill='both', expand=True)
    
    # ========== ЛЕВАЯ ЧАСТЬ: Информация о REVERT DE3NAKE и команды ==========
    left_frame = ttk.Frame(horizontal_container)
    left_frame.pack(side='left', fill='both', padx=(0, 10))
    left_frame.configure(width=400)
    
    # Canvas и Scrollbar для левой части
    left_canvas = tk.Canvas(left_frame)
    left_scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=left_canvas.yview)
    left_scrollable_frame = ttk.Frame(left_canvas)
    
    left_scrollable_frame.bind(
        "<Configure>",
        lambda e: left_canvas.configure(scrollregion=left_canvas.bbox("all"))
    )
    
    left_canvas.create_window((0, 0), window=left_scrollable_frame, anchor="nw")
    left_canvas.configure(yscrollcommand=left_scrollbar.set)
    
    def on_left_mousewheel(event):
        left_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    left_canvas.bind_all("<MouseWheel>", on_left_mousewheel)
    
    def configure_left_scroll_region(event):
        canvas_width = event.width
        canvas_items = left_canvas.find_all()
        if canvas_items:
            left_canvas.itemconfig(canvas_items[0], width=canvas_width)
        left_canvas.configure(scrollregion=left_canvas.bbox("all"))
    
    left_canvas.bind('<Configure>', configure_left_scroll_region)
    
    left_canvas.pack(side="left", fill="both", expand=True)
    left_scrollbar.pack(side="right", fill="y")
    
    # Контент левой части
    left_content = ttk.Frame(left_scrollable_frame, padding=15)
    left_content.pack(fill='both', expand=True)
    
    # Заголовок REVERT DE3NAKE
    revert_title = ttk.Label(
        left_content,
        text="🤩 REVERT DE3NAKE ⚫ ИСПРАВЛЕНИЯ ОТ ВСЕХ ПРОБЛЕМ",
        font=("Segoe UI", 14, "bold"),
        wraplength=350,
        justify="center"
    )
    revert_title.pack(anchor='w', pady=(0, 10))
    
    # Описание
    revert_desc = ttk.Label(
        left_content,
        text="🔴ТВИК исправляет все ошибки в системе после оптимизаций и настроек.\n\n"
             "🔴Исправляет все проблемы с ПК/НОУТБУКОМ\n\n"
             "🔴Использовать только при НЕОБХОДИМОСТИ!\n\n"
             "🔴ОСТОРОЖНО: МОЖЕТ УПАСТЬ ФПС В ИГРАХ",
        font=("Segoe UI", 10),
        wraplength=350,
        justify="left",
        foreground="red"
    )
    revert_desc.pack(anchor='w', pady=(0, 15))
    
    # Кнопка запуска REVERT DE3NAKE
    def launch_revert_de3nake():
        # Пробуем разные возможные пути
        possible_paths = [
            "tweaks\\Исправления\\REVERT DE3NAKE.bat",
            "tweaks\\Исправления\\REVERT DE3NAKE\\REVERT DE3NAKE.bat",
            "tweaks\\REVERT DE3NAKE.bat"
        ]
        revert_path = None
        for path in possible_paths:
            if os.path.exists(path):
                revert_path = path
                break
        
        if revert_path:
            # Запускаем через функцию execute_old из main.py
            import sys
            main_module = sys.modules.get('__main__')
            if main_module and hasattr(main_module, 'execute_old'):
                # Создаем временный чекбокс для запуска
                temp_var = tk.BooleanVar()
                if hasattr(main_module, 'checkboxes'):
                    main_module.checkboxes['REVERT DE3NAKE.bat'] = temp_var
                    temp_var.set(True)
                    # Запускаем execute_old, но только для этого чекбокса
                    # Вместо этого запустим напрямую
                    pass
            # Запускаем напрямую
            subprocess.call(f'cmd /c "{revert_path}"', shell=True)
            logger.log_info("Запущен REVERT DE3NAKE")
        else:
            logger.log_warning("Файл REVERT DE3NAKE.bat не найден")
    
    revert_btn = ttk.Button(
        left_content,
        text="REVERT DE3NAKE",
        command=launch_revert_de3nake,
        bootstyle="danger-outline"
    )
    revert_btn.pack(fill='x', pady=(0, 20))
    
    # Разделитель
    separator1 = ttk.Separator(left_content, orient='horizontal')
    separator1.pack(fill='x', pady=10)
    
    # Заголовок команд
    commands_title = ttk.Label(
        left_content,
        text="🧠 КОМАНДЫ ДЛЯ ЛЕЧЕНИЯ WINDOWS 💻",
        font=("Segoe UI", 12, "bold"),
        wraplength=350,
        justify="center"
    )
    commands_title.pack(anchor='w', pady=(0, 10))
    
    # Эффект
    effect_label = ttk.Label(
        left_content,
        text="🚀 ЭФФЕКТ:\n\n"
             "✅ Восстанавливает даже убитые обновлениями системы\n"
             "✅ Возвращает к жизни BSOD-экран смерти\n"
             "✅ Чинит ~95% системных ошибок\n"
             "✅ Исправляет проблемы с загрузкой файлов\n"
             "✅ Стабилизирует подключение к интернету\n"
             "✅ Сбрасывает каталог Winsock",
        font=("Segoe UI", 9),
        wraplength=350,
        justify="left"
    )
    effect_label.pack(anchor='w', pady=(0, 15))
    
    # Команды для лечения
    commands_data = [
        {
            "title": "⚙️ DISM /CheckHealth ➖ Мгновенная диагностика",
            "command": "DISM /Online /Cleanup-Image /CheckHealth",
            "description": "DISM /Online /Cleanup-Image /CheckHealth"
        },
        {
            "title": "⚙️ Перезапуск служб ➖",
            "command": "net start wuauserv && net start cryptSvc && net start bits && net start msiserver",
            "description": "net start wuauserv\nnet start cryptSvc\nnet start bits\nnet start msiserver"
        },
        {
            "title": "⚙️ ipconfig /flushdns ➖ Проблемы с интернетом",
            "command": "ipconfig /flushdns",
            "description": "ipconfig /flushdns"
        },
        {
            "title": "⚙️ chkdsk C: /f /r ➖ Проверка и исправление ошибок с дисками",
            "command": "chkdsk C: /f /r",
            "description": "chkdsk C: /f /r"
        },
        {
            "title": "⚙️ ipconfig /flushdns ➖ Очистить DNS-кэш",
            "command": "ipconfig /flushdns",
            "description": "ipconfig /flushdns"
        },
        {
            "title": "⚙️ chkdsk C: /f /r ➖ Проблемы с загрузкой системы или файлами",
            "command": "chkdsk C: /f /r",
            "description": "chkdsk C: /f /r"
        },
        {
            "title": "⚙️ DISM /RestoreHealth ➖ Глубокое лечение",
            "command": "DISM /Online /Cleanup-Image /RestoreHealth",
            "description": "DISM /Online /Cleanup-Image /RestoreHealth"
        },
        {
            "title": "⚙️ sfc /scannow ➖ Восстанавливает поврежденные системные файлы Windows",
            "command": "sfc /scannow",
            "description": "sfc /scannow"
        },
        {
            "title": "⚙️ Сбрасывает каталог Winsock к настройкам по умолчанию",
            "command": "netsh int ip reset",
            "description": "netsh int ip reset"
        }
    ]
    
    def execute_command(cmd):
        """Выполняет команду в cmd"""
        try:
            subprocess.Popen(f'cmd /c "{cmd}"', shell=True)
            logger.log_info(f"Выполнена команда: {cmd}")
        except Exception as e:
            logger.log_error(f"Ошибка при выполнении команды {cmd}: {str(e)}")
    
    for cmd_data in commands_data:
        cmd_frame = ttk.Labelframe(left_content, text=cmd_data["title"], padding=10)
        cmd_frame.pack(fill='x', pady=5)
        
        cmd_desc = ttk.Label(
            cmd_frame,
            text=cmd_data["description"],
            font=("Segoe UI", 9),
            wraplength=320,
            justify="left"
        )
        cmd_desc.pack(anchor='w', pady=(0, 5))
        
        cmd_btn = ttk.Button(
            cmd_frame,
            text="▶ Запустить",
            command=lambda c=cmd_data["command"]: execute_command(c),
            bootstyle="info-outline",
            width=20
        )
        cmd_btn.pack(anchor='w', pady=(5, 0))
    
    # ========== ПРАВАЯ ЧАСТЬ: Категории с чекбоксами ==========
    right_frame = ttk.Frame(horizontal_container)
    right_frame.pack(side='right', fill='both', expand=True)
    
    # Canvas и Scrollbar для правой части
    right_canvas = tk.Canvas(right_frame)
    right_scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=right_canvas.yview)
    right_scrollable_frame = ttk.Frame(right_canvas)
    
    right_scrollable_frame.bind(
        "<Configure>",
        lambda e: right_canvas.configure(scrollregion=right_canvas.bbox("all"))
    )
    
    right_canvas.create_window((0, 0), window=right_scrollable_frame, anchor="nw")
    right_canvas.configure(yscrollcommand=right_scrollbar.set)
    
    def on_right_mousewheel(event):
        right_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    right_canvas.bind_all("<MouseWheel>", on_right_mousewheel)
    
    def configure_right_scroll_region(event):
        canvas_width = event.width
        canvas_items = right_canvas.find_all()
        if canvas_items:
            right_canvas.itemconfig(canvas_items[0], width=canvas_width)
        right_canvas.configure(scrollregion=right_canvas.bbox("all"))
    
    right_canvas.bind('<Configure>', configure_right_scroll_region)
    
    right_canvas.pack(side="left", fill="both", expand=True)
    right_scrollbar.pack(side="right", fill="y")
    
    # Контент правой части
    right_content = ttk.Frame(right_scrollable_frame, padding=10)
    right_content.pack(fill='both', expand=True)
    
    # Получаем данные из tweaks7.py
    from tweaks.tweaks7 import tabs
    
    # Импортируем классы чекбоксов и функции из main
    # Получаем глобальные объекты из main
    import sys
    main_module = sys.modules.get('__main__')
    if main_module:
        RectangleCheckbox = getattr(main_module, 'RectangleCheckbox', None)
        WideRectangleCheckbox = getattr(main_module, 'WideRectangleCheckbox', None)
        ExpandableWideRectangleCheckbox = getattr(main_module, 'ExpandableWideRectangleCheckbox', None)
        get_button_name = getattr(main_module, 'get_button_name', lambda x: 'Исправления')
        checkboxes = getattr(main_module, 'checkboxes', {})
        config = getattr(main_module, 'config', configparser.ConfigParser())
    else:
        RectangleCheckbox = None
        WideRectangleCheckbox = None
        ExpandableWideRectangleCheckbox = None
        get_button_name = lambda x: 'Исправления'
        checkboxes = {}
        config = configparser.ConfigParser()
        config.read("user_data//settings.ini", encoding="cp1251")
    
    # Получаем режим отображения из настроек
    display_mode = config.get("General", "checkbox_display_mode", fallback="regular")
    
    # Словарь для хранения чекбоксов
    fixes_checkboxes = {}
    
    # Создаем фреймы для каждой категории
    for category, files in tabs.items():
        if not files:  # Пропускаем пустые категории
            continue
        
        # Создаем Labelframe для категории
        category_frame = ttk.Labelframe(right_content, text=category, padding=15)
        category_frame.pack(fill='x', pady=10)
        
        # Создаем внутренний фрейм для чекбоксов
        checkboxes_inner_frame = ttk.Frame(category_frame)
        checkboxes_inner_frame.pack(fill='both', expand=True)
        
        # Создаем чекбоксы для файлов в категории
        for i, file_name in enumerate(files):
            checkbox_var = tk.BooleanVar()
            tab_name = "Исправления"
            # Путь к файлу: учитываем, что файл может быть в подпапке категории
            # Если в имени файла есть обратный слэш, это подпапка
            if '\\' in file_name:
                # Файл в подпапке категории
                filepath = f"tweaks\\Исправления\\{category}\\{file_name}"
            else:
                # Файл напрямую в папке категории
                filepath = f"tweaks\\Исправления\\{category}\\{file_name}"
            
            # Проверяем режим отображения
            if display_mode == "expandable" and ExpandableWideRectangleCheckbox:
                checkbox = ExpandableWideRectangleCheckbox(
                    checkboxes_inner_frame,
                    file_name,
                    checkbox_var,
                    tab_name,
                    filepath
                )
                # Переопределяем метод _launch_script для использования правильного пути
                original_launch = checkbox._launch_script
                def custom_launch():
                    checkbox.checkbox_var.set(True)
                    # Проверяем существование файла
                    if not os.path.exists(filepath):
                        logger.log_error(f"Файл не найден: {filepath}")
                        return
                    try:
                        if file_name.endswith((".bat", ".cmd")):
                            subprocess.Popen(f'cmd /c "{filepath}"', shell=True)
                        elif file_name.endswith(".exe"):
                            subprocess.Popen(f'"{filepath}"', shell=True)
                        elif file_name.endswith(".ps1"):
                            subprocess.Popen([
                                "powershell.exe",
                                "-ExecutionPolicy", "Bypass",
                                "-File", filepath
                            ])
                        elif file_name.endswith(".reg"):
                            subprocess.Popen(f'reg import "{filepath}"', shell=True)
                        elif file_name.endswith(".vbs"):
                            subprocess.Popen(f'cscript "{filepath}"', shell=True)
                        logger.log_info(f"Запущен файл: {file_name}")
                    except Exception as e:
                        logger.log_error(f"Ошибка при запуске файла {file_name}: {str(e)}")
                checkbox._launch_script = custom_launch
                checkbox.pack(fill='x', padx=5, pady=5)
            elif display_mode == "wide" and WideRectangleCheckbox:
                checkbox = WideRectangleCheckbox(
                    checkboxes_inner_frame,
                    file_name,
                    checkbox_var,
                    tab_name,
                    filepath
                )
                # Переопределяем метод _launch_script для использования правильного пути
                def custom_launch():
                    checkbox.checkbox_var.set(True)
                    # Проверяем существование файла
                    if not os.path.exists(filepath):
                        logger.log_error(f"Файл не найден: {filepath}")
                        return
                    try:
                        if file_name.endswith((".bat", ".cmd")):
                            subprocess.Popen(f'cmd /c "{filepath}"', shell=True)
                        elif file_name.endswith(".exe"):
                            subprocess.Popen(f'"{filepath}"', shell=True)
                        elif file_name.endswith(".ps1"):
                            subprocess.Popen([
                                "powershell.exe",
                                "-ExecutionPolicy", "Bypass",
                                "-File", filepath
                            ])
                        elif file_name.endswith(".reg"):
                            subprocess.Popen(f'reg import "{filepath}"', shell=True)
                        elif file_name.endswith(".vbs"):
                            subprocess.Popen(f'cscript "{filepath}"', shell=True)
                        logger.log_info(f"Запущен файл: {file_name}")
                    except Exception as e:
                        logger.log_error(f"Ошибка при запуске файла {file_name}: {str(e)}")
                checkbox._launch_script = custom_launch
                checkbox.pack(fill='x', padx=5, pady=5)
            elif display_mode == "rectangle" and RectangleCheckbox:
                checkbox = RectangleCheckbox(
                    checkboxes_inner_frame,
                    file_name,
                    checkbox_var,
                    tab_name,
                    filepath
                )
                # Переопределяем метод _launch_script для использования правильного пути
                def custom_launch():
                    checkbox.checkbox_var.set(True)
                    # Проверяем существование файла
                    if not os.path.exists(filepath):
                        logger.log_error(f"Файл не найден: {filepath}")
                        return
                    try:
                        if file_name.endswith((".bat", ".cmd")):
                            subprocess.Popen(f'cmd /c "{filepath}"', shell=True)
                        elif file_name.endswith(".exe"):
                            subprocess.Popen(f'"{filepath}"', shell=True)
                        elif file_name.endswith(".ps1"):
                            subprocess.Popen([
                                "powershell.exe",
                                "-ExecutionPolicy", "Bypass",
                                "-File", filepath
                            ])
                        elif file_name.endswith(".reg"):
                            subprocess.Popen(f'reg import "{filepath}"', shell=True)
                        elif file_name.endswith(".vbs"):
                            subprocess.Popen(f'cscript "{filepath}"', shell=True)
                        logger.log_info(f"Запущен файл: {file_name}")
                    except Exception as e:
                        logger.log_error(f"Ошибка при запуске файла {file_name}: {str(e)}")
                checkbox._launch_script = custom_launch
                checkbox.pack(fill='x', padx=5, pady=5)
            else:
                # Обычный чекбокс с кнопкой запуска
                checkbox_frame = ttk.Frame(checkboxes_inner_frame)
                checkbox_frame.pack(fill='x', padx=5, pady=2)
                
                checkbox = ttk.Checkbutton(
                    checkbox_frame,
                    text=file_name,
                    variable=checkbox_var
                )
                checkbox.pack(side='left', anchor='w')
                
                # Добавляем кнопку запуска для обычного чекбокса
                def launch_fix(f_path=filepath, f_name=file_name):
                    """Запускает файл исправления"""
                    # Проверяем существование файла
                    if not os.path.exists(f_path):
                        logger.log_error(f"Файл не найден: {f_path}")
                        return
                    try:
                        if f_name.endswith((".bat", ".cmd")):
                            subprocess.Popen(f'cmd /c "{f_path}"', shell=True)
                        elif f_name.endswith(".exe"):
                            subprocess.Popen(f'"{f_path}"', shell=True)
                        elif f_name.endswith(".ps1"):
                            subprocess.Popen([
                                "powershell.exe",
                                "-ExecutionPolicy", "Bypass",
                                "-File", f_path
                            ])
                        elif f_name.endswith(".reg"):
                            subprocess.Popen(f'reg import "{f_path}"', shell=True)
                        elif f_name.endswith(".vbs"):
                            subprocess.Popen(f'cscript "{f_path}"', shell=True)
                        logger.log_info(f"Запущен файл: {f_name}")
                    except Exception as e:
                        logger.log_error(f"Ошибка при запуске файла {f_name}: {str(e)}")
                
                launch_btn = ttk.Button(
                    checkbox_frame,
                    text="▶ Запустить",
                    command=launch_fix,
                    width=12
                )
                launch_btn.pack(side='right', padx=(5, 0))
            
            fixes_checkboxes[file_name] = checkbox_var
            # Добавляем в глобальный словарь checkboxes, если он доступен
            if main_module and hasattr(main_module, 'checkboxes'):
                # Используем уникальный ключ с категорией для избежания конфликтов
                unique_key = f"{category}\\{file_name}"
                main_module.checkboxes[unique_key] = checkbox_var
    
    return fixes_tab
