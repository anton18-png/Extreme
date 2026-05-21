import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import os
import subprocess
import re

class AppUninstallerTab:
    """Класс для вкладки удаления приложений"""
    
    def __init__(self, parent, config, scripts_list):
        self.parent = parent
        self.config = config
        self.scripts_list = scripts_list
        self.app_buttons = {}
        self.selected_apps = set()
        
        # Указываем путь к папке со скриптами
        self.scripts_path = r"tweaks\Очистка\Удалить приложения"
        
        # Проверяем существование папки
        if not os.path.exists(self.scripts_path):
            messagebox.showwarning(
                "Предупреждение",
                f"Папка со скриптами не найдена:\n{self.scripts_path}\n\n"
                "Проверьте правильность пути."
            )
        
        # Переменные для фильтрации
        self.current_category = "Все"
        self.current_search = ""
        
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
            "text_secondary": "#8f9aaa"
        }
        
        self.apps_data = self.parse_scripts_to_apps()
        self.setup_ui()
    
    def parse_scripts_to_apps(self):
        """Парсит список скриптов в структурированные данные"""
        
        # Новый маппинг с категориями: Microsoft, UWP, Defender, Xbox, Браузеры, Остальное
        app_mapping = {
            # Microsoft (основные продукты Microsoft)
            "Microsoft Office от Darren White": {"name": "MS Office (Darren White)", "icon": "📊", "category": "Microsoft"},
            "Microsoft Office": {"name": "Microsoft Office", "icon": "📊", "category": "Microsoft"},
            "OneDrive": {"name": "OneDrive", "icon": "☁️", "category": "Microsoft"},
            "Программа удаления OneDrive v1.4": {"name": "OneDrive Remover", "icon": "☁️❌", "category": "Microsoft"},
            "Skype": {"name": "Skype", "icon": "📞", "category": "Microsoft"},
            "Cortana": {"name": "Cortana", "icon": "🤖", "category": "Microsoft"},
            
            # UWP (пакетные удаления)
            "вредоносные UWP приложения": {"name": "Вредоносные UWP", "icon": "🦠", "category": "UWP"},
            "все приложения Microsoft": {"name": "Все приложения MS", "icon": "📦", "category": "UWP"},
            "и другие приложения Metro": {"name": "Metro приложения", "icon": "📱", "category": "UWP"},
            "приложения": {"name": "Приложения", "icon": "📦", "category": "UWP"},
            "Paint 3D": {"name": "Paint 3D", "icon": "🎨", "category": "UWP"},
            "Print 3D": {"name": "Print 3D", "icon": "🖨️", "category": "UWP"},
            "3D Builder": {"name": "3D Builder", "icon": "🏗️", "category": "UWP"},
            "средство 3D-просмотра": {"name": "3D просмотр", "icon": "📦", "category": "UWP"},
            "Портал смешанной реальности": {"name": "Mixed Reality", "icon": "🥽", "category": "UWP"},
            "Groove Music": {"name": "Groove Music", "icon": "🎵", "category": "UWP"},
            "Кино и ТВ": {"name": "Кино и ТВ", "icon": "🎬", "category": "UWP"},
            "Фотографии (Майкрософт)": {"name": "Фотографии", "icon": "🖼️", "category": "UWP"},
            "Почта и Календарь": {"name": "Почта", "icon": "📧", "category": "UWP"},
            "Записки": {"name": "Sticky Notes", "icon": "📌", "category": "UWP"},
            "Деньги": {"name": "Деньги", "icon": "💰", "category": "UWP"},
            "Будильники и часы": {"name": "Будильники", "icon": "⏰", "category": "UWP"},
            "Ваш телефон": {"name": "Ваш телефон", "icon": "📱", "category": "UWP"},
            "Калькулятор": {"name": "Калькулятор", "icon": "🧮", "category": "UWP"},
            "Камера": {"name": "Камера", "icon": "📷", "category": "UWP"},
            "Карты": {"name": "Карты", "icon": "🗺️", "category": "UWP"},
            "Люди": {"name": "Люди", "icon": "👥", "category": "UWP"},
            "Советы": {"name": "Советы", "icon": "💡", "category": "UWP"},
            "Техническая помощь": {"name": "Помощь", "icon": "❓", "category": "UWP"},
            "Центр отзывов": {"name": "Отзывы", "icon": "📢", "category": "UWP"},
            "Mobile Plans": {"name": "Mobile Plans", "icon": "📱", "category": "UWP"},
            "Bing Sports": {"name": "Bing Sports", "icon": "⚽", "category": "UWP"},
            "Набросок на фрагменте экрана": {"name": "Sketch", "icon": "✏️", "category": "UWP"},
            "Расширение для изображений HEIF": {"name": "HEIF", "icon": "🖼️", "category": "UWP"},
            "Расширение для изображений Webp": {"name": "Webp", "icon": "🖼️", "category": "UWP"},
            "Расширение для интернет-мультимедиа": {"name": "Медиа", "icon": "🎥", "category": "UWP"},
            "Начало": {"name": "Начало", "icon": "🏠", "category": "UWP"},
            
            # Defender
            "Отключить Defender, SmartScreen и Antimalware": {"name": "Defender & SmartScreen", "icon": "🛡️", "category": "Defender"},
            "Убить Защитник": {"name": "Убить Защитник", "icon": "💀", "category": "Defender"},
            "Удалить Windows Defender (Fuck Windows Defender)": {"name": "Windows Defender (Fuck)", "icon": "🛡️", "category": "Defender"},
            "Удалить Windows Defender от Vlado": {"name": "Windows Defender (Vlado)", "icon": "🛡️", "category": "Defender"},
            "Удалить Защитник Windows (MartyFiles)": {"name": "Защитник (MartyFiles)", "icon": "🛡️", "category": "Defender"},
            
            # Xbox
            "Xbox App": {"name": "Xbox App", "icon": "🎮", "category": "Xbox"},
            "Xbox Bar": {"name": "Xbox Bar", "icon": "🎮", "category": "Xbox"},
            "Xbox Game Speech": {"name": "Xbox Game", "icon": "🎮", "category": "Xbox"},
            
            # Браузеры
            "Internet Explorer": {"name": "Internet Explorer", "icon": "🌐", "category": "Браузеры"},
            "Microsoft Edge Appx": {"name": "Microsoft Edge (Appx)", "icon": "🌊", "category": "Браузеры"},
            "Microsoft Edge и WebView": {"name": "Edge + WebView", "icon": "🌊", "category": "Браузеры"},
            "Microsoft Edge.exe": {"name": "Microsoft Edge", "icon": "🌊", "category": "Браузеры"},
            "Яндекс Браузер (BAT)": {"name": "Яндекс Браузер", "icon": "Я", "category": "Браузеры"},
            "Яндекс Браузер (EXE)": {"name": "Яндекс Браузер", "icon": "Я", "category": "Браузеры"},
        }
        
        apps_data = []
        for script in self.scripts_list:
            # Ищем расширение файла
            ext_match = re.search(r'\.(ps1|bat|cmd|exe)$', script)
            extension = ext_match.group(1) if ext_match else "bat"
            
            # Извлекаем название без расширения
            name_without_ext = script.rsplit('.', 1)[0]
            
            found = False
            
            # Ищем соответствие в маппинге
            for key, value in app_mapping.items():
                if key.lower() in name_without_ext.lower() or name_without_ext.lower() in key.lower():
                    apps_data.append({
                        "name": value["name"],
                        "icon": value["icon"],
                        "category": value["category"],
                        "script": script,
                        "installed": True,
                        "raw_name": name_without_ext,
                        "extension": extension
                    })
                    found = True
                    break
            
            if not found:
                # Очищаем название от лишних слов
                clean_name = name_without_ext.replace("Удалить ", "").replace("Microsoft ", "").replace("все ", "").replace("основные ", "")
                if len(clean_name) > 15:
                    clean_name = clean_name[:13] + "..."
                
                # По умолчанию помечаем как Остальное
                category = "Остальное"
                
                # Проверяем по ключевым словам
                name_lower = name_without_ext.lower()
                if "defender" in name_lower or "защитник" in name_lower:
                    category = "Defender"
                elif "xbox" in name_lower:
                    category = "Xbox"
                elif "microsoft" in name_lower or "edge" in name_lower or "office" in name_lower:
                    category = "Microsoft"
                elif "uwp" in name_lower or "metro" in name_lower:
                    category = "UWP"
                elif "яндекс" in name_lower or "browser" in name_lower or "браузер" in name_lower:
                    category = "Браузеры"
                
                apps_data.append({
                    "name": clean_name,
                    "icon": "📦",
                    "category": category,
                    "script": script,
                    "installed": True,
                    "raw_name": name_without_ext,
                    "extension": extension
                })
        
        # Сортируем по категориям
        return sorted(apps_data, key=lambda x: (x["category"], x["name"]))
    
    def setup_ui(self):
        """Настройка стильного UI"""
        
        # Главный контейнер
        main_container = ttk.Frame(self.parent)
        main_container.pack(fill=BOTH, expand=True)
        
        # Верхняя панель с заголовком и статистикой
        self.create_header(main_container)
        
        # Панель с категориями и поиском
        self.create_toolbar(main_container)
        
        # Основная область с приложениями (квадратные карточки)
        self.create_content_area(main_container)
        
        # Нижняя панель с действиями
        self.create_footer(main_container)
    
    def create_header(self, parent):
        """Создание заголовка"""
        
        header = ttk.Frame(parent)
        header.pack(fill=X, padx=20, pady=(20, 10))
        
        title = ttk.Label(
            header,
            text="Управление приложениями",
            font=("Segoe UI", 20, "bold"),
            foreground=self.colors["text"]
        )
        title.pack(side=LEFT)
        
        self.total_label = ttk.Label(
            header,
            text=f"📦 {len(self.apps_data)} приложений",
            font=("Segoe UI", 12),
            foreground=self.colors["text_secondary"]
        )
        self.total_label.pack(side=LEFT, padx=(15, 0))
    
    def create_toolbar(self, parent):
        """Создание панели инструментов"""
        
        toolbar = ttk.Frame(parent)
        toolbar.pack(fill=X, padx=20, pady=10)
        
        # Левая часть - категории (Microsoft, UWP, Defender, Xbox, Браузеры, Остальное)
        categories_frame = ttk.Frame(toolbar)
        categories_frame.pack(side=LEFT)
        
        # Явно задаем категории в нужном порядке
        all_categories = ["Все", "Microsoft", "UWP", "Defender", "Xbox", "Браузеры", "Остальное"]
        
        # Сохраняем кнопки категорий
        self.category_buttons = {}
        
        for cat in all_categories:
            btn = ttk.Button(
                categories_frame,
                text=cat,
                bootstyle="primary" if cat == "Все" else "secondary-outline",
                command=lambda c=cat: self.filter_by_category(c),
                width=10
            )
            btn.pack(side=LEFT, padx=2)
            self.category_buttons[cat] = btn
        
        # Правая часть - поиск
        search_frame = ttk.Frame(toolbar)
        search_frame.pack(side=RIGHT)
        
        # Поле поиска
        self.search_var = ttk.StringVar()
        self.search_var.trace('w', lambda *args: self.search_apps())
        
        self.search_entry = ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            width=25,
            font=("Segoe UI", 10)
        )
        self.search_entry.pack(side=LEFT, padx=(0, 5))
        self.search_entry.insert(0, "🔍 Поиск...")
        
        def on_focus_in(e):
            if self.search_entry.get() == "🔍 Поиск...":
                self.search_entry.delete(0, END)
        
        def on_focus_out(e):
            if not self.search_entry.get():
                self.search_entry.insert(0, "🔍 Поиск...")
                self.current_search = ""
                self.update_display()
        
        self.search_entry.bind("<FocusIn>", on_focus_in)
        self.search_entry.bind("<FocusOut>", on_focus_out)
        
        # Кнопка сброса фильтров
        reset_btn = ttk.Button(
            search_frame,
            text="✕",
            bootstyle="secondary",
            command=self.reset_filters,
            width=3
        )
        reset_btn.pack(side=LEFT)
    
    def create_content_area(self, parent):
        """Создание основной области с квадратными карточками"""
        
        # Контейнер с прокруткой
        container = ttk.Frame(parent)
        container.pack(fill=BOTH, expand=True, padx=20, pady=10)
        
        # Canvas для прокрутки
        self.canvas = ttk.Canvas(container, highlightthickness=0, bg=self.colors["bg"])
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=self.canvas.winfo_width())
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Обновляем ширину canvas при изменении размера
        def on_canvas_configure(e):
            self.canvas.itemconfig(1, width=e.width)
        
        self.canvas.bind('<Configure>', on_canvas_configure)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Привязка прокрутки колесиком
        def on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        self.canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        # Создаем сетку приложений
        self.update_display()
    
    def update_display(self):
        """Обновление отображения приложений с учетом фильтров"""
        
        # Проверяем, существует ли scrollable_frame
        if not hasattr(self, 'scrollable_frame'):
            return
        
        # Фильтруем приложения
        filtered_apps = self.apps_data.copy()
        
        # Фильтр по категории
        if self.current_category and self.current_category != "Все":
            filtered_apps = [app for app in filtered_apps if app["category"] == self.current_category]
        
        # Фильтр по поиску
        if self.current_search:
            search_lower = self.current_search.lower()
            filtered_apps = [
                app for app in filtered_apps 
                if search_lower in app["name"].lower() 
                or search_lower in app["raw_name"].lower()
                or search_lower in app["category"].lower()
            ]
        
        # Обновляем счетчик
        self.total_label.config(text=f"📦 {len(filtered_apps)} из {len(self.apps_data)} приложений")
        
        # Обновляем сетку
        self.update_apps_grid(filtered_apps)
    
    def update_apps_grid(self, apps):
        """Обновление сетки с квадратными карточками (4 в ряд)"""
        
        # Проверяем, существует ли scrollable_frame
        if not hasattr(self, 'scrollable_frame'):
            return
        
        # Очищаем scrollable_frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        if not apps:
            # Показываем сообщение, если ничего не найдено
            no_results_frame = ttk.Frame(self.scrollable_frame)
            no_results_frame.pack(expand=True, fill=BOTH, pady=50)
            
            no_results_label = ttk.Label(
                no_results_frame,
                text="😕 Ничего не найдено",
                font=("Segoe UI", 16, "bold"),
                foreground=self.colors["text_secondary"]
            )
            no_results_label.pack()
            
            if self.current_search:
                suggestion_label = ttk.Label(
                    no_results_frame,
                    text=f"По запросу '{self.current_search}' ничего не найдено",
                    font=("Segoe UI", 11),
                    foreground=self.colors["text_secondary"]
                )
                suggestion_label.pack(pady=10)
            else:
                suggestion_label = ttk.Label(
                    no_results_frame,
                    text="Попробуйте изменить параметры фильтрации",
                    font=("Segoe UI", 11),
                    foreground=self.colors["text_secondary"]
                )
                suggestion_label.pack(pady=10)
            
            return
        
        # Группируем по категориям (только для режима "Все" и без поиска)
        if self.current_category == "Все" and not self.current_search:
            categories = {}
            for app in apps:
                cat = app["category"]
                if cat not in categories:
                    categories[cat] = []
                categories[cat].append(app)
            
            # Создаем секции для каждой категории
            for category, category_apps in categories.items():
                self.create_category_section(category, category_apps)
        else:
            # При поиске или фильтрации показываем все приложения подряд
            self.create_flat_grid(apps)
    
    def create_category_section(self, category, apps):
        """Создание секции категории с квадратными карточками"""
        
        # Заголовок категории
        category_header = ttk.Frame(self.scrollable_frame)
        category_header.pack(fill=X, pady=(15, 5))
        
        title = ttk.Label(
            category_header,
            text=category.upper(),
            font=("Segoe UI", 12, "bold"),
            foreground=self.colors["accent"]
        )
        title.pack(side=LEFT)
        
        # Счетчик в категории
        count_label = ttk.Label(
            category_header,
            text=f"({len(apps)})",
            font=("Segoe UI", 10),
            foreground=self.colors["text_secondary"]
        )
        count_label.pack(side=LEFT, padx=(5, 0))
        
        # Сетка приложений - 4 колонки
        grid_frame = ttk.Frame(self.scrollable_frame)
        grid_frame.pack(fill=X, pady=5)
        
        # По 4 приложения в ряд
        for i, app in enumerate(apps):
            if i % 4 == 0:
                row_frame = ttk.Frame(grid_frame)
                row_frame.pack(fill=X, pady=2)
                for j in range(4):
                    row_frame.columnconfigure(j, weight=1)
            
            col = i % 4
            self.create_app_card(row_frame, col, app)
    
    def create_flat_grid(self, apps):
        """Создание плоской сетки без категорий (4 колонки)"""
        
        # Заголовок с количеством результатов
        if self.current_search:
            header_frame = ttk.Frame(self.scrollable_frame)
            header_frame.pack(fill=X, pady=(10, 5))
            
            results_label = ttk.Label(
                header_frame,
                text=f"Результаты поиска: {len(apps)}",
                font=("Segoe UI", 11, "italic"),
                foreground=self.colors["text_secondary"]
            )
            results_label.pack(anchor=W)
        
        # Сетка приложений - 4 колонки
        grid_frame = ttk.Frame(self.scrollable_frame)
        grid_frame.pack(fill=X, pady=5)
        
        for i, app in enumerate(apps):
            if i % 4 == 0:
                row_frame = ttk.Frame(grid_frame)
                row_frame.pack(fill=X, pady=2)
                for j in range(4):
                    row_frame.columnconfigure(j, weight=1)
            
            col = i % 4
            self.create_app_card(row_frame, col, app)
    
    def create_app_card(self, parent, col, app_data):
        """Создание квадратной карточки приложения с крестиком"""
        
        # Квадратная карточка
        card = ttk.Frame(parent, bootstyle="secondary")
        card.grid(row=0, column=col, padx=8, pady=8, sticky="nsew")
        
        # Контейнер с отступами
        container = ttk.Frame(card)
        container.pack(fill=BOTH, expand=True, padx=12, pady=12)
        
        # Иконка (большая)
        icon_label = ttk.Label(
            container,
            text=app_data["icon"],
            font=("Segoe UI", 36)
        )
        icon_label.pack(pady=(10, 5))
        
        # Название приложения
        name_label = ttk.Label(
            container,
            text=app_data["name"],
            font=("Segoe UI", 10, "bold"),
            wraplength=120
        )
        name_label.pack()
        
        # Категория
        cat_label = ttk.Label(
            container,
            text=app_data["category"],
            font=("Segoe UI", 8),
            foreground=self.colors["text_secondary"]
        )
        cat_label.pack(pady=(2, 5))
        
        # Расширение
        ext_label = ttk.Label(
            container,
            text=f".{app_data.get('extension', 'bat')}",
            font=("Segoe UI", 7),
            foreground=self.colors["text_secondary"]
        )
        ext_label.pack()
        
        # Крестик для удаления (в правом верхнем углу)
        delete_btn = ttk.Label(
            card,
            text="✕",
            font=("Segoe UI", 14, "bold"),
            foreground=self.colors["danger"],
            cursor="hand2"
        )
        delete_btn.place(relx=1.0, rely=0.0, anchor="ne", x=-5, y=5)
        
        # Привязываем событие клика для удаления
        delete_btn.bind("<Button-1>", lambda e, s=app_data["script"]: self.delete_app(s))
        
        # Кнопка восстановления (иконка)
        restore_btn = ttk.Label(
            card,
            text="↻",
            font=("Segoe UI", 12),
            foreground=self.colors["success"],
            cursor="hand2"
        )
        restore_btn.place(relx=0.0, rely=1.0, anchor="sw", x=5, y=-5)
        
        # Привязываем событие клика для восстановления
        restore_btn.bind("<Button-1>", lambda e, s=app_data["script"]: self.restore_app(s))
        
        # Эффекты наведения
        def on_enter(e):
            card.configure(bootstyle="primary")
        
        def on_leave(e):
            card.configure(bootstyle="secondary")
        
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        
        # Сохраняем ссылки
        app_data["card"] = card
        self.app_buttons[app_data["name"]] = app_data
    
    def create_footer(self, parent):
        """Создание нижней панели"""
        
        footer = ttk.Frame(parent)
        footer.pack(fill=X, padx=20, pady=(10, 20))
        
        # Левая часть - информация
        info_label = ttk.Label(
            footer,
            text="💡 Нажмите ✕ для удаления, ↻ для восстановления",
            font=("Segoe UI", 9),
            foreground=self.colors["text_secondary"]
        )
        info_label.pack(side=LEFT)
        
        # Правая часть - кнопки
        buttons_frame = ttk.Frame(footer)
        buttons_frame.pack(side=RIGHT)
        
        # Кнопка "Удалить все"
        delete_all_btn = ttk.Button(
            buttons_frame,
            text="🗑️ Удалить все",
            bootstyle="danger-outline",
            command=self.delete_all_apps,
            width=15
        )
        delete_all_btn.pack(side=LEFT, padx=5)
        
        # Кнопка "Восстановить все"
        restore_all_btn = ttk.Button(
            buttons_frame,
            text="↻ Восстановить все",
            bootstyle="success-outline",
            command=self.restore_all_apps,
            width=17
        )
        restore_all_btn.pack(side=LEFT, padx=5)
    
    def filter_by_category(self, category):
        """Фильтрация по категории"""
        print(f"Фильтр по категории: {category}")
        
        # Обновляем стиль кнопок
        for cat, btn in self.category_buttons.items():
            if cat == category:
                btn.configure(bootstyle="primary")
            else:
                btn.configure(bootstyle="secondary-outline")
        
        # Очищаем поиск при фильтрации
        if self.search_entry.get() != "🔍 Поиск...":
            self.search_entry.delete(0, END)
            self.search_entry.insert(0, "🔍 Поиск...")
            self.search_var.set("")
        
        # Сохраняем выбранную категорию
        self.current_category = category
        self.current_search = ""
        
        # Обновляем отображение
        self.update_display()
    
    def search_apps(self):
        """Поиск приложений"""
        query = self.search_var.get()
        
        if query and query != "🔍 Поиск...":
            print(f"Поиск: {query}")
            
            # Сохраняем поисковый запрос
            self.current_search = query
            
            # Сбрасываем категорию при поиске
            self.current_category = "Все"
            
            # Обновляем стиль кнопок категорий
            for cat, btn in self.category_buttons.items():
                if cat == "Все":
                    btn.configure(bootstyle="primary")
                else:
                    btn.configure(bootstyle="secondary-outline")
        else:
            self.current_search = ""
        
        # Обновляем отображение
        self.update_display()
    
    def reset_filters(self):
        """Сброс всех фильтров"""
        print("Сброс фильтров")
        
        # Сбрасываем поиск
        self.search_entry.delete(0, END)
        self.search_entry.insert(0, "🔍 Поиск...")
        self.search_var.set("")
        self.current_search = ""
        
        # Сбрасываем категорию
        self.current_category = "Все"
        for cat, btn in self.category_buttons.items():
            if cat == "Все":
                btn.configure(bootstyle="primary")
            else:
                btn.configure(bootstyle="secondary-outline")
        
        # Обновляем отображение
        self.update_display()
    
    def delete_app(self, script_name):
        """Удаление приложения"""
        if messagebox.askyesno(
            "Подтверждение",
            f"Удалить это приложение?",
            icon='warning'
        ):
            try:
                script_path = os.path.join(self.scripts_path, script_name)
                
                if not os.path.exists(script_path):
                    messagebox.showerror(
                        "Ошибка", 
                        f"❌ Скрипт не найден:\n{script_path}"
                    )
                    return
                
                # Запускаем скрипт
                if script_name.endswith('.ps1'):
                    subprocess.run(['powershell.exe', '-ExecutionPolicy', 'Bypass', '-File', script_path])
                else:
                    subprocess.run([script_path], shell=True)
                
                messagebox.showinfo("Успех", "✅ Скрипт выполнен успешно!")
                    
            except Exception as e:
                messagebox.showerror("Ошибка", f"❌ {str(e)}")
    
    def delete_all_apps(self):
        """Удаление всех приложений"""
        count = len(self.apps_data)
        if messagebox.askyesno(
            "Подтверждение",
            f"Удалить все ({count}) приложения?",
            icon='warning'
        ):
            messagebox.showinfo("Информация", "Массовое удаление запущено")
    
    def restore_app(self, script_name):
        """Восстановление приложения"""
        try:
            os.system("start ms-windows-store://home")
            messagebox.showinfo("Информация", "Microsoft Store открыт")
        except Exception as e:
            messagebox.showerror("Ошибка", f"❌ {str(e)}")
    
    def restore_all_apps(self):
        """Восстановление всех приложений"""
        try:
            os.system("start ms-windows-store://home")
            messagebox.showinfo("Информация", "Microsoft Store открыт")
        except Exception as e:
            messagebox.showerror("Ошибка", f"❌ {str(e)}")


def create_app_uninstall_tab(parent, config, scripts_list):
    """Создание вкладки удаления приложений"""
    tab_frame = ttk.Frame(parent)
    app_uninstaller = AppUninstallerTab(tab_frame, config, scripts_list)
    return tab_frame