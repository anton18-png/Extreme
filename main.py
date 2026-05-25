# Импортируем необходимые модули
import os  # Модуль для работы с файловой системой, например, для создания директорий
import tkinter as tk  # Основной модуль для работы с графическим интерфейсом
from tkinter import ttk  # Расширение Tkinter для более красивых виджетов
from tkinter import filedialog  # Модуль для диалогов выбора файлов
import ttkbootstrap as ttk  # Дополнительное оформление для Tkinter, предоставляет стили и темы
import subprocess  # Модуль для выполнения внешних процессов, используется для выполнения скриптов
import getpass  # Модуль для работы с именами пользователей, хотя здесь явно не используется
from datetime import (
    datetime,
)  # Модуль для работы с датой и временем, используется для создания уникальных имен файлов
import configparser  # Модуль для работы с конфигурационными файлами, здесь для чтения и записи настроек
import json  # Для работы с JSON файлами
import shutil  # Для копирования файлов
from telemetry.logger import Logger  # Импортируем класс Logger
import tkinter.messagebox as messagebox  # Добавляем модуль для вывода сообщений
# from gpt import GPTClient  # Импортируем GPTClient
from pathlib import Path
# from windows_vote import WindowsVoteWindow
# from services_manager import create_services_tab
import random
import hashlib  # Для вычисления хэшей файлов
import threading  # Для неблокирующей проверки обновлений
import webbrowser

# Получаем имя текущего пользователя системы
username = getpass.getuser()

# Очищаем имя пользователя от недопустимых символов для имени файла
# Заменяем проблемные символы на подчеркивание
invalid_chars = '<>:"/\\|?*'
clean_username = ''.join('_' if c in invalid_chars else c for c in username)

# при вероятности 5% открываем рекламу
def open_random_site(numder_open_random_site):
    pass

# Версия программы
version = "v4 Beta"

# Импортируем путь для доступа к модулям
# Этот код добавляет папку tweaks в путь поиска модулей, чтобы импортировать скрипты из этой директории
import sys  # Импортируем модуль sys для работы с системными функциями

sys.path.insert(
    0, "./tweaks"
)  # Добавляем папку tweaks в путь поиска модулей, чтобы импортировать скрипты из этой директории

# Импортируем пользовательские вкладки
from tabs_beta import (
    tabs_main,
    tabs,
    tabs_1,
    tabs_2,
    tabs_3,
    tabs_4,
    tabs_5,
    tabs_6,
    tabs_update,
)  # Импортируем вкладки из модуля tabs_beta

# Импортируем tabs_mini для минималистичной вкладки
try:
    from tweaks.tabs_beta import tabs_mini
except ImportError:
    tabs_mini = {}

# Импортируем безопасные твики для режима новичка
try:
    from tweaks.tabs_novice import (
        tabs_main as tabs_main_novice,
        tabs as tabs_novice,
        tabs_4 as tabs_4_novice,
        tabs_6 as tabs_6_novice,
    )
except ImportError:
    # Если файл не найден, используем пустые словари
    tabs_main_novice = {}
    tabs_novice = {}
    tabs_4_novice = {}
    tabs_6_novice = {}

# Создаем папку user_data, если она не существует
os.makedirs(
    "user_data", exist_ok=True
)  # Создаем папку user_data, если она не существует
os.makedirs(
    "user_data//Configs", exist_ok=True
)  # Создаем папку Configs, если она не существует

# Инициализация логгера
logger = Logger()  # Инициализация логгера

# Инициализация конфигурации ДО создания окна
# Этот код инициализирует конфигурацию, которая хранит настройки программы
config = configparser.ConfigParser()  # Инициализация конфигурации
config.read("user_data//settings.ini", encoding="cp1251")  # Чтение в ANSI

# Создаем обязательные секции с настройками по умолчанию
required_sections = {
    "General": {
        "theme": "boosterxvapor",   # Тема интерфейса
        "font_family": "Terminal",  # Шрифт интерфейса
        "font_size": "12",  # Размер шрифта интерфейса
        "checkbox_font_size": "12",  # Размер шрифта чекбоксов
        "quick_button_font_size": "16",  # Размер шрифта кнопок быстрого доступа
        "tooltips_enabled": "True",  # Включение всплывающих подсказок
        "checkbox_display_mode": "rectangle",  # Режим отображения чекбоксов: regular, rectangle или wide
        "first_run_completed": "False",  # Флаг первого запуска
        "ad_enabled": "False",  # Включение рекламы
        "offer_backup_enabled": "False",  # Предложение создания бэкапа
        "confirm_switch_tab_enabled": "False",  # Подтверждение переключения вкладок
        "developer_mode": "True",  # Режим разработчика
        "novice_mode": "False",  # Режим новичка
        "initial_tab": "switch_to_main", # Вкладка по умолчанию
        "show_top_panel": "True",  # Показывать верхнее меню
        "show_sidebar": "True",  # Показывать боковое меню
        "tweak_execution_mode": "default",  # Способ запуска твиков: default, no_launcher, launcher, powerrun, cmd, create_config_and_run
        "auto_update_enabled": "False",  # Включение автообновления
        "frames_instead_of_tabs": "True",  # Фреймы вместо вкладок
        "show_checkbox_full_path": "True",  # Показывать полный путь чекбоксов (True) или только имя файла (False)
    },
    "Window": {"fullscreen": "True"},  # Полноэкранный режим
    "Columns": {"default": "3"},  # Количество колонок в окне
    "Telemetry": {
        "send_on_close": "False",  # Отправка логов при закрытии программы
        "share_telemetry": "False",  # Обмен телеметрией с другими пользователями
    },
}

# Этот код проверяет, есть ли секция в конфигурации и если нет, то добавляет её
config_changed = False  # Отслеживаем изменения конфигурации
for (
    section,
    options,
) in required_sections.items():  # Проверяем, есть ли секция в конфигурации
    if not config.has_section(section):  # Если секции нет, то добавляем её
        config.add_section(section)  # Добавляем секцию
        config_changed = True  # Конфиг изменился
    for key, value in options.items():  # Проверяем, есть ли ключ в секции
        if not config.has_option(section, key):  # Если ключа нет, то добавляем его
            config[section][key] = value  # Добавляем ключ и значение
            config_changed = True  # Конфиг изменился

# Сохраняем обновленный конфиг только если были изменения
if config_changed:
    with open(
        "user_data//settings.ini", "w", encoding="cp1251"
    ) as configfile:  # Запись в ANSI
        config.write(configfile)  # Записываем конфигурацию в файл

# Функция для получения шрифта больших меток (определена раньше, чтобы быть доступной в show_license_window)
def get_large_label_font():
    """Возвращает шрифт для больших меток"""
    try:
        font_family = current_font[0]
        base_size = current_font[1]
    except (NameError, IndexError):
        # Если current_font еще не определен, используем значения из config
        font_family = config.get("General", "font_family", fallback="Segoe UI")
        base_size = int(config.get("General", "font_size", fallback="12"))
    large_size = max(11, int(base_size * 1.2))  # Минимум 11, примерно в 1.2 раза больше базового
    return (font_family, large_size, "bold")

# Функция для показа лицензионного окна
def show_license_window():
    """Показывает лицензионное окно при первом запуске"""
    license_window = ttk.Toplevel(root)
    license_window.title("Лицензионное соглашение - Extreme Tweaker")
    license_window.geometry("900x700")
    license_window.resizable(False, False)
    license_window.transient(root)
    license_window.grab_set()
    
    # Центрируем окно
    license_window.update_idletasks()
    x = (license_window.winfo_screenwidth() // 2) - (900 // 2)
    y = (license_window.winfo_screenheight() // 2) - (700 // 2)
    license_window.geometry(f"900x700+{x}+{y}")
    
    # Основной контейнер
    main_frame = ttk.Frame(license_window, padding=20)
    main_frame.pack(fill="both", expand=True)
    
    # Заголовок
    title_label = ttk.Label(
        main_frame,
        text="Лицензионное соглашение",
        font=get_large_label_font()
    )
    title_label.pack(pady=(0, 15))
    
    # Текст лицензии в скроллируемом виджете
    license_text_frame = ttk.Frame(main_frame)
    license_text_frame.pack(fill="both", expand=True, pady=(0, 15))
    
    # Получаем шрифт из конфигурации (current_font может быть еще не определен)
    try:
        license_font = current_font
    except NameError:
        license_font = (
            config.get("General", "font_family", fallback="Segoe UI"),
            int(config.get("General", "font_size", fallback="12"))
        )
    
    license_text = tk.Text(
        license_text_frame,
        wrap=tk.WORD,
        font=license_font,
        padx=15,
        pady=15,
        relief="flat",
        borderwidth=1
    )
    license_text.pack(side="left", fill="both", expand=True)
    
    scrollbar = ttk.Scrollbar(license_text_frame, orient="vertical", command=license_text.yview)
    scrollbar.pack(side="right", fill="y")
    license_text.configure(yscrollcommand=scrollbar.set)
    
    license_content = """
ДАННОЕ ПРОГРАММНОЕ ОБЕСПЕЧЕНИЕ ПРЕДОСТАВЛЯЕТСЯ «КАК ЕСТЬ», БЕЗ КАКИХ-ЛИБО ГАРАНТИЙ, ЯВНО ВЫРАЖЕННЫХ ИЛИ ПОДРАЗУМЕВАЕМЫХ, ВКЛЮЧАЯ ГАРАНТИИ ТОВАРНОЙ ПРИГОДНОСТИ, СООТВЕТСТВИЯ ПО ЕГО КОНКРЕТНОМУ НАЗНАЧЕНИЮ И ОТСУТСТВИЯ НАРУШЕНИЙ, НО НЕ ОГРАНИЧИВАЯСЬ ИМИ. НИ В КАКОМ СЛУЧАЕ АВТОРЫ ИЛИ ПРАВООБЛАДАТЕЛИ НЕ НЕСУТ ОТВЕТСТВЕННОСТИ ПО КАКИМ-ЛИБО ИСКАМ, ЗА УЩЕРБ ИЛИ ПО ИНЫМ ТРЕБОВАНИЯМ, В ТОМ ЧИСЛЕ, ПРИ ДЕЙСТВИИ КОНТРАКТА, ДЕЛИКТЕ ИЛИ ИНОЙ СИТУАЦИИ, ВОЗНИКШИМ ИЗ-ЗА ИСПОЛЬЗОВАНИЯ ПРОГРАММНОГО ОБЕСПЕЧЕНИЯ ИЛИ ИНЫХ ДЕЙСТВИЙ С ПРОГРАММНЫМ ОБЕСПЕЧЕНИЕМ.

🎯 Extreme Tweaker: почему его стоит попробовать (честный обзор)

Ребята, давайте без прикрас. Extreme - это не волшебная таблетка, а инструмент. Как и любой мощный инструмент, он требует понимания что и зачем вы делаете.

Что это такое?

Extreme - это база, которая позволяет внести в систему огромное количество глобальных твиков. Не просто "ускорить ПК", а точечно настроить под себя:

Честно о преимуществах:

✅ Открытый исходный код - в отличие от многих популярных твикеров, вы всегда можете посмотреть КОНКРЕТНО какие изменения вносятся в реестр и систему. Никаких скрытых действий!

✅ Признание экспертов - некоторые наши твики используют такие известные в мире оптимизации личности как Igromanoff и DE3NAKE. Они проверяли, тестировали и используют наши твики в настройке ПК.

✅ Универсальность - собраны лучшие твики из Hone, BoosterX и других проектов. Один инструмент вместо десятка.

✅ Для слабых ПК - реально помогает дать вторую жизнь старому железу за счет удаления всего лишнего.

Горькая правда (предупреждаем!):

⚠️ Риск есть всегда - даже на оригинальных сборках Windows твики могут работать непредсказуемо. Все зависит от вашего конкретного железа, драйверов и сборки.

⚠️ Не для всех - некоторые пользователи называют Extreme лучшим твикером, другие - худшим. Все индивидуально!

⚠️ Может ухудшить - на некоторых конфигурациях чрезмерная оптимизация приводит к нестабильности системы. Начинайте с базовых пресетов!

⚠️ Требует знаний - это не "нажал одну кнопку и все работает". Нужно понимать что вы отключаете и зачем.

Для кого это?

💻 Геймеры - хотите максимум FPS и минимум лагов

🔧 Энтузиасты - любите копаться в настройках

🚀 Владельцы слабых ПК - нужно выжать максимум из старого железа

🔒 Любителей приватности - цените конфиденциальность

Итог: Extreme - это мощный, но требовательный инструмент. Если вы готовы разбираться и принимать осознанные решения - он может кардинально улучшить ваш опыт использования Windows. Если ищете "волшебную кнопку" - возможно, это не ваш выбор.

Попробуйте, но если вы новичок в сфере оптимизации - начинайте с малого! 💾

Почему антивирусы ругаются на твикер? Честное объяснение

🛡 Вопрос от сообщества: "Почему антивирусы блокируют Extreme Tweaker?"

Давайте разберемся честно и без технических сложностей!

❌ Являются ли наши твики вирусами?

Однозначно НЕТ. Но понимаем ваше беспокойство - давайте объясним, что происходит.

🤔 Почему антивирусы "ругаются"?

Как мы упоминали в прошлом посте - наш твикер изменяет системные настройки, что вызывает подозрения. Но есть и техническая причина:

🔧 PyInstaller - наш способ сборки

Extreme Tweaker компилируется через PyInstaller - стандартный инструмент для создания исполняемых файлов из Python-кода. И вот что антивирусам не нравится:

- Распаковка во временные каталоги - PyInstaller временно распаковывает код при запуске

- Использование Python-интерпретатора - часто используется вредоносным ПО

- Отсутствие цифровой подписи - мы пока не можем позволить дорогой сертификат

- "Неизвестный" файл - новый софт без репутации вызывает подозрения

💡 Почему мы не "исправляем" это:

Чтобы убрать ложные срабатывания, нам придется:

- Убрать половину функций твикера

- Отказаться от PyInstaller и глубокой оптимизации

- Пожертвовать производительностью ради "спокойствия" антивирусов

Мы не готовы на такие компромиссы! 🚫

🔒 Наша позиция:

📜 Открытый исходный код - вы всегда можете посмотреть, что делает каждая функция

🎯 Честная работа - мы не добавляем трояны, майнеры или шпионские модули (нам лень)

🔍 Проверяйте сами - используйте VirusTotal, смотрите вкладку "Поведение"

📞 Открытость - задавайте вопросы, мы всегда на связи

Ложные срабатывания - это неизбежная плата за использование современных инструментов сборки и глубокой оптимизации системы! 🔧

Extreme Tweaker: Правда об оптимизации Windows

Давайте без иллюзий. Современное железо и оптимизация — что на самом деле работает?

Реальность такова:

- На современном железе обычные твикеры дают прирост в пределах погрешности (±2-3%)

- На слабых ПК можно выжать 10-15%, иногда больше

- За всё нужно платить — теряешь некоторые, а то и большинство функций

Что предлагаем мы:

Extreme Tweaker не волшебная таблетка. Это инструмент, который:

- Может дать реальный прирост даже на RTX 4090 + i9

- Но придется отказаться от части функционала Windows

- И система будет заточена не под универсальность, а под игры, и то не все

К примеру:

- Базовая оптимизация уже закрывает доступ к Forza Horizon

- Зато Need For Speed начинает летать

- Valorant может как ускориться, так и перестать работать

Золотая середина:

В Extreme Tweaker можно найти баланс:

- ✅ Увеличение FPS

- ✅ Исчезновение input lag

- ✅ Нормальная работоспособность Windows

- ⚠️ Частичная потеря функционала Windows

Выбор за вами:

- Максимальный FPS ценой совместимости

- Баланс производительности и функциональности

- Стандартная настройка без рисков

Extreme Tweaker даёт все три варианта. Используйте то, что подходит именно вам.

Никаких сказок про +50% FPS. Только реальные цифры и честные компромиссы.
"""
    
    license_text.insert("1.0", license_content)
    license_text.config(state="disabled")
    
    # Фрейм с кнопками
    buttons_frame = ttk.Frame(main_frame)
    buttons_frame.pack(fill="x")
    
    def accept_license():
        license_window.destroy()
        # Открываем Telegram канал после принятия лицензии
        try:
            import webbrowser
            webbrowser.open("https://t.me/all_tweaker")
        except Exception as e:
            logger.log_error(f"Ошибка при открытии Telegram канала: {str(e)}")
    
    accept_button = ttk.Button(
        buttons_frame,
        text="Принимаю условия",
        bootstyle="success",
        command=accept_license,
        width=20
    )
    accept_button.pack(side="right", padx=(10, 0))
    
    decline_button = ttk.Button(
        buttons_frame,
        text="Отклонить",
        bootstyle="danger",
        command=lambda: root.quit(),
        width=20
    )
    decline_button.pack(side="right")
    
    # Ждем закрытия окна
    license_window.wait_window()

# Проверяем, был ли первый запуск
first_run_completed = config.getboolean("General", "first_run_completed", fallback=False)

# Теперь создаем корневое окно
root = ttk.Window(themename=config["General"]["theme"])  # Создаем корневое окно
root.title(f"Extreme Tweaker {version} by Anton18-PNG")  # Заголовок окна
root.attributes(
    "-fullscreen", config.getboolean("Window", "fullscreen")
)  # Полноэкранный режим
root.geometry("1280x720")  # Размер окна

# Показываем лицензионное окно при первом запуске
if not first_run_completed:
    # show_license_window()
    # # Устанавливаем флаг, что первый запуск завершен
    # config["General"]["first_run_completed"] = "True"
    # with open("user_data//settings.ini", "w", encoding="cp1251") as configfile:
    #     config.write(configfile)
    pass

# Импортируем обработчик ошибок
from telemetry.error_handler import (
    handle_top_level_error,
)  # Импортируем обработчик ошибок

# Устанавливаем обработчик необработанных исключений
sys.excepthook = (
    lambda *args: handle_top_level_error()
)  # Устанавливаем обработчик необработанных исключений


def reload_program(event=None):
    root.destroy()
    import sys
    import subprocess

    subprocess.run([sys.executable] + sys.argv)


"""
+------------------------------------+
| Функция для проверки обновлений    |
+------------------------------------+
"""


def calculate_file_hash(file_path):
    """Вычисляет SHA256 хэш файла"""
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            # Читаем файл по частям для экономии памяти
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Ошибка при вычислении хэша файла {file_path}: {e}")
        return None


def check_for_updates():
    """Проверяет наличие обновлений и запускает их установку"""
    try:
        # Проверяем, включено ли автообновление
        if not config.getboolean("General", "auto_update_enabled", fallback=True):
            print("Автообновление отключено в настройках")
            return
        
        # Пути к файлам
        # local_file = r"C:\Apps\Extreme\SetupWinterWizardPro.exe"
        local_file = r"C:\Apps\Extreme\SetupWinterWizard.exe"
        # github_url = "https://github.com/anton18-png/Extreme/raw/refs/heads/main/SetupWinterWizardPro.exe"
        github_url = "https://github.com/anton18-png/Extreme/raw/refs/heads/main/SetupWinterWizard.exe"
        temp_file = os.path.join(os.environ.get("TEMP", "."), "SetupWinterWizard_temp.exe")
        
        # Вычисляем хэш локального файла
        local_hash = None
        if os.path.exists(local_file):
            local_hash = calculate_file_hash(local_file)
            print(f"Локальный хэш SetupWinterWizard.exe: {local_hash}")
        else:
            print(f"Локальный файл {local_file} не найден")
        
        # Скачиваем файл с GitHub во временную папку с помощью curl
        # print("Проверка обновлений: скачивание файла с GitHub...")
        try:
            # Используем curl для скачивания файла
            curl_command = [
                "curl",
                "-g",
                "-k",
                "-L",
                "-#",
                "-o",
                temp_file,
                github_url
            ]
            result = subprocess.run(curl_command, capture_output=True, text=True, timeout=60)
            if result.returncode != 0:
                print(f"Ошибка при скачивании файла с GitHub: {result.stderr}")
                return
            # print("Файл успешно скачан")
        except subprocess.TimeoutExpired:
            print("Превышено время ожидания при скачивании файла")
            return
        except FileNotFoundError:
            print("curl не найден в системе. Автообновление недоступно.")
            return
        except Exception as e:
            print(f"Ошибка при скачивании файла с GitHub: {e}")
            return
        
        # Вычисляем хэш скачанного файла
        github_hash = calculate_file_hash(temp_file)
        print(f"Хэш файла с GitHub: {github_hash}")
        
        # Сравниваем хэши
        if github_hash and github_hash != local_hash:
            print("Обнаружено обновление! Запуск установки...")
            
            # Скачиваем файл в нужное место с помощью curl
            try:
                # Создаем директорию, если её нет
                os.makedirs(os.path.dirname(local_file), exist_ok=True)
                
                # Скачиваем файл напрямую в нужное место с помощью curl
                curl_command = [
                    "curl",
                    "-g",
                    "-k",
                    "-L",
                    "-#",
                    "-o",
                    local_file,
                    github_url
                ]
                result = subprocess.run(curl_command, capture_output=True, text=True, timeout=60)
                if result.returncode != 0:
                    print(f"Ошибка при скачивании обновления: {result.stderr}")
                    return
                
                print(f"Файл обновления сохранен: {local_file}")
                
                # Удаляем временный файл
                try:
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                except:
                    pass
                
                # Закрываем программу
                print("Закрытие программы для установки обновления...")
                
                # Запускаем установщик в отдельном процессе с флагом -ppass
                subprocess.Popen([local_file, "-ppass"], shell=True)
                
                # Закрываем текущую программу через главный поток
                def close_and_kill():
                    try:
                        subprocess.run(["taskkill", "/im", "Extreme.exe", "/f"], 
                                      capture_output=True, timeout=5)
                    except:
                        pass
                    root.destroy()
                
                root.after(500, close_and_kill)
                
            except Exception as e:
                print(f"Ошибка при установке обновления: {e}")
        else:
            print("Обновления не найдены. Программа актуальна.")
            # Удаляем временный файл
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except:
                pass
                
    except Exception as e:
        print(f"Ошибка при проверке обновлений: {e}")


def check_for_updates_threaded():
    """Запускает проверку обновлений в отдельном потоке"""
    thread = threading.Thread(target=check_for_updates, daemon=True)
    thread.start()


# Функции для экспорта/импорта настроек
def export_settings():  # Функция для экспорта настроек
    try:  # Пробуем выполнить код
        # Создаем директорию для экспорта если её нет
        os.makedirs(
            "user_data//Configs/Exports", exist_ok=True
        )  # Создаем директорию для экспорта если её нет

        # Генерируем имя файла с текущей датой
        timestamp = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )  # Генерируем имя файла с текущей датой
        default_filename = (
            f"All_Tweaker_Settings_{timestamp}.json"  # Имя файла по умолчанию
        )

        # Открываем диалог сохранения файла
        filename = filedialog.asksaveasfilename(
            initialdir="user_data//Configs/Exports",  # Директория по умолчанию
            initialfile=default_filename,  # Имя файла по умолчанию
            defaultextension=".json",  # Расширение файла по умолчанию
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],  # Типы файлов
        )

        if filename:
            # Создаем словарь с настройками
            settings_dict = {}  # Создаем словарь с настройками
            for section in config.sections():  # Проходим по всем секциям конфигурации
                settings_dict[section] = dict(
                    config[section]
                )  # Добавляем секцию и её настройки в словарь

            # Сохраняем настройки в JSON файл
            with open(
                filename, "w", encoding="utf-8"
            ) as f:  # Открываем файл для записи
                json.dump(
                    settings_dict, f, indent=4, ensure_ascii=False
                )  # Записываем настройки в файл

            # Копируем файлы конфигурации если они есть
            if os.path.exists(
                "user_data//Configs"
            ):  # Проверяем, есть ли директория Configs
                config_files = [
                    f for f in os.listdir("user_data//Configs") if f.endswith(".bat")
                ]  # Получаем все файлы с расширением .bat
                if config_files:  # Если есть файлы с расширением .bat
                    config_dir = (
                        os.path.splitext(filename)[0] + "_configs"
                    )  # Создаем директорию для файлов конфигурации
                    os.makedirs(
                        config_dir, exist_ok=True
                    )  # Создаем директорию для файлов конфигурации
                    for (
                        file
                    ) in config_files:  # Проходим по всем файлам с расширением .bat
                        shutil.copy2(
                            os.path.join("Configs", file), config_dir
                        )  # Копируем файлы конфигурации в директорию для файлов конфигурации

            print(
                "🎉 Настройки успешно экспортированы в", filename
            )  # Выводим сообщение о успешном экспорте настроек
            return True  # Возвращаем True
    except Exception as e:  # Если возникает ошибка
        print(
            f"❌ Ошибка при экспорте настроек: {str(e)}"
        )  # Выводим сообщение об ошибке
        return False  # Возвращаем False


def import_settings():  # Функция для импорта настроек
    try:  # Пробуем выполнить код
        # Открываем диалог выбора файла
        filename = filedialog.askopenfilename(
            initialdir="Configs/Exports",  # Директория по умолчанию
            title="Выберите файл настроек",  # Заголовок диалога
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],  # Типы файлов
        )

        if filename:
            # Читаем настройки из JSON файла
            with open(
                filename, "r", encoding="utf-8"
            ) as f:  # Открываем файл для чтения
                imported_settings = json.load(f)  # Загружаем настройки из JSON файла

            # Проверяем обязательные секции
            for (
                section,
                options,
            ) in (
                required_sections.items()
            ):  # Проходим по всем секциям в required_sections
                if (
                    section not in imported_settings
                ):  # Если секция не найдена в imported_settings
                    imported_settings[section] = (
                        options  # Добавляем секцию и её настройки в imported_settings
                    )
                else:
                    for (
                        key,
                        value,
                    ) in options.items():  # Проходим по всем ключам в options
                        if (
                            key not in imported_settings[section]
                        ):  # Если ключ не найден в imported_settings[section]
                            imported_settings[section][key] = (
                                value  # Добавляем ключ и его значение в imported_settings[section]
                            )

            # Обновляем конфигурацию
            for (
                section
            ) in imported_settings:  # Проходим по всем секциям в imported_settings
                if not config.has_section(section):  # Если секция не найдена в config
                    config.add_section(section)  # Добавляем секцию в config
                for key, value in imported_settings[
                    section
                ].items():  # Проходим по всем ключам в imported_settings[section]
                    config[section][key] = str(
                        value
                    )  # Добавляем ключ и его значение в config[section]

            # Сохраняем обновленную конфигурацию
            with open(
                "user_data//settings.ini", "w", encoding="utf-8"
            ) as configfile:  # Открываем файл для записи
                config.write(configfile)  # Записываем конфигурацию в файл

            # Импортируем файлы конфигурации если они есть
            config_dir = (
                os.path.splitext(filename)[0] + "_configs"
            )  # Создаем директорию для файлов конфигурации
            if os.path.exists(
                config_dir
            ):  # Проверяем, есть ли директория для файлов конфигурации
                os.makedirs(
                    "Configs", exist_ok=True
                )  # Создаем директорию для файлов конфигурации
                for file in os.listdir(
                    config_dir
                ):  # Проходим по всем файлам в директории для файлов конфигурации
                    if file.endswith(".bat"):  # Если файл имеет расширение .bat
                        shutil.copy2(
                            os.path.join(config_dir, file), "Configs"
                        )  # Копируем файлы конфигурации в директорию для файлов конфигурации

            # Перечитываем настройки
            config.read(
                "user_data//settings.ini", encoding="utf-8"
            )  # Читаем настройки из файла

            # Обновляем интерфейс
            update_theme()  # Обновляем тему интерфейса
            update_font()  # Обновляем шрифт интерфейса
            update_tooltip_state()  # Обновляем состояние всплывающих подсказок

            messagebox.showinfo(
                "✅ Успех", "🎉 Настройки успешно импортированы"
            )  # Выводим сообщение о успешном импорте настроек
            return True  # Возвращаем True
    except Exception as e:  # Если возникает ошибка
        messagebox.showerror(
            "❌ Ошибка", f"❌ Ошибка при импорте настроек: {str(e)}"
        )  # Выводим сообщение об ошибке
        return False  # Возвращаем False


# Инициализируем глобальную переменную для управления состоянием всплывающих подсказок
tooltips_enabled = True  # Состояние всплывающих подсказок

# В секции инициализации переменных добавить
fullscreen_var = tk.StringVar(
    value="Включено" if config.getboolean("Window", "fullscreen") else "Выключено"
)  # Состояние полноэкранного режима

# Словарь для сопоставления имен функций с пользовательскими названиями
function_to_tab_mapping = {
    "switch_to_minimal": "Минимальный вид",  # Имя функции для переключения на минималистичную вкладку
    "switch_to_main": "Главная",  # Имя функции для переключения на главную вкладку
    "switch_to_optimization": "Оптимизация",  # Имя функции для переключения на вкладку оптимизации
    "switch_to_drivers": "Драйверы",  # Имя функции для переключения на вкладку драйверов
    "switch_to_power": "Электропитание",  # Имя функции для переключения на вкладку электропитания
    "switch_to_clean": "Очистка",  # Имя функции для переключения на вкладку очистки
    "switch_to_other": "Другое",  # Имя функции для переключения на вкладку другое
    "switch_to_fixes": "Исправления",  # Имя функции для переключения на вкладку исправлений
    "switch_to_settings": "Настройки",  # Имя функции для переключения на вкладку настроек
}

# Словарь с описаниями вкладок
tab_descriptions = {
    "switch_to_minimal": "Минималистичный интерфейс с упрощенной навигацией",
    "switch_to_main": "Главная страница с конфигурациями и быстрым доступом",
    "switch_to_optimization": "Оптимизация системы для повышения производительности",
    "switch_to_drivers": "Управление драйверами устройств (ОПАСНО: может повредить оборудование)",
    "switch_to_power": "Настройки электропитания и энергосбережения",
    "switch_to_clean": "Очистка системы от временных файлов и мусора",
    "switch_to_other": "Дополнительные настройки и инструменты",
    "switch_to_fixes": "Исправление ошибок и проблем Windows",
    "switch_to_settings": "Настройки программы и параметры интерфейса",
}

# В секции инициализации переменных добавить
initial_tab_var = tk.StringVar(
    value=function_to_tab_mapping.get(
        config.get("General", "initial_tab", fallback="switch_to_main"), "Главная"
    )
)  # Имя функции для переключения на главную вкладку

"""
+------------------------------------+
| Функция для обновления цветовой    |
| схемы интерфейса                   |
+------------------------------------+
"""


def update_colors():  # Функция для обновления цветовой схемы интерфейса
    try:  # Пробуем выполнить код
        with open(
            "user_data//settings.ini", "w", encoding="cp1251"
        ) as configfile:  # Открываем файл для записи
            config.write(configfile)  # Записываем конфигурацию в файл
        root.update()  # Обновляем интерфейс
    except Exception as e:  # Если возникает ошибка
        logger.log_error(
            "❌ Ошибка при обновлении цветов", exc_info=e
        )  # Выводим сообщение об ошибке


"""
+------------------------------------+
| Функция для получения имени кнопки |
| на основе имени вкладки            |
+------------------------------------+
"""


def get_button_name(
    tab_name,
):  # Функция для получения имени кнопки на основе имени вкладки
    """
    Функция для получения имени кнопки на основе имени вкладки.

    Эта функция выполняет следующие действия:
    1. Проверяет, в каком словаре вкладок находится tab_name
    2. Возвращает соответствующее имя кнопки

    Параметры:
    ----------
    tab_name : str
        Имя вкладки, для которой нужно получить имя кнопки

    Возвращает:
    -----------
    str
        Имя кнопки, соответствующее вкладке

    Пример использования:
    --------------------
    button_name = get_button_name("Оптимизация")  # Вернет "Оптимизация"

    Примечания:
    ----------
    - tabs_main - словарь с главными вкладками
    - tabs - словарь с вкладками оптимизации
    - tabs_1 - словарь с вкладками драйверов
    - tabs_2 - словарь с вкладками электропитания
    - tabs_3 - словарь с вкладками исправлений
    - tabs_4 - словарь с вкладками очистки
    - tabs_5 - словарь с другими вкладками
    - tabs_6 - словарь с вкладками настроек
    """
    # Проверяем, есть ли вкладка в словаре главных вкладок
    if tab_name in tabs_main:  # Если вкладка находится в словаре главных вкладок
        # Возвращаем имя кнопки для главных вкладок
        return "Главная"  # Возвращаем имя кнопки для главных вкладок
    # Проверяем, есть ли вкладка в словаре вкладок оптимизации
    elif tab_name in tabs:  # Если вкладка находится в словаре вкладок оптимизации
        # Возвращаем имя кнопки для вкладок оптимизации
        return "Оптимизация"  # Возвращаем имя кнопки для вкладок оптимизации
    # Проверяем, есть ли вкладка в словаре вкладок драйверов
    elif tab_name in tabs_1:  # Если вкладка находится в словаре вкладок драйверов
        # Возвращаем имя кнопки для вкладок драйверов
        return "Драйверы"  # Возвращаем имя кнопки для вкладок драйверов
    # Проверяем, есть ли вкладка в словаре вкладок электропитания
    elif tab_name in tabs_2:  # Если вкладка находится в словаре вкладок электропитания
        # Возвращаем имя кнопки для вкладок электропитания
        return "Электропитание"  # Возвращаем имя кнопки для вкладок электропитания
    # Проверяем, есть ли вкладка в словаре вкладок исправлений
    elif tab_name in tabs_3:  # Если вкладка находится в словаре вкладок исправлений
        # Возвращаем имя кнопки для вкладок исправлений
        return "Исправления"  # Возвращаем имя кнопки для вкладок исправлений
    # Проверяем, есть ли вкладка в словаре вкладок очистки
    elif tab_name in tabs_4:  # Если вкладка находится в словаре вкладок очистки
        # Возвращаем имя кнопки для вкладок очистки
        return "Очистка"  # Возвращаем имя кнопки для вкладок очистки
    # Проверяем, есть ли вкладка в словаре других вкладок
    elif tab_name in tabs_5:  # Если вкладка находится в словаре других вкладок
        # Возвращаем имя кнопки для других вкладок
        return "Другое"  # Возвращаем имя кнопки для других вкладок
    # Проверяем, есть ли вкладка в словаре вкладок настроек
    elif tab_name in tabs_update:  # # Если вкладка находится в словаре других вкладок
        # Возвращаем имя кнопки для вкладок настроек
        return "Обновления"  # Возвращаем имя кнопки для вкладок настроек
    # Проверяем, есть ли вкладка в словаре вкладок настроек
    elif tab_name in tabs_6:  # Если вкладка находится в словаре вкладок настроек
        # Возвращаем имя кнопки для вкладок настроек
        return "Настройки"  # Возвращаем имя кнопки для вкладок настроек
    # Проверяем, есть ли вкладка в словаре минималистичных вкладок
    elif tabs_mini and tab_name in tabs_mini:  # Если вкладка находится в словаре минималистичных вкладок
        # Для минималистичных вкладок возвращаем имя вкладки напрямую
        # так как имена вкладок соответствуют именам папок
        return tab_name  # Возвращаем имя вкладки напрямую
    # Если вкладка не найдена ни в одном словаре
    return ""  # Возвращаем пустую строку


"""
+------------------------------------+
| Класс для создания всплывающих     |
| подсказок (ToolTip)                |
+------------------------------------+
"""


class ToolTip:  # Класс для создания всплывающих подсказок (ToolTip)
    def __init__(self, widget, filepath):  # Инициализация класса
        self.widget = widget  # Инициализируем widget
        self.filepath = filepath  # Инициализируем filepath
        self.tooltip = None  # Инициализируем tooltip
        self.widget.bind(
            "<Enter>", self.show_tooltip
        )  # Привязываем событие наведения к событию наведения
        self.widget.bind(
            "<Leave>", self.hide_tooltip
        )  # Привязываем событие наведения к событию наведения

        # Загружаем описания из файла
        self.descriptions = {}  # Инициализируем descriptions
        try:  # Пробуем выполнить код
            with open(
                "tweaks//descriptions.txt", "r", encoding="utf-8"
            ) as f:  # Открываем файл для чтения
                for line in f:  # Проходим по всем строкам в файле
                    if "=" in line:  # Если в строке есть '='
                        key, value = line.strip().split(
                            "=", 1
                        )  # Разделяем строку на ключ и значение
                        self.descriptions[key] = (
                            value  # Добавляем ключ и значение в descriptions
                        )
        except Exception as e:  # Если возникает ошибка
            print(
                f"❌ Ошибка при загрузке описаний: {str(e)}"
            )  # Выводим сообщение об ошибке

    def find_description(self, checkbox_name):  # Функция для поиска описания
        # Получаем имя файла из полного пути
        file_name = os.path.basename(
            checkbox_name
        )  # Получаем имя файла из полного пути

        # Сначала ищем точное совпадение
        if file_name in self.descriptions:  # Если имя файла находится в descriptions
            return self.descriptions[file_name]  # Возвращаем описание

        # Если точного совпадения нет, ищем частичное совпадение
        for key in self.descriptions:  # Проходим по всем ключам в descriptions
            if (
                key in file_name or file_name in key
            ):  # Если ключ находится в имени файла или имя файла находится в ключе
                return self.descriptions[key]  # Возвращаем описание
        return None  # Возвращаем None

    def format_description(self, text):  # Функция для форматирования описания
        # Разбиваем текст на предложения и добавляем перенос строки после каждой точки
        sentences = text.split(
            ". "
        )  # Разбиваем текст на предложения и добавляем перенос строки после каждой точки
        formatted_text = ".\n".join(
            sentences
        )  # Добавляем дополнительный перенос строки для лучшей читаемости
        return (
            formatted_text.replace("Плюсы:", "\nПлюсы:")
            .replace("Минусы:", "\nМинусы:")
            .replace("Рекомендуется", "\nРекомендуется")
        )  # Заменяем текст на форматированный текст

    def show_tooltip(self, event):  # Функция для отображения всплывающей подсказки
        global tooltips_enabled  # Объявляем переменную tooltips_enabled
        if not tooltips_enabled:  # Если всплывающие подсказки не включены
            return  # Возвращаем None

        x, y, _, _ = self.widget.bbox("insert")  # Получаем координаты виджета
        x += self.widget.winfo_rootx() + 25  # Увеличиваем смещение вправо
        y += self.widget.winfo_rooty() - 200  # Увеличиваем смещение вверх

        if x < 0:  # Если x меньше 0
            x = 0  # Устанавливаем x в 0
        if y < 0:  # Если y меньше 0
            y = 0  # Устанавливаем y в 0

        self.tooltip = tk.Toplevel(self.widget)  # Создаем всплывающее окно
        self.tooltip.wm_overrideredirect(True)  # Отключаем стандартные возможности окна

        tooltip_width = 600  # Устанавливаем ширину подсказки
        tooltip_height = 200  # Увеличиваем высоту подсказки
        self.tooltip.geometry(f"{tooltip_width}x{tooltip_height}+{x}+{y}")

        try:  # Пробуем выполнить код
            # Получаем имя чекбокса
            checkbox_name = self.widget["text"]  # Получаем имя чекбокса

            # Ищем описание
            description = self.find_description(checkbox_name)  # Получаем описание

            if description:  # Если описание есть
                # Форматируем описание, добавляя переносы строк
                formatted_description = self.format_description(
                    description
                )  # Форматируем описание
                label = tk.Label(
                    self.tooltip,  # Создаем метку
                    text=formatted_description,  # Устанавливаем текст метки
                    background="#190831",  # Темный фон
                    foreground="#32FBE2",  # Бирюзовый текст
                    relief="solid",  # Устанавливаем стиль рамки
                    borderwidth=3,  # Увеличиваем ширину рамки
                    highlightthickness=2,  # Добавляем толщину выделения
                    highlightbackground="#FFD700",  # Золотой цвет рамки
                    highlightcolor="#FFD700",  # Золотой цвет рамки при фокусе
                    wraplength=580,  # Устанавливаем максимальную ширину текста
                    justify=tk.LEFT,  # Выравнивание текста по левому краю
                    padx=10,  # Добавляем отступы
                    pady=10,  # Добавляем отступы
                )
            else:  # Если описания нет
                # Если описания нет, показываем содержимое файла
                current_tab = tab_control.select()  # Получаем текущую вкладку
                tab_text = tab_control.tab(
                    current_tab, "text"
                )  # Получаем текст вкладки
                button_name = get_button_name(tab_text)  # Получаем имя кнопки
                # Определяем папку для поиска файла
                base_folder = {
                    "Главная": "Главная",  # Главная
                    "Оптимизация": "Оптимизация",  # Оптимизация
                    "Драйверы": "Драйверы",  # Драйверы
                    "Электропитание": "Электропитание",  # Электропитание
                    "Исправления": "Исправления",  # Исправления
                    "Очистка": "Очистка",  # Очистка
                    "Другое": "Другое",  # Другое
                    "Настройки": "Настройки",  # Настройки
                    "Старые твики": "Старые твики",  # Старые твики
                }.get(button_name, button_name)  # Получаем имя папки

                rel_path = os.path.normpath(self.filepath).split(f"tweaks{os.sep}")[
                    -1
                ]  # Получаем путь к файлу
                full_path = os.path.join(
                    "tweaks", base_folder, rel_path
                )  # Получаем полный путь к файлу

                with open(full_path, "r", encoding="utf-8") as file:  # Открываем файл
                    file_content = file.read()  # Читаем содержимое файла
                    if (
                        len(file_content) > 1000
                    ):  # Если длина содержимого файла больше 1000 символов
                        file_content = (
                            file_content[:1000] + "..."
                        )  # Обрезаем содержимое файла
                    # Форматируем содержимое файла
                    formatted_content = self.format_description(
                        file_content
                    )  # Форматируем содержимое файла
                    label = tk.Label(
                        self.tooltip,  # Создаем метку
                        text=formatted_content,  # Устанавливаем текст метки
                        background="#190831",  # Темный фон
                        foreground="#32FBE2",  # Бирюзовый текст
                        relief="solid",  # Устанавливаем стиль рамки
                        borderwidth=3,  # Увеличиваем ширину рамки
                        highlightthickness=2,  # Добавляем толщину выделения
                        highlightbackground="#FFD700",  # Золотой цвет рамки
                        highlightcolor="#FFD700",  # Золотой цвет рамки при фокусе
                        wraplength=580,  # Устанавливаем максимальную ширину текста
                        justify=tk.LEFT,  # Выравнивание текста по левому краю
                        padx=10,  # Добавляем отступы
                        pady=10,  # Добавляем отступы
                    )

        except Exception as e:  # Если возникает ошибка
            error_message = f"Ошибка: {str(e)}"  # Сообщение об ошибке
            label = tk.Label(
                self.tooltip,  # Создаем метку
                text=error_message,  # Устанавливаем текст метки
                background="#190831",  # Темный фон
                foreground="#32FBE2",  # Бирюзовый текст
                relief="solid",  # Устанавливаем стиль рамки
                borderwidth=3,  # Увеличиваем ширину рамки
                highlightthickness=2,  # Добавляем толщину выделения
                highlightbackground="#FFD700",  # Золотой цвет рамки
                highlightcolor="#FFD700",  # Золотой цвет рамки при фокусе
                wraplength=580,  # Устанавливаем максимальную ширину текста
                justify=tk.LEFT,  # Выравнивание текста по левому краю
                padx=10,  # Добавляем отступы
                pady=10,  # Добавляем отступы
            )

        label.pack(fill=tk.BOTH, expand=True)  # Упаковываем метку

    def hide_tooltip(self, event):  # Функция для скрытия всплывающей подсказки
        if self.tooltip:  # Если всплывающая подсказка существует
            self.tooltip.destroy()  # Удаляем всплывающую подсказку
            self.tooltip = None  # Удаляем всплывающую подсказку
        self.tooltip = None  # Удаляем всплывающую подсказку


"""
+----------------------------------------------+
| Функция для выделения всех элементов в табах |
+----------------------------------------------+
"""


def select_all_for_tabs(tab_frame):  # Функция для выделения всех элементов в табах
    # Проходим по всем чекбоксам и устанавливаем их значение в True
    for checkbox in checkboxes.values():  # Проходим по всем чекбоксам
        checkbox.set(True)  # Устанавливаем состояние чекбокса в True


def switch_to_select():
    # Получаем текущую активную вкладку
    current_tab = tab_control.select()
    if not current_tab:
        return

    # Получаем имя текущей вкладки напрямую из tab_control
    current_tab_name = tab_control.tab(current_tab, "text")

    # Выделяем чекбоксы только в текущей вкладке
    for checkbox_name, checkbox_var in checkboxes.items():
        if get_tab_name(checkbox_name) == current_tab_name:
            checkbox_var.set(True)


"""
+----------------------------------------+
| Функция для выполнения старых скриптов |
+----------------------------------------+
"""
def offer_backup():
    """Предлагает пользователю создать бэкап реестра при запуске программы"""
    # Проверяем настройку offer_backup_enabled
    if not config.getboolean("General", "offer_backup_enabled", fallback=True):
        return
    if messagebox.askyesno(
        "Резервное копирование",
        "Рекомендуется создать резервную копию реестра перед использованием твикера.\n\nСоздать резервную копию сейчас?",
        icon='warning'
    ):
        export_full_registry()

def execute_old():  # Функция для выполнения старых скриптов
    offer_backup()
    
    # Получаем настройку способа запуска твиков
    execution_mode = config.get("General", "tweak_execution_mode", fallback="default")
    
    # Если режим "create_config_and_run", сначала создаем конфиг
    if execution_mode == "create_config_and_run":
        # Собираем все выбранные чекбоксы
        activated_checkboxes = [
            checkbox_name
            for checkbox_name, checkbox_var in checkboxes.items()
            if checkbox_var.get()
        ]
        
        if not activated_checkboxes:
            # Молча выходим без предупреждения
            return
        
        # Создаем конфиг
        try:
            filename = create_batch_file(activated_checkboxes)
            update_config_file_list()
            # Убраны все сообщения
        except Exception:
            # Ошибка игнорируется в фоновом режиме
            pass
        return  # Выходим после создания конфига
    
    # Проходим по всем чекбоксам в фоне
    for checkbox_name, checkbox_var in checkboxes.items():
        if checkbox_var.get():  # Если чекбокс включен
            tab_name = get_tab_name(checkbox_name)
            
            if tab_name is None:
                continue  # Молча пропускаем
            
            button_name = get_button_name(tab_name)
            tweak_path = f"tweaks\\{button_name}\\{tab_name}\\{checkbox_name}"
            
            if not os.path.exists(tweak_path):
                continue  # Молча пропускаем
            
            # Определяем режим запуска твика
            tweak_execution_mode = execution_mode if execution_mode != "create_config_and_run" else "default"
            
            # Запуск в фоне без отображения окон
            def run_tweak_by_mode(tweak_path, is_reg=False):
                try:
                    if tweak_execution_mode == "no_launcher":
                        subprocess.Popen(f'cmd /c "{tweak_path}"', shell=True, 
                                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    elif tweak_execution_mode == "launcher":
                        subprocess.Popen(f'Utils\\launcher.exe "{tweak_path}"', shell=True,
                                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    elif tweak_execution_mode == "powerrun":
                        subprocess.Popen(f'Utils\\PowerRun.exe "{tweak_path}"', shell=True,
                                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    elif tweak_execution_mode == "cmd":
                        subprocess.Popen(f'cmd /c "{tweak_path}"', shell=True,
                                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    else:  # default
                        if is_reg:
                            subprocess.Popen(f'cmd /c "{tweak_path}"', shell=True,
                                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                            subprocess.Popen(f'Utils\\PowerRun.exe "{tweak_path}"', shell=True,
                                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        else:
                            subprocess.Popen(f'cmd /c "{tweak_path}"', shell=True,
                                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                            subprocess.Popen(f'Utils\\launcher.exe "{tweak_path}"', shell=True,
                                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                except Exception:
                    pass  # Игнорируем ошибки выполнения

            # Если скрипт имеет расширение .bat, .cmd или .exe
            if checkbox_name.endswith((".bat", ".cmd", ".exe")):
                run_tweak_by_mode(tweak_path)

            # Если скрипт имеет расширение .ps1
            elif checkbox_name.endswith(".ps1"):
                try:
                    if not os.path.exists(tweak_path):
                        continue
                    
                    temp_ps1_path = ".\\1.ps1"
                    import shutil
                    shutil.copy2(tweak_path, temp_ps1_path)
                    
                    if tweak_execution_mode == "no_launcher":
                        subprocess.Popen([
                            'powershell.exe', '-ExecutionPolicy', 'Bypass', '-File', temp_ps1_path
                        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    else:
                        subprocess.Popen([
                            "Utils\\launcher.exe",
                            f'powershell.exe -ExecutionPolicy Bypass -File "{temp_ps1_path}"'
                        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    
                    # Удаляем временный файл после выполнения (с задержкой)
                    import threading
                    def delayed_cleanup():
                        import time
                        time.sleep(5)  # Даем время на выполнение
                        try:
                            os.remove(temp_ps1_path)
                        except:
                            pass
                    threading.Thread(target=delayed_cleanup, daemon=True).start()
                    
                except Exception:
                    # Запасной вариант - игнорируем ошибки
                    pass

            # Если скрипт имеет расширение .reg
            elif checkbox_name.endswith(".reg"):
                if execution_mode == "powerrun":
                    subprocess.Popen(f'Utils\\PowerRun.exe "{tweak_path}"', shell=True,
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                else:
                    run_tweak_by_mode(tweak_path, is_reg=True)

            # Если скрипт имеет расширение .pow
            elif checkbox_name.endswith(".pow"):
                subprocess.Popen(f'powercfg /import "{tweak_path}"', shell=True,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                run_tweak_by_mode(tweak_path)
                # Телеметрия полностью удалена

            # Если скрипт не имеет расширение .bat, .cmd, .exe, .ps1 или .reg
            else:
                run_tweak_by_mode(tweak_path)

            # Вся телеметрия удалена


"""
+------------------------------------+
| Функция для создания batch файла   |
| на основе выбранных чекбоксов      |
+------------------------------------+
"""


def create_batch_file(
    activated_checkboxes,
):  # Функция для создания batch файла на основе выбранных чекбоксов
    # """
    # Функция для создания batch файла на основе выбранных чекбоксов.

    # Эта функция выполняет следующие действия:
    # 1. Создает уникальное имя файла с текущей датой и временем
    # 2. Создает директорию Configs, если она не существует
    # 3. Записывает команды в batch файл для каждого выбранного чекбокса

    # Параметры:
    # ----------
    # activated_checkboxes : list
    #     Список имен выбранных чекбоксов

    # Возвращает:
    # -----------
    # str
    #     Путь к созданному batch файлу

    # Пример использования:
    # --------------------
    # filename = create_batch_file(["чекбокс1", "чекбокс2"])
    # # Создаст файл Configs\Config Extreme 2024-03-20 12-30-45.bat

    # Примечания:
    # ----------
    # - Batch файл - это текстовый файл с расширением .bat, содержащий команды для выполнения
    # - @echo off - отключает вывод команд в консоль
    # - chcp 65001 - устанавливает кодировку UTF-8 для корректного отображения русских символов
    # - cmd /c - выполняет команду и закрывает консоль
    # """
    # Создаем уникальное имя файла с текущей датой и временем
    # datetime.now() - текущая дата и время
    # strftime - форматирует дату и время в строку
    filename = f"user_data\\Configs\\{clean_username}_Config_{datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.bat"
    
    # Создаем директорию Configs, если она не существует
    # exist_ok=True - не вызывает ошибку, если директория уже существует
    os.makedirs(
        "Configs", exist_ok=True
    )  # Создаем директорию Configs, если она не существует

    # Открываем файл для записи в кодировке UTF-8
    with open(
        filename, "w", encoding="utf-8"
    ) as f:  # Открываем файл для записи в кодировке UTF-8
        # Записываем команду для отключения вывода команд
        f.write("@echo off\n")
        # Устанавливаем кодировку UTF-8
        f.write("chcp 65001\n")

        # Для каждого выбранного чекбокса
        for (
            checkbox_name,
            checkbox_var,
        ) in checkboxes.items():  # Проходим по всем чекбоксам
            # Если чекбокс выбран (его значение True)
            if checkbox_var.get():  # Если чекбокс выбран (его значение True)
                # Получаем имя вкладки для чекбокса
                tab_name = get_tab_name(
                    checkbox_name
                )  # Получаем имя вкладки для чекбокса

                # Получаем имя кнопки на основе имени вкладки
                button_name = get_button_name(
                    tab_name
                )  # Получаем имя кнопки на основе имени вкладки

                # Записываем команду для выполнения скрипта
                # tweaks\\{button_name}\\{tab_name}\\{checkbox_name} - путь к скрипту
                f.write(
                    f'cmd /c "tweaks\\{button_name}\\{tab_name}\\{checkbox_name}"\n'
                )  # Записываем команду для выполнения скрипта

    # Возвращаем путь к созданному файлу
    return filename


"""
+---------------------------------------------------+
| Функция для обновления списка файлов конфигурации |
+---------------------------------------------------+
"""


def update_config_file_list():  # Функция для обновления списка файлов конфигурации
    global config_file_values  # Объявляем переменную как глобальную
    config_file_values = [
        f for f in os.listdir("Configs") if f.endswith(".bat")
    ]  # Получаем список .bat файлов


"""
+------------------------------------+
| Основная функция выполнения        |
| конфигурационного файла            |
+------------------------------------+
"""


def execute():  # Основная функция выполнения конфигурационного файла
    # Собираем все выбранные чекбоксы
    activated_checkboxes = [
        checkbox_name
        for checkbox_name, checkbox_var in checkboxes.items()
        if checkbox_var.get()
    ]
    if (
        execute_function_var.get() == "Создать конфиг"
    ):  # Если функция выполнения - "Создать конфиг"
        filename = create_batch_file(
            activated_checkboxes
        )  # Создаем конфигурационный файл
        update_config_file_list()  # Обновляем список файлов конфигурации
    elif (
        execute_function_var.get() == "Выполнить"
    ):  # Если функция выполнения - "Выполнить"
        execute_old()  # Вызов функции для выполнения старых скриптов


"""
+------------------------------------+
| Функция для выполнения             |
| конфигурационного файла            |
+------------------------------------+
"""


def execute_config():  # Функция для выполнения конфигурационного файла
    selected_file = config_file_var.get()  # Получаем выбранный файл
    if selected_file:  # Если файл выбран
        print(f"Start Configs\\{selected_file}")  # Выводим путь к файлу
        subprocess.call(
            f'Utils\\launcher.exe "Configs\\{selected_file}"', shell=True
        )  # Выполняем файл


"""
+------------------------------------+
| Функция для получения имени вкладки|
| по имени чекбокса                  |
+------------------------------------+
"""


def get_tab_name(
    checkbox_name,
):  # Функция для получения имени вкладки по имени чекбокса
    """
    Функция для определения имени вкладки по имени чекбокса.

    Эта функция выполняет следующие действия:
    1. Проверяет, к какому словарю относится чекбокс
    2. Возвращает имя вкладки, в которой находится чекбокс

    Параметры:
    ----------
    checkbox_name : str
        Имя чекбокса, для которого нужно найти вкладку

    Возвращает:
    -----------
    str
        Имя вкладки, в которой находится чекбокс

    Пример использования:
    --------------------
    tab_name = get_tab_name("чекбокс1")
    # Возвращает "System" если чекбокс находится во вкладке System

    Примечания:
    ----------
    - Функция проверяет все словари: tabs_main, tabs, tabs_1, tabs_2, etc.
    - Если чекбокс не найден ни в одном словаре, возвращает None
    """
    # Проверяем все словари вкладок
    for tab_dict in [
        tabs_main,
        tabs,
        tabs_1,
        tabs_2,
        tabs_3,
        tabs_4,
        tabs_5,
        tabs_6,
        tabs_update,
    ]:  # Проходим по всем словарям вкладок
        for (
            tab_name,
            checkbox_list,
        ) in tab_dict.items():  # Проходим по всем вкладкам в словаре
            if (
                checkbox_name in checkbox_list
            ):  # Если чекбокс найден в списке чекбоксов вкладки
                return tab_name  # Возвращаем имя вкладки

    # Если чекбокс не найден ни в одном словаре, возвращаем None
    return None  # Возвращаем None


"""
+------------------------------------+
| Функция для перезапуска процесса   |
+------------------------------------+
"""


def collect_and_send():  # Функция для сбора и отправки телеметрии
    # from telemetry.telemetry_manager import (
    #     TelemetryManager,
    # )  # Импортируем класс TelemetryManager из модуля telemetry_manager

    # manager = TelemetryManager()  # Создаем экземпляр класса TelemetryManager
    # # logger.logger.info(
    # #     "Начало сбора и отправки телеметрии..."
    # # )  # Логируем начало сбора и отправки телеметрии
    
    # # Проверяем, включен ли обмен телеметрией
    # share_enabled = config.getboolean("Telemetry", "share_telemetry", fallback=False)
    
    # if manager.collect_telemetry_data(share_enabled=share_enabled):  # Если телеметрия успешно собрана
    #     pass
    #     # logger.logger.info(
    #     #     "Телеметрия успешно собрана и отправлена"
    #     # )  # Логируем успешное собрание и отправку телеметрии
    #     # print(
    #     #     "Телеметрия успешно собрана и отправлена"
    #     # )  # Выводим сообщение о успешном собрании и отправке телеметрии
    # else:  # Если телеметрия не собрана
    #     logger.logger.error(
    #         "Ошибка при сборе и отправке телеметрии"
    #     )  # Логируем ошибку при сборе и отправке телеметрии
    #     print(
    #         "Ошибка при сборе и отправке телеметрии"
    #     )  # Выводим сообщение об ошибке при сборе и отправке телеметрии
    pass


def restart():  # Функция для перезапуска программы
    root.destroy()  # Закрываем окно
    root.quit()  # Закрываем программу


# Настраиваем основные цвета и стили
style = ttk.Style()  # Создаем объект стиля
# Шрифты будут настроены позже через update_font_style() после инициализации current_font

# Настраиваем стиль для кнопок (без шрифта, он будет установлен позже)
style.configure(
    "Custom.TButton",
    padding=5,  # Отступы внутри кнопки
    relief="solid",  # Делаем обводку видимой
    borderwidth=1,  # Делаем обводку видимой
)

# Настраиваем стиль для вкладок (без шрифта, он будет установлен позже)
style.configure(
    "TNotebook.Tab",
    padding=[10, 5],  # Отступы внутри вкладок
)

# Создаем пустой словарь для хранения переменных состояния чекбоксов
checkboxes = {}

# Список доступных шрифтов
font_family_values = [
    "scode18",
    "Segoe UI",
    "Rust",
    "Foxy",
    "Frizon",
    "Velocity",
    "Roboto",
    "Montserrat",
    "Lato",
    "Open Sans",
    "Nunito",
    "Arial",
    "Times New Roman",
    "Verdana",
    "Georgia",
    "Courier New",
    "Ubuntu",
    "Ubuntu Mono",
    "Ubuntu Condensed",
    "Ubuntu Light",
    "Ubuntu Bold",
    "System",
    "Terminal",
    "Small Fonts",
    "Fixedsys",
    "hooge 05_53",
    "hooge 05_54",
    "hooge 05_55",
    "JetBrainsMono Nerd Font",
    "JetBrainsMono Nerd Font Mono",
]

# Инициализация всех переменных
font_size_var = tk.IntVar(value=int(config["General"].get("font_size", "12")))  # Переменная для хранения размера шрифта
theme_var = tk.StringVar(
    value=config["General"]["theme"]
)  # Переменная для хранения темы
search_entry_var = tk.StringVar()  # Переменная для хранения поискового запроса
execute_function_var = tk.StringVar(
    value="Выполнить"
    if "Execute" not in config or "execute_function" not in config["Execute"]
    else config["Execute"]["execute_function"]
)  # Переменная для хранения функции выполнения
config_file_var = tk.StringVar()  # Переменная для хранения файла конфигурации
font_family_var = tk.StringVar(
    value=config["General"]["font_family"]
)  # Переменная для хранения шрифта
quick_button_font_size_var = tk.IntVar(
    value=int(config["General"].get("quick_button_font_size", "12"))
)  # Переменная для хранения размера шрифта кнопок быстрого доступа

# Инициализация списка файлов конфигурации
config_file_values = (
    [f for f in os.listdir("Configs") if f.endswith(".bat")]
    if os.path.exists("Configs")
    else []
)

# Получаем размер поля конфигурации из настроек
width = int(float(config["General"].get("size_of_the_config_field", "1.5")) * 30)

# Загружаем состояние подсказок из конфигурации
if "General" not in config:  # Если General нет в конфигурации
    config["General"] = {}  # Создаем пустой словарь для General
if "tooltips_enabled" not in config["General"]:  # Если tooltips_enabled нет в General
    config["General"]["tooltips_enabled"] = (
        "True"  # Устанавливаем tooltips_enabled в True
    )
tooltip_control_var = tk.StringVar(
    value="Включено"
    if config["General"].getboolean("tooltips_enabled", True)
    else "Выключено"
)  # Переменная для хранения состояния подсказок
tooltips_enabled = config["General"].getboolean(
    "tooltips_enabled", True
)  # Получаем состояние подсказок

# Переменные для хранения текущих значений шрифта и темы
checkbox_current_font = (
    config["General"]["font_family"],
    int(config["General"]["checkbox_font_size"]),
)  # Переменная для хранения текущего шрифта и размера шрифта для чекбоксов
current_font = (
    config["General"]["font_family"],
    int(config["General"]["font_size"]),
)  # Переменная для хранения текущего шрифта и размера шрифта
current_theme = config["General"]["theme"]  # Переменная для хранения темы

# Функции для получения размеров шрифтов для разных элементов
def get_title_font():
    """Возвращает шрифт для заголовка (увеличенный размер)"""
    font_family = current_font[0]
    base_size = current_font[1]
    title_size = max(18, int(base_size * 2.5))  # Минимум 18, обычно в 2.5 раза больше базового
    return (font_family, title_size, "bold", "italic")

def get_version_font():
    """Возвращает шрифт для версии (средний размер)"""
    font_family = current_font[0]
    base_size = current_font[1]
    version_size = max(10, int(base_size * 1.3))  # Минимум 10, примерно в 1.3 раза больше базового
    return (font_family, version_size)

def get_icon_button_font():
    """Возвращает шрифт для иконок кнопок (всегда использует размер из настроек)"""
    font_family = current_font[0]
    icon_size = quick_button_font_size_var.get()  # Всегда используем размер из настроек
    return (font_family, icon_size)

def get_medium_label_font():
    """Возвращает шрифт для средних меток"""
    font_family = current_font[0]
    base_size = current_font[1]
    medium_size = max(9, int(base_size * 1.0))  # Примерно базовый размер
    return (font_family, medium_size)

def get_small_label_font():
    """Возвращает шрифт для маленьких меток"""
    font_family = current_font[0]
    base_size = current_font[1]
    small_size = max(8, int(base_size * 0.9))  # Чуть меньше базового
    return (font_family, small_size)

# Создаем главный контейнер
main_container = ttk.Frame(root)  # Создаем главный контейнер
main_container.pack(
    fill="both", expand=True, padx=20, pady=20
)  # Упаковываем главный контейнер

# Создаем верхнюю панель
top_panel = ttk.Frame(main_container)  # Создаем верхнюю панель
top_panel.pack(fill="x", pady=(0, 20))  # Упаковываем верхнюю панель

# Создаем логотип и заголовок
title_frame = ttk.Frame(top_panel)  # Создаем логотип и заголовок
title_frame.pack(side="left")  # Упаковываем логотип и заголовок

# Создаем заголовок
title_label = ttk.Label(
    title_frame, text="⚡️ Extreme", font=get_title_font()
)

# Проверяем текущую тему и устанавливаем цвет текста
current_theme = style.theme_use()  # получаем название текущей темы
if current_theme in ["light_hone", "light_newhone", "hone", "newhone"]:
    title_label.configure(foreground="#eb9227")
if current_theme in ["extreme", "extra"]:
    title_label.configure(foreground="#ff1744")

title_label.pack(side="left")  # Упаковываем заголовок

# Добавляем обработчик клика на заголовок
title_label.bind("<Button-1>", lambda e: switch_to_minimal())
title_label.configure(cursor="hand2")  # Меняем курсор на указатель

version_label = ttk.Label(
    title_frame, text=version, font=get_version_font()
)  # Создаем версию
version_label.pack(side="left", padx=(10, 0), pady=(10, 0))  # Упаковываем версию

current_theme = style.theme_use()  # получаем название текущей темы
if current_theme in ["light_hone", "light_newhone", "hone", "newhone"]:
    version_label.configure(foreground="#eb9227")
if current_theme in ["extreme", "extra"]:
    version_label.configure(foreground="#ff1744")

version_label.pack(side="left")  # Упаковываем заголовок

# Создаем правую часть верхней панели
top_right_panel = ttk.Frame(top_panel)  # Создаем правую часть верхней панели
top_right_panel.pack(side="right", fill="y")  # Упаковываем правую часть верхней панели

# Поле поиска с иконкой
search_frame = ttk.Frame(top_right_panel)  # Создаем поле поиска с иконкой
search_frame.pack(side="left", padx=(0, 10))  # Упаковываем поле поиска с иконкой

"""
+------------------------------------+
| Функция для фильтрации чекбоксов   |
| на основе поискового запроса       |
+------------------------------------+
"""


def filter_checkboxes(
    *args,
):  # Функция для фильтрации чекбоксов на основе поискового запроса
    search_text = search_entry_var.get().lower()  # Получаем поисковый запрос
    if (
        search_text == "поиск..."
    ):  # Если текст равен "поиск...", считаем что поиск пустой
        search_text = ""  # Если текст равен "поиск...", считаем что поиск пустой

    # Проходим по всем вкладкам
    for tab_id in tab_control.tabs():  # Проходим по всем вкладкам
        tab_frame = tab_control.children[tab_id.split(".")[-1]]  # Получаем вкладку

        # Если вкладка не загружена, загружаем её
        if (
            hasattr(tab_frame, "tab_info") and not tab_frame.tab_info.get("loaded", False)
        ):  # Если вкладка не загружена, загружаем её
            # Проверяем, есть ли checkbox_names (не все вкладки имеют чекбоксы)
            if "checkbox_names" in tab_frame.tab_info:
                create_tab_content(
                    tab_frame.tab_info["name"],
                    tab_frame,
                    tab_frame.tab_info["checkbox_names"],
                )  # Загружаем вкладку
                tab_frame.tab_info["loaded"] = (
                    True  # Устанавливаем флаг загрузки в True
                )
            elif tab_frame.tab_info.get("name") == "Главная":
                # Для главной вкладки используем специальную функцию
                create_main_tab_content(tab_frame)
                tab_frame.tab_info["loaded"] = True

        # Рекурсивная функция для поиска и фильтрации чекбоксов
        def filter_widgets_recursive(parent):
            """Рекурсивно ищет и фильтрует чекбоксы во всех дочерних виджетах"""
            for widget in parent.winfo_children():
                # Обрабатываем обычные чекбоксы
                if isinstance(widget, ttk.Checkbutton):
                    checkbox_text = widget.cget("text").lower()
                    # Показываем или скрываем чекбокс в зависимости от поискового запроса
                    if search_text and search_text not in checkbox_text:
                        widget.grid_remove()  # Скрываем чекбокс
                    else:
                        widget.grid()  # Показываем чекбокс
                # Обрабатываем RectangleCheckbox
                elif hasattr(widget, 'checkbox_name'):
                    checkbox_text = widget.checkbox_name.lower()
                    # Показываем или скрываем чекбокс в зависимости от поискового запроса
                    if search_text and search_text not in checkbox_text:
                        widget.grid_remove()  # Скрываем чекбокс
                    else:
                        widget.grid()  # Показываем чекбокс
                # Обрабатываем placeholder (пустые метки)
                elif isinstance(widget, ttk.Label) and widget.cget("text") == "":
                    # Показываем placeholder только если поиск пустой
                    if search_text:
                        widget.grid_remove()
                    else:
                        widget.grid()
                # Рекурсивно обрабатываем дочерние виджеты
                else:
                    filter_widgets_recursive(widget)
        
        # Получаем все чекбоксы на вкладке
        for (
            widget
        ) in tab_frame.winfo_children():  # Проходим по всем виджетам на вкладке
            if isinstance(widget, ttk.Frame):  # Ищем main_container
                filter_widgets_recursive(widget)  # Рекурсивно фильтруем все виджеты

        # Обновляем прокрутку для каждой вкладки
        if (
            hasattr(tab_frame, "tab_info") and tab_frame.tab_info["loaded"]
        ):  # Если вкладка загружена
            for (
                widget
            ) in tab_frame.winfo_children():  # Проходим по всем виджетам на вкладке
                if isinstance(widget, ttk.Frame):  # Если виджет является фреймом
                    for inner_widget in (
                        widget.winfo_children()
                    ):  # Проходим по всем виджетам на вкладке
                        if isinstance(
                            inner_widget, tk.Canvas
                        ):  # Если виджет является canvas
                            inner_widget.config(
                                scrollregion=inner_widget.bbox("all")
                            )  # Обновляем прокрутку для каждой вкладки


# Поле поиска
search_entry = ttk.Entry(
    search_frame,  # Создаем поле поиска
    textvariable=search_entry_var,  # Связываем поле поиска с переменной поискового запроса
    width=30,  # Ширина поля поиска
    font=("Segoe UI", 10),  # Шрифт поля поиска
    style="TEntry",
)  # Применяем новый стиль
search_entry.pack(side="left")  # Упаковываем поле поиска
search_entry.insert(0, "Поиск...")  # Вставляем текст "Поиск..." в поле поиска

# Привязываем события к полю поиска
search_entry_var.trace("w", filter_checkboxes)  # Отслеживаем изменения в поле поиска
search_entry.bind(
    "<FocusIn>",
    lambda e: search_entry.delete(0, "end")
    if search_entry.get() == "Поиск..."
    else None,
)  # Привязываем событие к полю поиска
search_entry.bind(
    "<FocusOut>",
    lambda e: (search_entry.insert(0, "Поиск..."), filter_checkboxes())
    if search_entry.get() == ""
    else None,
)  # Привязываем событие к полю поиска


# Кнопка "Выделить все"
def switch_to_select():
    # Получаем текущую активную вкладку
    current_tab = tab_control.select()
    if not current_tab:
        return

    # Получаем имя текущей вкладки напрямую из tab_control
    current_tab_name = tab_control.tab(current_tab, "text")

    # Выделяем чекбоксы только в текущей вкладке
    for checkbox_name, checkbox_var in checkboxes.items():
        if get_tab_name(checkbox_name) == current_tab_name:
            checkbox_var.set(True)


select_all_button = ttk.Button(
    top_right_panel,
    text="Выделить все",
    bootstyle="warning-outline",
    command=switch_to_select,
)  # Создаем кнопку "Выделить все"
select_all_button.pack(side="left", padx=5)  # Упаковываем кнопку "Выделить все"


# Кнопка "Донат"
def open_donat():
    import webbrowser

    webbrowser.open("https://www.tinkoff.ru/cf/2VBH9zSztcW")
    donat_button.pack_forget()  # Убираем кнопку после нажатия
    # отключаем рекламу в конфигурации
    config["General"]["ad_enabled"] = (
        "False"  # Используем строку вместо булева значения
    )
    with open("user_data//settings.ini", "w", encoding="cp1251") as configfile:
        config.write(configfile)


# проверяем включена ли реклама в конфигурации
if config["General"].getboolean("ad_enabled", True):
    donat_button = ttk.Button(
        top_right_panel, text="Донат", bootstyle="warning-outline", command=open_donat
    )
    donat_button.pack(side="left", padx=5)
else:
    # donat_button.pack_forget()
    pass


# Кнопка "Реклама"
def open_youtube():
    import webbrowser

    webbrowser.open("https://shre.su/0KO3")
    ad_button.pack_forget()  # Убираем кнопку после нажатия
    # отключаем рекламу в конфигурации
    config["General"]["ad_enabled"] = (
        "False"  # Используем строку вместо булева значения
    )
    with open("user_data//settings.ini", "w", encoding="cp1251") as configfile:
        config.write(configfile)


# проверяем включена ли реклама в конфигурации
if config["General"].getboolean("ad_enabled", True):
    ad_button = ttk.Button(
        top_right_panel,
        text="Бесплатно поддержать",
        bootstyle="info-outline",
        command=open_youtube,
    )
    ad_button.pack(side="left", padx=5)
else:
    # ad_button.pack_forget()
    pass

# Кнопка выполнить
def execute_all():
    execute_old()
    for tab_id in tab_control.tabs():
        frame = tab_control.children.get(tab_id.split(".")[-1])
        if frame and hasattr(frame, "apply_all"):
            try:
                frame.apply_all()
            except Exception as e:
                print(f"Ошибка apply_all: {e}")

execute_button = ttk.Button(
    top_right_panel, text="Выполнить", bootstyle="success-outline", command=execute_all
)  # Создаем кнопку "Выполнить"
execute_button.pack(side="left", padx=5)  # Упаковываем кнопку "Выполнить"


# Кнопка "Перезагрузка Windows"
def restart_windows():
    question = messagebox.askyesno(
        "Перезагрузка Windows", "Вы уверены, что хотите перезагрузить Windows?"
    )
    if question:
        os.system("shutdown /r /t 0")

fullscreen_mode = config.getboolean("Window", "fullscreen", fallback=False)
if fullscreen_mode or root.attributes("-fullscreen", False):

    # Кнопка "Свернуть"
    def minimize_window():
        root.iconify()


    # Кнопка "Свернуть"
    minimize_button = ttk.Button(
        top_right_panel, text="_", bootstyle="danger-outline", command=minimize_window
    )  # Создаем кнопку "Свернуть"
    minimize_button.pack(side="left", padx=5)  # Упаковываем кнопку "Свернуть"


    # Кнопка "Restore"
    def restore_window():
        # если программа в полноэкранном режиме, то свернуть
        if root.attributes("-fullscreen"):
            root.attributes("-fullscreen", False)
        # если программа в обычном режиме, то развернуть
        else:
            root.attributes("-fullscreen", True)


    # Кнопка "Restore"
    restore_button = ttk.Button(
        top_right_panel, text=" ", bootstyle="danger-outline", command=restore_window
    )  # Создаем кнопку "Restore"
    restore_button.pack(side="left", padx=5)  # Упаковываем кнопку "Restore"

    # Кнопка "Выйти"
    exit_button = ttk.Button(
        top_right_panel, text="X", bootstyle="danger-outline", command=restart
    )  # Создаем кнопку "Выйти"
    exit_button.pack(side="left", padx=5)  # Упаковываем кнопку "Выйти"

# Создаем контейнер для вкладок и боковой панели
content_container = ttk.Frame(
    main_container
)  # Создаем контейнер для вкладок и боковой панели
content_container.pack(
    fill="both", expand=True
)  # Упаковываем контейнер для вкладок и боковой панели

# Создаем боковую панель для быстрого доступа
sidebar = ttk.Frame(
    content_container, style="Card.TFrame"
)  # Создаем боковую панель для быстрого доступа
sidebar.pack(
    side="left", fill="y", padx=(0, 20)
)  # Упаковываем боковую панель для быстрого доступа

"""
+------------------------------------+
| Функция для обновления значения    |
| функции выполнения в конфигурации  |
+------------------------------------+
"""


def update_execute_function(event=None):
    config.set(
        "Execute", "execute_function", execute_function_var.get()
    )  # Обновляем значение функции выполнения в конфигурации
    with open(
        "user_data//settings.ini", "w", encoding="cp1251"
    ) as configfile:  # Запись в ANSI
        config.write(configfile)  # Запись в ANSI


"""
+------------------------------------+
| Функция для обновления состояния   |
| подсказок                          |
+------------------------------------+
"""


def update_tooltip_state(*args):  # Функция для обновления состояния подсказок
    try:  # Попробуем обновить состояние подсказок
        global tooltips_enabled  # Объявляем переменную tooltips_enabled
        old_value = tooltips_enabled  # Сохраняем старое значение tooltips_enabled
        tooltips_enabled = (
            tooltip_control_var.get() == "Включено"
        )  # Обновляем значение tooltips_enabled
        config["General"]["tooltips_enabled"] = str(
            tooltips_enabled
        )  # Обновляем значение tooltips_enabled в конфигурации
        with open(
            "user_data//settings.ini", "w", encoding="cp1251"
        ) as configfile:  # Запись в ANSI
            config.write(configfile)  # Запись в ANSI
        logger.log_settings_change(
            "tooltips_enabled", old_value, tooltips_enabled
        )  # Логируем изменение состояния подсказок
    except Exception as e:  # Если возникает ошибка
        logger.log_error(
            "Ошибка при обновлении состояния подсказок", exc_info=e
        )  # Логируем ошибку


"""
+------------------------------------+
| Функция для обновления стиля       |
| элементов интерфейса с учетом      |
| заданного шрифта                   |
+------------------------------------+
"""


def update_font_style(update_window=True):
    """Обновляет стили шрифтов для всех виджетов интерфейса"""
    style = ttk.Style()  # Создаем объект стиля
    
    # Глобальный стиль по умолчанию
    style.configure(".", font=current_font)  # Настраиваем шрифт для всех виджетов по умолчанию
    
    # Базовые стили ttk
    style.configure("TLabel", font=current_font)  # Обновляем стиль для Label
    style.configure("TButton", font=current_font)  # Обновляем стиль для Button
    style.configure("TCheckbutton", font=checkbox_current_font)  # Чекбоксы используют checkbox_current_font
    style.configure("TCombobox", font=current_font)  # Обновляем стиль для Combobox
    style.configure("TEntry", font=current_font)  # Обновляем стиль для Entry
    style.configure("TNotebook.Tab", font=current_font)  # Обновляем стиль для Notebook.Tab
    # TScale не поддерживает настройку шрифта в ttkbootstrap (вызывает ошибку дублирования элемента)
    try:
        style.configure("TScale", font=current_font)  # Обновляем стиль для Scale
    except Exception:
        pass  # Игнорируем ошибку, так как TScale не использует шрифт напрямую
    
    # Кастомные стили
    style.configure("Custom.TButton", font=current_font)  # Обновляем стиль для Custom.TButton
    style.configure("Custom.TCheckbutton", font=checkbox_current_font)  # ВАЖНО: Чекбоксы используют checkbox_current_font
    style.configure("Custom.TLabel", font=current_font)  # Обновляем стиль для Custom.TLabel
    style.configure("Custom.TNotebook.Tab", font=current_font)  # Обновляем стиль для Custom.TNotebook.Tab
    style.configure("Custom.TEntry", font=current_font)  # Обновляем стиль для Custom.TEntry
    
    # Стили для категорий
    style.configure("Category.TButton", font=current_font)  # Используем current_font для категорий
    style.configure("Category.TLabel", font=current_font)  # Используем current_font для категорий
    
    # Стиль для Treeview
    try:
        style.configure("Treeview", font=current_font)  # Обновляем стиль для Treeview
        style.configure("Treeview.Heading", font=current_font)  # Обновляем стиль для заголовков Treeview
    except:
        pass
    
    # Применяем шрифт к виджетам tkinter через опции по умолчанию
    try:
        root.option_add("*Text.font", current_font)
        root.option_add("*Text.Font", current_font)
        root.option_add("*Entry.font", current_font)
        root.option_add("*Entry.Font", current_font)
        root.option_add("*Listbox.font", current_font)
        root.option_add("*Listbox.Font", current_font)
        root.option_add("*Label.font", current_font)
        root.option_add("*Label.Font", current_font)
        root.option_add("*Button.font", current_font)
        root.option_add("*Button.Font", current_font)
    except:
        pass
    
    # Обновляем окно только если нужно (не при начальной загрузке)
    if update_window:
        root.update_idletasks()  # Используем update_idletasks вместо update для лучшей производительности


"""
+------------------------------------+
| Функция для обновления текущей     |
| темы интерфейса                    |
+------------------------------------+
"""


# функция для обновления стиля кнопок при смене на любые темы
def update_button_style():
    # Создаем новый стиль для кнопок
    style.configure("Icon.TButton", font=get_icon_button_font(), padding=10, width=3)

    # Список светлых тем
    light_themes = [
        "cosmo",
        "flatly",
        "litera",
        "minty",
        "lumen",
        "sandstone",
        "yeti",
        "pulse",
        "united",
        "morph",
        "journal",
        "simplex",
        "cerculean",
        "green",
    ]

    # Настраиваем цвета и стиль в зависимости от темы
    if current_theme == "extreme": 
        style.configure("Icon.TButton", background="#0a0a0a", foreground="#ff1744", bordercolor="black", relief="solid")
    elif current_theme == "hone" or current_theme == "newhone": 
        style.configure("Icon.TButton", background="#0c131f", foreground="#eb9227", bordercolor="#0c131f", relief="solid")
    elif current_theme == "light_hone" or current_theme == "light_newhone": 
        style.configure("Icon.TButton", background="#d9e3f1", foreground="#eb9227", bordercolor="#d9e3f1", relief="solid")
    elif current_theme == "extra":
        style.configure("Icon.TButton", background="#0c131f", foreground="#ff1744", bordercolor="#0c131f", relief="solid")
    elif current_theme == "wincry_classic":
        style.configure("Icon.TButton", background="#1a1a1a", foreground="white", bordercolor="white", relief="solid")
    elif current_theme in light_themes:
        style.configure("Icon.TButton", background="#f0f0f0", foreground="black")
    elif current_theme == "wincry_warning" or current_theme == "wincry_full_warning":
        style.configure("Icon.TButton", background="#1a1a1a", foreground="#f0ad4e")
    else:
        style.configure("Icon.TButton", background="#1a1a1a", foreground="white")


def update_theme(event=None):  # Функция для обновления темы интерфейса
    try:  # Попробуем обновить тему интерфейса
        global current_theme  # Объявляем переменную current_theme
        new_theme = theme_var.get()  # Получаем новое значение темы
        if (
            new_theme != current_theme
        ):  # Если новое значение темы не равно текущему значению темы
            old_theme = current_theme  # Сохраняем старое значение темы

            # Обновляем остальные настройки
            update_colors()  # Обновляем цвета
            update_font()  # Обновляем шрифт
            config["General"]["theme"] = (
                new_theme  # Обновляем значение темы в конфигурации
            )
            with open(
                "user_data//settings.ini", "w", encoding="cp1251"
            ) as configfile:  # Запись в ANSI
                config.write(configfile)  # Запись в ANSI
            logger.log_settings_change(
                "theme", old_theme, new_theme
            )  # Логируем изменение темы

            # перезапускаем программу
            reload_program()
    except Exception as e:  # Если возникает ошибка
        logger.log_error("Ошибка при обновлении темы", exc_info=e)  # Логируем ошибку


"""
+------------------------------------+
| Функция для обновления текущей     |
| темы интерфейса                    |
+------------------------------------+
"""


def update_font(event=None):  # Функция для обновления шрифта
    try:  # Попробуем обновить шрифт
        global checkbox_current_font  # Объявляем переменную checkbox_current_font
        font_family = font_family_var.get()  # Получаем новое значение шрифта
        checkbox_font_size = font_size_var.get()  # Получаем новое значение шрифта
        old_font = checkbox_current_font  # Сохраняем старое значение шрифта
        checkbox_current_font = (
            font_family,
            checkbox_font_size,
        )  # Обновляем значение шрифта

        global current_font  # Объявляем переменную current_font
        # Получаем размер шрифта из переменной, а не из config
        font_size = font_size_var.get()
        current_font = (
            font_family,
            font_size,
        )  # Обновляем значение шрифта

        update_font_style()  # Обновляем стиль шрифта
        update_button_style()  # Обновляем стиль кнопок (включая Icon.TButton)
        # Обновляем также специальные элементы интерфейса
        try:
            if 'title_label' in globals():
                title_label.configure(font=get_title_font())
            if 'version_label' in globals():
                version_label.configure(font=get_version_font())
        except:
            pass
        config["General"]["font_family"] = (
            font_family  # Обновляем значение шрифта в конфигурации
        )
        config["General"]["font_size"] = str(
            font_size
        )  # Обновляем размер шрифта в конфигурации
        config["General"]["checkbox_font_size"] = str(
            checkbox_font_size
        )  # Обновляем значение шрифта в конфигурации
        with open(
            "user_data//settings.ini", "w", encoding="cp1251"
        ) as configfile:  # Запись в ANSI
            config.write(configfile)  # Запись в ANSI
        logger.log_settings_change(
            "font_settings", old_font, checkbox_current_font
        )  # Логируем изменение шрифта
        root.update_idletasks()  # Обновляем окно (используем update_idletasks вместо update для лучшей производительности)
    except Exception as e:  # Если возникает ошибка
        logger.log_error("Ошибка при обновлении шрифта", exc_info=e)  # Логируем ошибку


class RectangleCheckbox(ttk.Frame):
    """Виджет чекбокса в виде прямоугольника с кнопкой запуска и описанием"""
    
    def __init__(self, parent, checkbox_name, checkbox_var, tab_name, filepath, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.checkbox_name = checkbox_name
        self.checkbox_var = checkbox_var
        self.tab_name = tab_name
        self.filepath = filepath
        
        # Настройка стиля рамки
        self.configure(relief="solid", borderwidth=2)
        
        # Создаем контейнер для содержимого
        content_frame = ttk.Frame(self)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Верхняя часть: чекбокс и название
        top_frame = ttk.Frame(content_frame)
        top_frame.pack(fill="x", pady=(0, 5))
        
        # Чекбокс
        checkbox_widget = ttk.Checkbutton(
            top_frame,
            text=checkbox_name,
            variable=checkbox_var,
            style="Custom.TCheckbutton",
        )
        checkbox_widget.pack(side="left", anchor="w")
        
        # Описание (загружаем из descriptions.txt или файла)
        description = self._get_description()
        if description:
            desc_label = ttk.Label(
                content_frame,
                text=description[:150] + "..." if len(description) > 150 else description,
                wraplength=300,
                font=("Segoe UI", 9),
                foreground="#888888"
            )
            desc_label.pack(fill="x", pady=(5, 10), anchor="w")
        
        # Кнопка запуска
        launch_btn = ttk.Button(
            content_frame,
            text="▶ Запустить",
            command=self._launch_script,
            width=15
        )
        launch_btn.pack(side="bottom", pady=(5, 0))
    
    def _get_description(self):
        """Получает описание из descriptions.txt или файла"""
        try:
            # Пробуем загрузить из descriptions.txt
            descriptions = {}
            with open("tweaks//descriptions.txt", "r", encoding="utf-8") as f:
                for line in f:
                    if "=" in line:
                        key, value = line.strip().split("=", 1)
                        descriptions[key] = value
            
            file_name = os.path.basename(self.checkbox_name)
            if file_name in descriptions:
                return descriptions[file_name]
            
            # Ищем частичное совпадение
            for key in descriptions:
                if key in file_name or file_name in key:
                    return descriptions[key]
            
            # Если не найдено, возвращаем None
            return None
        except Exception:
            return None
    
    def _launch_script(self):
        """Запускает скрипт, связанный с чекбоксом"""
        if not self.checkbox_var.get():
            # Если чекбокс не выбран, выбираем его
            self.checkbox_var.set(True)
        
        # Получаем путь к скрипту
        tab_name = self.tab_name
        button_name = get_button_name(tab_name)
        tweak_path = f"tweaks\\{button_name}\\{tab_name}\\{self.checkbox_name}"
        
        # Проверяем существование файла
        if not os.path.exists(tweak_path):
            logger.log_error(f"Файл не найден: {tweak_path}")
            return
        
        try:
            # Запускаем скрипт в зависимости от расширения
            if self.checkbox_name.endswith((".bat", ".cmd")):
                subprocess.Popen(f'cmd /c "{tweak_path}"', shell=True)
            elif self.checkbox_name.endswith(".exe"):
                subprocess.Popen(f'"{tweak_path}"', shell=True)
            elif self.checkbox_name.endswith(".ps1"):
                subprocess.Popen([
                    "powershell.exe",
                    "-ExecutionPolicy", "Bypass",
                    "-File", tweak_path
                ])
            elif self.checkbox_name.endswith(".reg"):
                subprocess.Popen(f'reg import "{tweak_path}"', shell=True)
            elif self.checkbox_name.endswith(".pow"):
                subprocess.Popen(f'powercfg /import "{tweak_path}"', shell=True)
            else:
                subprocess.Popen(f'cmd /c "{tweak_path}"', shell=True)
            
            logger.log_info(f"Запущен скрипт: {self.checkbox_name}")
        except Exception as e:
            logger.log_error(f"Ошибка при запуске скрипта {self.checkbox_name}: {str(e)}")


class WideRectangleCheckbox(ttk.Frame):
    """Виджет чекбокса в виде широкого прямоугольника, занимающего всю ширину строки"""
    
    def __init__(self, parent, checkbox_name, checkbox_var, tab_name, filepath, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.checkbox_name = checkbox_name
        self.checkbox_var = checkbox_var
        self.tab_name = tab_name
        self.filepath = filepath
        
        # Настройка стиля рамки
        self.configure(relief="solid", borderwidth=2)
        
        # Создаем основной контейнер
        main_content = ttk.Frame(self)
        main_content.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Верхняя часть: чекбокс слева и название справа
        top_frame = ttk.Frame(main_content)
        top_frame.pack(fill="x", pady=(0, 8))
        
        # Чекбокс слева
        checkbox_widget = ttk.Checkbutton(
            top_frame,
            text="",  # Без текста, название будет отдельно
            variable=checkbox_var,
            style="Custom.TCheckbutton",
        )
        checkbox_widget.pack(side="left", anchor="w", padx=(0, 15))
        
        # Название опции
        name_label = ttk.Label(
            top_frame,
            text=checkbox_name,
            font=("Segoe UI", 11, "bold"),
            anchor="w"
        )
        name_label.pack(side="left", fill="x", expand=True)
        
        # Кнопка запуска справа
        launch_btn = ttk.Button(
            top_frame,
            text="▶ Запустить",
            command=self._launch_script,
            width=15
        )
        launch_btn.pack(side="right", padx=(10, 0))
        
        # Описание снизу
        description = self._get_description()
        if description:
            desc_label = ttk.Label(
                main_content,
                text=description,
                wraplength=800,
                font=("Segoe UI", 9),
                foreground="#666666",
                anchor="w",
                justify="left"
            )
            desc_label.pack(fill="x", pady=(5, 0), anchor="w")
    
    def _get_description(self):
        """Получает описание из descriptions.txt или файла"""
        try:
            # Пробуем загрузить из descriptions.txt
            descriptions = {}
            with open("tweaks//descriptions.txt", "r", encoding="utf-8") as f:
                for line in f:
                    if "=" in line:
                        key, value = line.strip().split("=", 1)
                        descriptions[key] = value
            
            file_name = os.path.basename(self.checkbox_name)
            if file_name in descriptions:
                return descriptions[file_name]
            
            # Ищем частичное совпадение
            for key in descriptions:
                if key in file_name or file_name in key:
                    return descriptions[key]
            
            # Если не найдено, возвращаем None
            return None
        except Exception:
            return None
    
    def _launch_script(self):
        """Запускает скрипт, связанный с чекбоксом"""
        if not self.checkbox_var.get():
            # Если чекбокс не выбран, выбираем его
            self.checkbox_var.set(True)
        
        # Получаем путь к скрипту
        tab_name = self.tab_name
        button_name = get_button_name(tab_name)
        tweak_path = f"tweaks\\{button_name}\\{tab_name}\\{self.checkbox_name}"
        
        # Проверяем существование файла
        if not os.path.exists(tweak_path):
            logger.log_error(f"Файл не найден: {tweak_path}")
            return
        
        try:
            # Запускаем скрипт в зависимости от расширения
            if self.checkbox_name.endswith((".bat", ".cmd")):
                subprocess.Popen(f'cmd /c "{tweak_path}"', shell=True)
            elif self.checkbox_name.endswith(".exe"):
                subprocess.Popen(f'"{tweak_path}"', shell=True)
            elif self.checkbox_name.endswith(".ps1"):
                subprocess.Popen([
                    "powershell.exe",
                    "-ExecutionPolicy", "Bypass",
                    "-File", tweak_path
                ])
            elif self.checkbox_name.endswith(".reg"):
                subprocess.Popen(f'reg import "{tweak_path}"', shell=True)
            elif self.checkbox_name.endswith(".pow"):
                subprocess.Popen(f'powercfg /import "{tweak_path}"', shell=True)
            else:
                subprocess.Popen(f'cmd /c "{tweak_path}"', shell=True)
            
            logger.log_info(f"Запущен скрипт: {self.checkbox_name}")
        except Exception as e:
            logger.log_error(f"Ошибка при запуске скрипта {self.checkbox_name}: {str(e)}")


class ExpandableWideRectangleCheckbox(ttk.Frame):
    """Виджет чекбокса в виде широкого прямоугольника с раскрывающимся описанием"""
    
    def __init__(self, parent, checkbox_name, checkbox_var, tab_name, filepath, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.checkbox_name = checkbox_name
        self.checkbox_var = checkbox_var
        self.tab_name = tab_name
        self.filepath = filepath
        self.is_expanded = False
        
        # Настройка стиля рамки
        self.configure(relief="solid", borderwidth=2)
        
        # Создаем основной контейнер
        main_content = ttk.Frame(self)
        main_content.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Верхняя часть: чекбокс слева и название справа
        top_frame = ttk.Frame(main_content)
        top_frame.pack(fill="x", pady=(0, 8))
        
        # Чекбокс слева
        checkbox_widget = ttk.Checkbutton(
            top_frame,
            text="",  # Без текста, название будет отдельно
            variable=checkbox_var,
            style="Custom.TCheckbutton",
        )
        checkbox_widget.pack(side="left", anchor="w", padx=(0, 15))
        
        # Название опции
        name_label = ttk.Label(
            top_frame,
            text=checkbox_name,
            font=("Segoe UI", 11, "bold"),
            anchor="w"
        )
        name_label.pack(side="left", fill="x", expand=True)
        
        # Кнопка "+" для раскрытия описания
        expand_btn = ttk.Button(
            top_frame,
            text="➕",
            command=self._toggle_description,
            width=3
        )
        expand_btn.pack(side="left", padx=(10, 10))
        
        # Кнопка запуска справа
        launch_btn = ttk.Button(
            top_frame,
            text="▶ Запустить",
            command=self._launch_script,
            width=15
        )
        launch_btn.pack(side="right", padx=(10, 0))
        
        # Контейнер для описания (изначально скрыт)
        self.description_frame = ttk.Frame(main_content)
        self.description_label = None
        
        # Загружаем описание, но не показываем его
        self.description = self._get_description()
    
    def _toggle_description(self):
        """Переключает видимость описания"""
        if self.description:
            if self.is_expanded:
                # Скрываем описание
                self.description_frame.pack_forget()
                self.is_expanded = False
            else:
                # Показываем описание
                if self.description_label is None:
                    self.description_label = ttk.Label(
                        self.description_frame,
                        text=self.description,
                        wraplength=800,
                        font=("Segoe UI", 9),
                        foreground="#666666",
                        anchor="w",
                        justify="left"
                    )
                    self.description_label.pack(fill="x", pady=(5, 0), anchor="w")
                self.description_frame.pack(fill="x", pady=(5, 0))
                self.is_expanded = True
    
    def _get_description(self):
        """Получает описание из descriptions.txt или файла"""
        try:
            # Пробуем загрузить из descriptions.txt
            descriptions = {}
            with open("tweaks//descriptions.txt", "r", encoding="utf-8") as f:
                for line in f:
                    if "=" in line:
                        key, value = line.strip().split("=", 1)
                        descriptions[key] = value
            
            file_name = os.path.basename(self.checkbox_name)
            if file_name in descriptions:
                return descriptions[file_name]
            
            # Ищем частичное совпадение
            for key in descriptions:
                if key in file_name or file_name in key:
                    return descriptions[key]
            
            # Если не найдено, возвращаем None
            return None
        except Exception:
            return None
    
    def _launch_script(self):
        """Запускает скрипт, связанный с чекбоксом"""
        if not self.checkbox_var.get():
            # Если чекбокс не выбран, выбираем его
            self.checkbox_var.set(True)
        
        # Получаем путь к скрипту
        tab_name = self.tab_name
        button_name = get_button_name(tab_name)
        tweak_path = f"tweaks\\{button_name}\\{tab_name}\\{self.checkbox_name}"
        
        # Проверяем существование файла
        if not os.path.exists(tweak_path):
            logger.log_error(f"Файл не найден: {tweak_path}")
            return
        
        try:
            # Запускаем скрипт в зависимости от расширения
            if self.checkbox_name.endswith((".bat", ".cmd")):
                subprocess.Popen(f'cmd /c "{tweak_path}"', shell=True)
            elif self.checkbox_name.endswith(".exe"):
                subprocess.Popen(f'"{tweak_path}"', shell=True)
            elif self.checkbox_name.endswith(".ps1"):
                subprocess.Popen([
                    "powershell.exe",
                    "-ExecutionPolicy", "Bypass",
                    "-File", tweak_path
                ])
            elif self.checkbox_name.endswith(".reg"):
                subprocess.Popen(f'reg import "{tweak_path}"', shell=True)
            elif self.checkbox_name.endswith(".pow"):
                subprocess.Popen(f'powercfg /import "{tweak_path}"', shell=True)
            else:
                subprocess.Popen(f'cmd /c "{tweak_path}"', shell=True)
            
            logger.log_info(f"Запущен скрипт: {self.checkbox_name}")
        except Exception as e:
            logger.log_error(f"Ошибка при запуске скрипта {self.checkbox_name}: {str(e)}")


class SapphireCheckbox(ttk.Frame):
    """Виджет чекбокса в виде широкого прямоугольника с раскрывающимся описанием (в два столбца)"""
    
    def __init__(self, parent, checkbox_name, checkbox_var, tab_name, filepath, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.checkbox_name = checkbox_name
        self.checkbox_var = checkbox_var
        self.tab_name = tab_name
        self.filepath = filepath
        self.is_expanded = False
        
        # Настройка стиля рамки
        self.configure(relief="solid", borderwidth=2)
        
        # Создаем основной контейнер
        main_content = ttk.Frame(self)
        main_content.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Верхняя часть: чекбокс слева и название справа
        top_frame = ttk.Frame(main_content)
        top_frame.pack(fill="x", pady=(0, 8))
        
        # Чекбокс слева
        checkbox_widget = ttk.Checkbutton(
            top_frame,
            text="",  # Без текста, название будет отдельно
            variable=checkbox_var,
            style="Custom.TCheckbutton",
        )
        checkbox_widget.pack(side="left", anchor="w", padx=(0, 15))
        
        # Название опции
        name_label = ttk.Label(
            top_frame,
            text=checkbox_name,
            font=("Segoe UI", 11, "bold"),
            anchor="w"
        )
        name_label.pack(side="left", fill="x", expand=True)
        
        # Кнопка "+" для раскрытия описания
        expand_btn = ttk.Button(
            top_frame,
            text="➕",
            command=self._toggle_description,
            width=3
        )
        expand_btn.pack(side="left", padx=(10, 10))
        
        # Кнопка запуска справа
        launch_btn = ttk.Button(
            top_frame,
            text="▶ Запустить",
            command=self._launch_script,
            width=15
        )
        launch_btn.pack(side="right", padx=(10, 0))
        
        # Контейнер для описания (изначально скрыт)
        self.description_frame = ttk.Frame(main_content)
        self.description_label = None
        
        # Загружаем описание, но не показываем его
        self.description = self._get_description()
    
    def _toggle_description(self):
        """Переключает видимость описания"""
        if self.description:
            if self.is_expanded:
                # Скрываем описание
                self.description_frame.pack_forget()
                self.is_expanded = False
            else:
                # Показываем описание
                if self.description_label is None:
                    self.description_label = ttk.Label(
                        self.description_frame,
                        text=self.description,
                        wraplength=800,
                        font=("Segoe UI", 9),
                        foreground="#666666",
                        anchor="w",
                        justify="left"
                    )
                    self.description_label.pack(fill="x", pady=(5, 0), anchor="w")
                self.description_frame.pack(fill="x", pady=(5, 0))
                self.is_expanded = True
    
    def _get_description(self):
        """Получает описание из descriptions.txt или файла"""
        try:
            # Пробуем загрузить из descriptions.txt
            descriptions = {}
            with open("tweaks//descriptions.txt", "r", encoding="utf-8") as f:
                for line in f:
                    if "=" in line:
                        key, value = line.strip().split("=", 1)
                        descriptions[key] = value
            
            file_name = os.path.basename(self.checkbox_name)
            if file_name in descriptions:
                return descriptions[file_name]
            
            # Ищем частичное совпадение
            for key in descriptions:
                if key in file_name or file_name in key:
                    return descriptions[key]
            
            # Если не найдено, возвращаем None
            return None
        except Exception:
            return None
    
    def _launch_script(self):
        """Запускает скрипт, связанный с чекбоксом"""
        if not self.checkbox_var.get():
            # Если чекбокс не выбран, выбираем его
            self.checkbox_var.set(True)
        
        # Получаем путь к скрипту
        tab_name = self.tab_name
        button_name = get_button_name(tab_name)
        tweak_path = f"tweaks\\{button_name}\\{tab_name}\\{self.checkbox_name}"
        
        # Проверяем существование файла
        if not os.path.exists(tweak_path):
            logger.log_error(f"Файл не найден: {tweak_path}")
            return
        
        try:
            # Запускаем скрипт в зависимости от расширения
            if self.checkbox_name.endswith((".bat", ".cmd")):
                subprocess.Popen(f'cmd /c "{tweak_path}"', shell=True)
            elif self.checkbox_name.endswith(".exe"):
                subprocess.Popen(f'"{tweak_path}"', shell=True)
            elif self.checkbox_name.endswith(".ps1"):
                subprocess.Popen([
                    "powershell.exe",
                    "-ExecutionPolicy", "Bypass",
                    "-File", tweak_path
                ])
            elif self.checkbox_name.endswith(".reg"):
                subprocess.Popen(f'reg import "{tweak_path}"', shell=True)
            elif self.checkbox_name.endswith(".pow"):
                subprocess.Popen(f'powercfg /import "{tweak_path}"', shell=True)
            else:
                subprocess.Popen(f'cmd /c "{tweak_path}"', shell=True)
            
            logger.log_info(f"Запущен скрипт: {self.checkbox_name}")
        except Exception as e:
            logger.log_error(f"Ошибка при запуске скрипта {self.checkbox_name}: {str(e)}")


def create_tab_content(
    tab_name, tab_frame, checkbox_names
):  # Функция для создания содержимого вкладки
    # Очищаем существующее содержимое вкладки
    for widget in tab_frame.winfo_children():  # Проходим по всем виджетам на вкладке
        widget.destroy()  # Удаляем виджет

    # Создаем основной контейнер для вкладки
    main_container = ttk.Frame(tab_frame)  # Создаем основной контейнер для вкладки
    main_container.pack(
        fill=tk.BOTH, expand=True
    )  # Упаковываем основной контейнер для вкладки

    # Словарь с описаниями вкладок (показываются всегда)
    tab_descriptions = {
        'Бэкап': '💾 Создание резервных копий системы и реестра. Рекомендуется делать бэкап перед применением любых изменений, чтобы иметь возможность вернуть систему в исходное состояние.',
        'Обновления': '🔄 Управление обновлениями Windows. Вы можете включить или отключить автоматические обновления системы, а также удалить уже скачанные файлы обновлений.',
        'Поддержка': '☕ Способы поддержать разработчика проекта. Ваша поддержка помогает развивать Extreme Tweaker и добавлять новые функции.',
        'Активаторы': '🔑 Инструменты для активации Windows. Различные методы активации системы для всех версий Windows.',
        'Анонимность': '🔒 Максимальная конфиденциальность и анонимность. Отключение телеметрии, блокировка слежки и защита приватности.',
        'Приватность': '🛡️ Настройки приватности и безопасности. Отключение телеметрии, защита данных и контроль над сбором информации.',
        'Оптимизация MartyFiles': '⚡ Базовые настройки для оптимизации системы. Безопасные твики для улучшения производительности без риска для стабильности.',
        'Безопасная оптимизация': '🛡️ Оптимизация системы с акцентом на безопасность. Включает настройки DirectX, отключение телеметрии и оптимизацию для игр без потери стабильности.',
        'Основная оптимизация': '🚀 Основные настройки для повышения производительности. Включает отключение ненужных функций Windows, оптимизацию для игр и улучшение отзывчивости системы.',
        'Углубленная оптимизация': '⚙️ Продвинутые настройки для опытных пользователей. Изменяет параметры системы на более глубоком уровне для максимальной производительности.',
        'Максимальная оптимизация': '🔥 Экстремальная оптимизация для максимальной производительности. Включает агрессивные настройки, которые могут повлиять на стабильность системы.',
        'Меньшая задержка ввода и более плавный игровой процесс': '⚡ Настройки приоритетов процессов для уменьшения задержки ввода и улучшения плавности игрового процесса.',
        'Настройка от de3nake': '🎯 Продвинутые настройки от эксперта de3nake. Оптимизация задержек, таймеров и системных параметров для игр.',
        'Оптимизация программ': '🎮 Оптимизация конкретных программ и игр. Настройки для браузеров, игр (CS2, Fortnite, Valorant) и других приложений для лучшей производительности.',
        'Остальное': '📦 Дополнительные твики и настройки. Различные оптимизации, которые не вошли в другие категории.',
        'Службы': '⚙️ Управление службами Windows. Отключение ненужных служб для повышения производительности и освобождения ресурсов.',
        'Хардкор оптимизация': '💀 Экстремальная оптимизация для опытных пользователей. Агрессивные настройки, которые могут нарушить работу некоторых функций Windows.',
        'BIOS': '🔧 Настройки BIOS через Extreme Tweaker. Изменение параметров BIOS без перезагрузки в BIOS меню.',
        'BSD': '📝 Настройки BCD (Boot Configuration Data). Твики загрузчика Windows для оптимизации запуска системы.',
        'DirectX': '🎮 Оптимизация DirectX и OpenGL. Настройки графических API для улучшения производительности в играх.',
        'Hyper-V': '🖥️ Управление виртуализацией Hyper-V. Отключение или настройка виртуализации для повышения производительности.',
        'Звук': '🔊 Оптимизация звуковой подсистемы. Настройки для уменьшения задержки аудио и улучшения качества звука.',
        'Клавиатура': '⌨️ Оптимизация клавиатуры. Настройки для уменьшения задержки ввода с клавиатуры.',
        'МАКСИМАЛЬНАЯ ГЕРЦОВКА': '⚡ Максимальная частота таймера системы. Экстремальные настройки для минимальных задержек.',
        'Мышка': '🖱️ Оптимизация мыши. Настройки для уменьшения задержки мыши и улучшения отклика.',
        'Оптимизация Amd': '🔴 Оптимизация для процессоров AMD. Специальные настройки для процессоров AMD Ryzen и других.',
        'Оптимизация Intel': '🔵 Оптимизация для процессоров Intel. Специальные настройки для процессоров Intel Core.',
        'Оптимизация Nvidia': '🟢 Оптимизация видеокарт NVIDIA. Настройки драйверов и параметров видеокарт NVIDIA.',
        'Память': '💾 Оптимизация оперативной памяти. Настройки управления памятью для разных объемов RAM.',
        'Сеть': '🌐 Оптимизация сетевых настроек. Уменьшение пинга, оптимизация TCP/IP и сетевых драйверов.',
        'Твики': '⚙️ Различные системные твики. Оптимизация CPU, GPU, USB и других компонентов системы.',
        'Адские режимы электропитания': '⚡ Экстремальные схемы электропитания. Максимальная производительность ценой энергопотребления.',
        'Все планы электропитания': '🔋 Полная коллекция схем электропитания. Все доступные планы для разных сценариев использования.',
        'Классика': '📚 Проверенные временем твики и схемы электропитания из All Tweaker.',
        'Популярные режимы электропитания': '⭐ Самые популярные схемы электропитания. Рекомендуемые планы для игр и производительности.',
        'Схемы AMD&INTEL': '🔴🔵 Специальные схемы для процессоров AMD и Intel. Оптимизированные планы электропитания для разных процессоров.',
        'Схемы где ЗАГРУЖЕННОСТЬ ПРОЦЕССОРА 100%': '💯 Схемы с максимальной загрузкой процессора. Планы для максимальной производительности CPU.',
        'Исправление проблем': '🔧 Инструменты для исправления проблем. Восстановление функций Windows после применения твиков.',
        'Отмена': '↩️ Отмена примененных твиков. Возврат настроек к значениям по умолчанию.',
        'Классическая очистка': '🧹 Очистка системы от временных файлов, кэша и мусора. Безопасные инструменты для освобождения места на диске и улучшения производительности.',
        'Очистка': '🗑️ Дополнительные инструменты очистки. Удаление временных файлов, логов и кэша.',
        'Удалить приложения': '📦 Удаление встроенных приложений Windows. Удаление ненужных UWP-приложений и компонентов.',
        'Паки': '📦 Готовые наборы твиков. Комплексные пакеты оптимизации от разных авторов.',
        'Программы': '💻 Установка и оптимизация сторонних программ. Настройки для популярных приложений.',
        'Сеть': '🌐 Дополнительные сетевые настройки. Оптимизация интернет-соединения и сетевых параметров.',
        'Кастомизация': '🎨 Настройка внешнего вида Windows. Изменение интерфейса, цветов, иконок и других визуальных элементов системы под ваши предпочтения.',
        'Обновления': '🔄 Управление обновлениями Extreme Tweaker и Windows. Обновление программы и настройки обновлений системы.',
        'Average': '📊 Средний уровень оптимизации. Сбалансированные настройки для большинства пользователей.',
        'Base': '🏠 Базовые настройки. Основные твики для начала оптимизации.',
        'fix mouse': '🖱️ Исправление проблем с мышью. Настройки для устранения проблем с откликом мыши.',
        'Hard': '💀 Жесткая оптимизация. Агрессивные настройки для опытных пользователей.',
        'setting kenma - bro its heavy': '⚡ Экстремальная оптимизация от kenma. Максимальная производительность.',
        'setting kenma v2 - bro its heavy': '⚡ Экстремальная оптимизация от kenma v2. Улучшенная версия.',
        'setting qqnwr': '🎯 Специальные настройки qqnwr. Оптимизация для конкретных сценариев.',
        'Терапия после обновлений винды': '💊 Восстановление настроек после обновлений Windows. Возврат оптимизаций после системных обновлений.'
    }
    
    # Словарь с советами для разных вкладок (разные советы для разных вкладок)
    tab_tips = {
        'Бэкап': '💡 Совет: Создайте бэкап реестра перед применением любых изменений!',
        'Обновления': '💡 Совет: После обновления Windows используйте вкладку "Терапия после обновлений" для восстановления оптимизаций.',
        'Поддержка': '💡 Совет: Ваша поддержка помогает развивать проект и добавлять новые функции!',
        'Анонимность': '💡 Совет: Комбинируйте разные твики для максимальной приватности.',
        'Приватность': '💡 Совет: Начните с базовых твиков от DE3NAKE для безопасной настройки.',
        'Оптимизация MartyFiles': '💡 Совет: Эти твики безопасны и подходят для начинающих.',
        'Безопасная оптимизация': '💡 Совет: Рекомендуется для большинства пользователей - баланс производительности и стабильности.',
        'Основная оптимизация': '💡 Совет: Хороший выбор для геймеров - заметный прирост FPS без потери функциональности.',
        'Углубленная оптимизация': '⚠️ Внимание: Для опытных пользователей! Может повлиять на стабильность системы.',
        'Максимальная оптимизация': '⚠️ Внимание: Экстремальные настройки! Используйте только если понимаете последствия.',
        'Меньшая задержка ввода и более плавный игровой процесс': '💡 Совет: Выберите настройку в зависимости от ваших предпочтений - баланс или минимальная задержка.',
        'Настройка от de3nake': '💡 Совет: Эти настройки от эксперта - используйте для максимальной производительности в играх.',
        'Оптимизация программ': '💡 Совет: Выберите твики для конкретных программ, которые вы используете.',
        'Остальное': '💡 Совет: Здесь собраны дополнительные твики - используйте с осторожностью.',
        'Службы': '⚠️ Внимание: Отключение служб может нарушить работу некоторых функций Windows!',
        'Хардкор оптимизация': '💀 Внимание: Только для опытных! Может серьезно повлиять на работу системы.',
        'BIOS': '⚠️ Внимание: Изменение настроек BIOS может повлиять на стабильность системы!',
        'DirectX': '💡 Совет: Настройки DirectX особенно важны для игр - начните с базовых оптимизаций.',
        'Звук': '💡 Совет: Настройки звука помогут уменьшить задержку аудио в играх и приложениях.',
        'Клавиатура': '💡 Совет: Уменьшение задержки клавиатуры особенно важно для соревновательных игр.',
        'Мышка': '💡 Совет: Оптимизация мыши критична для FPS игр - начните с базовых настроек.',
        'Оптимизация Nvidia': '💡 Совет: Настройки NVIDIA помогут выжать максимум из вашей видеокарты.',
        'Память': '💡 Совет: Выберите настройку в зависимости от объема вашей оперативной памяти.',
        'Сеть': '💡 Совет: Сетевые оптимизации помогут уменьшить пинг в онлайн-играх.',
        'Классическая очистка': '💡 Совет: Регулярная очистка системы поможет поддерживать производительность.',
        'Кастомизация': '💡 Совет: Настройте внешний вид Windows под свои предпочтения!',
        'Исправление проблем': '💡 Совет: Если что-то пошло не так, используйте эти инструменты для восстановления.',
        'Отмена': '💡 Совет: Используйте для возврата настроек к значениям по умолчанию.'
    }

    # Проверяем режим новичка и показываем описание вкладки
    novice_mode = config.getboolean("General", "novice_mode", fallback=False)
    # if novice_mode and tab_name in tab_descriptions:
    
    # Показываем описание вкладки всегда (не только в режиме новичка)
    if tab_name in tab_descriptions:
        # Создаем информационный фрейм с описанием вкладки
        info_frame = ttk.Labelframe(main_container, text="ℹ️ Описание вкладки", padding=15)
        info_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        description_label = ttk.Label(
            info_frame,
            text=tab_descriptions[tab_name],
            font=("Segoe UI", 10),
            wraplength=1200,
            justify="left",
            foreground="#32FBE2"
        )
        description_label.pack(anchor="w")
        
        # Добавляем подсказку (разные советы для разных вкладок)
        if tab_name in tab_tips:
            tip_label = ttk.Label(
                info_frame,
                text=tab_tips[tab_name],
                font=("Segoe UI", 9),
                wraplength=1200,
                justify="left",
                foreground="#888888"
            )
            tip_label.pack(anchor="w", pady=(8, 0))

    # Создаем фрейм для поиска
    search_frame = ttk.Frame(main_container)
    search_frame.pack(fill="x", padx=10, pady=(20, 5))

    # Создаем поле поиска
    search_var = tk.StringVar()
    search_entry = ttk.Entry(
        search_frame, textvariable=search_var, font=("Segoe UI", 10)
    )
    search_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
    
    # Добавляем подсказку для новичков в поле поиска вкладки
    if novice_mode:
        placeholder_text = "Поиск... (Введите название твика)"
        search_entry.insert(0, placeholder_text)
        
        def on_search_focus_in(event):
            current_text = search_entry.get()
            if current_text == placeholder_text:
                search_entry.delete(0, "end")
        
        def on_search_focus_out(event):
            current_text = search_entry.get()
            if current_text == "":
                search_entry.insert(0, placeholder_text)
        
        search_entry.bind("<FocusIn>", on_search_focus_in)
        search_entry.bind("<FocusOut>", on_search_focus_out)
    else:
        search_entry.insert(0, "Поиск...")

    # Создаем кнопку поиска
    search_button = ttk.Button(search_frame, text="Поиск", bootstyle="info-outline")
    # search_button.pack(side='right')

    # Создаем канвас с вертикальным и горизонтальным скроллбарами
    canvas = tk.Canvas(main_container)  # Создаем канвас

    # Создаем вертикальный скроллбар
    v_scrollbar = ttk.Scrollbar(
        main_container, orient=tk.VERTICAL, command=canvas.yview
    )  # Создаем вертикальный скроллбар
    v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # Упаковываем вертикальный скроллбар

    # Создаем горизонтальный скроллбар
    h_scrollbar = ttk.Scrollbar(
        tab_frame, orient=tk.HORIZONTAL, command=canvas.xview
    )  # Создаем горизонтальный скроллбар
    h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)  # Упаковываем горизонтальный скроллбар

    # Размещаем канвас
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # Упаковываем канвас

    # Настраиваем привязку скроллбаров к холсту
    canvas.configure(
        xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set
    )  # Настраиваем привязку скроллбаров к холсту

    # Создаем внутренний фрейм для контента
    inner_frame = ttk.Frame(canvas)  # Создаем внутренний фрейм для контента
    canvas_window = canvas.create_window(
        (0, 0), window=inner_frame, anchor="nw"
    )  # Создаем окно для внутреннего фрейма

    # Функция для обновления области прокрутки
    def configure_scroll_region(event):
        canvas.configure(scrollregion=canvas.bbox("all"))  # Обновляем область прокрутки
        # Устанавливаем ширину окна канваса равной ширине внутреннего фрейма или канваса (что больше)
        canvas.itemconfig(
            canvas_window, width=max(inner_frame.winfo_reqwidth(), canvas.winfo_width())
        )  # Устанавливаем ширину окна канваса равной ширине внутреннего фрейма или канваса (что больше)

    # Функция для обработки изменения размера холста
    def configure_canvas(event):
        canvas.itemconfig(
            canvas_window, width=event.width
        )  # Устанавливаем ширину окна канваса равной ширине внутреннего фрейма или канваса (что больше)

    # Функция для прокрутки колесиком мыши
    def on_mousewheel(event):
        # Горизонтальная прокрутка при Shift
        if hasattr(event, "state") and (event.state == 1 or event.state & 0x1):
            if event.num == 5 or event.delta == -120:
                canvas.xview_scroll(1, "units")
            elif event.num == 4 or event.delta == 120:
                canvas.xview_scroll(-1, "units")
            elif event.delta == -1:
                canvas.xview_scroll(1, "units")
            elif event.delta == 1:
                canvas.xview_scroll(-1, "units")
        else:
            # Вертикальная прокрутка
            if event.num == 5 or event.delta == -120:
                canvas.yview_scroll(1, "units")
            elif event.num == 4 or event.delta == 120:
                canvas.yview_scroll(-1, "units")
            elif event.delta == -1:
                canvas.yview_scroll(1, "units")
            elif event.delta == 1:
                canvas.yview_scroll(-1, "units")

    # Для Linux: отдельные обработчики для Shift+Button-4/5
    def on_shift_button4(event):
        canvas.xview_scroll(-1, "units")

    def on_shift_button5(event):
        canvas.xview_scroll(1, "units")

    # Привязываем обработчики событий
    inner_frame.bind("<Configure>", configure_scroll_region)
    canvas.bind("<Configure>", configure_canvas)

    # Прокрутка колесиком мыши (Windows/Mac)
    canvas.bind("<Enter>", lambda e: canvas.focus_set())
    canvas.bind("<MouseWheel>", on_mousewheel)
    # Прокрутка колесиком мыши (Linux)
    canvas.bind("<Button-4>", on_mousewheel)
    canvas.bind("<Button-5>", on_mousewheel)
    # Горизонтальная прокрутка с Shift (Linux)
    canvas.bind("<Shift-Button-4>", on_shift_button4)
    canvas.bind("<Shift-Button-5>", on_shift_button5)
    # Также для inner_frame (если мышь над чекбоксами)
    inner_frame.bind("<MouseWheel>", on_mousewheel)
    inner_frame.bind("<Button-4>", on_mousewheel)
    inner_frame.bind("<Button-5>", on_mousewheel)
    inner_frame.bind("<Shift-Button-4>", on_shift_button4)
    inner_frame.bind("<Shift-Button-5>", on_shift_button5)
    
    # Функция для привязки колесика мыши ко всем виджетам внутри checkboxes_frame
    def bind_mousewheel_to_widgets(parent_widget):
        """Рекурсивно привязывает колесико мыши ко всем виджетам"""
        for widget in parent_widget.winfo_children():
            widget.bind("<MouseWheel>", on_mousewheel)
            widget.bind("<Button-4>", on_mousewheel)
            widget.bind("<Button-5>", on_mousewheel)
            widget.bind("<Shift-Button-4>", on_shift_button4)
            widget.bind("<Shift-Button-5>", on_shift_button5)
            # Рекурсивно обрабатываем дочерние виджеты
            if hasattr(widget, 'winfo_children'):
                bind_mousewheel_to_widgets(widget)

    # Получаем количество колонок из конфига или используем значение по умолчанию
    num_columns = config.getint(
        "Columns", tab_name, fallback=config.getint("Columns", "default", fallback=3)
    )  # Получаем количество колонок из конфига или используем значение по умолчанию

    # Создаем фрейм для чекбоксов с отступами
    checkboxes_frame = ttk.Frame(inner_frame)
    checkboxes_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Получаем режим отображения из настроек
    display_mode = config.get("General", "checkbox_display_mode", fallback="regular")
    
    # Создаем чекбоксы
    for i, checkbox_name in enumerate(checkbox_names):  # Проходим по всем чекбоксам
        if checkbox_name.strip():  # Если чекбокс не пустой
            checkbox_var = tk.BooleanVar()  # Создаем переменную для чекбокса
            # Получаем имя папки через get_button_name для правильного формирования пути
            button_name = get_button_name(tab_name)
            # Проверяем, является ли это вкладкой из tabs_mini
            is_mini_tab = tabs_mini and tab_name in tabs_mini
            if button_name and not is_mini_tab:
                # Для обычных вкладок используем button_name/tab_name
                filepath = f"tweaks//{button_name}//{tab_name}//{checkbox_name}"  # Получаем путь к файлу
            else:
                # Для минималистичных вкладок или если button_name пустой, используем tab_name напрямую
                filepath = f"tweaks//{tab_name}//{checkbox_name}"  # Получаем путь к файлу
            
            # Проверяем режим отображения
            if display_mode == "expandable":
                # Создаем виджет в виде широкого прямоугольника с раскрывающимся описанием (BoosterX)
                checkbox = ExpandableWideRectangleCheckbox(
                    checkboxes_frame,
                    checkbox_name,
                    checkbox_var,
                    tab_name,
                    filepath
                )
                checkbox.grid(
                    row=i,
                    column=0,
                    columnspan=num_columns,
                    sticky="ew",
                    padx=10,
                    pady=5,
                )  # Упаковываем виджет на всю ширину
            elif display_mode == "sapphire":
                # Создаем виджет в виде широкого прямоугольника с раскрывающимся описанием (в два столбца)
                checkbox = SapphireCheckbox(
                    checkboxes_frame,
                    checkbox_name,
                    checkbox_var,
                    tab_name,
                    filepath
                )
                # В режиме Sapphire размещаем в два столбца
                row = i // 2
                col = i % 2
                checkbox.grid(
                    row=row,
                    column=col,
                    sticky="ew",
                    padx=10,
                    pady=5,
                )
                # Настраиваем веса колонок для двух столбцов
                checkboxes_frame.grid_columnconfigure(0, weight=1)
                checkboxes_frame.grid_columnconfigure(1, weight=1)
            elif display_mode == "rectangle":
                # Создаем виджет в виде прямоугольника
                checkbox = RectangleCheckbox(
                    checkboxes_frame,
                    checkbox_name,
                    checkbox_var,
                    tab_name,
                    filepath
                )
                checkbox.grid(
                    row=i // num_columns,
                    column=i % num_columns,
                    sticky="nsew",
                    padx=10,
                    pady=10,
                )  # Упаковываем виджет
            else:
                # Создаем обычный чекбокс
                checkbox = ttk.Checkbutton(
                    checkboxes_frame,
                    text=checkbox_name,
                    variable=checkbox_var,
                    style="Custom.TCheckbutton",
                )  # Создаем чекбокс
                checkbox.grid(
                    row=i // num_columns,
                    column=i % num_columns,
                    sticky="w",
                    padx=10,
                    pady=5,
                )  # Упаковываем чекбокс
                ToolTip(checkbox, filepath)  # Добавляем подсказку к чекбоксу
            
            checkboxes[checkbox_name] = (
                checkbox_var  # Добавляем переменную для чекбокса в словарь
            )
        else:  # Если чекбокс пустой
            placeholder = ttk.Label(
                checkboxes_frame, text="", width=3
            )  # Создаем placeholder
            placeholder.grid(
                row=i // num_columns,
                column=i % num_columns,
                sticky="w",
                padx=10,
                pady=5,
            )  # Упаковываем placeholder

    # Функция для фильтрации чекбоксов
    def filter_checkboxes(*args):
        search_text = search_var.get().lower()
        # Игнорируем placeholder текст
        if search_text == "поиск...":
            search_text = ""
        
        for widget in checkboxes_frame.winfo_children():
            # Проверяем как обычные чекбоксы, так и RectangleCheckbox
            if isinstance(widget, ttk.Checkbutton):
                if search_text in widget.cget("text").lower():
                    widget.grid()
                else:
                    widget.grid_remove()
            elif isinstance(widget, RectangleCheckbox):
                if search_text in widget.checkbox_name.lower():
                    widget.grid()
                else:
                    widget.grid_remove()
            elif isinstance(widget, ExpandableWideRectangleCheckbox):
                if search_text in widget.checkbox_name.lower():
                    widget.grid()
                else:
                    widget.grid_remove()
            elif isinstance(widget, SapphireCheckbox):
                if search_text in widget.checkbox_name.lower():
                    widget.grid()
                else:
                    widget.grid_remove()
            # Обрабатываем placeholder (пустые метки)
            elif isinstance(widget, ttk.Label) and widget.cget("text") == "":
                # Показываем placeholder только если поиск пустой
                if search_text:
                    widget.grid_remove()
                else:
                    widget.grid()

    # Привязываем функцию фильтрации к изменению текста в поле поиска
    search_var.trace("w", filter_checkboxes)
    search_button.config(command=lambda: filter_checkboxes())

    # Обновляем размеры и конфигурацию прокрутки
    inner_frame.update_idletasks()  # Обновляем размеры и конфигурацию прокрутки
    canvas.config(
        scrollregion=canvas.bbox("all")
    )  # Обновляем размеры и конфигурацию прокрутки

    # Устанавливаем минимальный размер для внутреннего фрейма
    inner_frame.grid_columnconfigure(
        num_columns - 1, weight=1
    )  # Устанавливаем минимальный размер для внутреннего фрейма
    
    # Если режим прямоугольников, настраиваем равномерное распределение колонок
    if display_mode == "rectangle":
        for col in range(num_columns):
            checkboxes_frame.grid_columnconfigure(col, weight=1, uniform="rect_cols")
    
    # Привязываем колесико мыши ко всем виджетам внутри checkboxes_frame
    bind_mousewheel_to_widgets(checkboxes_frame)


def create_consolidated_optimization_tab(parent, tabs_dict, config, button_name="Оптимизация"):
    main = ttk.Frame(parent)
    main.pack(fill="both", expand=True)

    top_actions = ttk.Frame(main)
    top_actions.pack(fill="x", padx=10, pady=(10, 5))

    all_vars = {}

    def select_all():
        for var in all_vars.values():
            var.set(True)

    def deselect_all():
        for var in all_vars.values():
            var.set(False)

    select_all_btn = ttk.Button(
        top_actions, text="Выбрать все твики",
        bootstyle="primary-outline", command=select_all, width=22
    )
    select_all_btn.pack(side="left", padx=(0, 5))

    deselect_all_btn = ttk.Button(
        top_actions, text="Снять все",
        bootstyle="secondary-outline", command=deselect_all, width=15
    )
    deselect_all_btn.pack(side="left", padx=(0, 5))

    canvas = tk.Canvas(main, highlightthickness=0, height=400)
    h_scrollbar = ttk.Scrollbar(main, orient=tk.HORIZONTAL, command=canvas.xview)
    scrollable = ttk.Frame(canvas)

    scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable, anchor="nw")
    canvas.configure(xscrollcommand=h_scrollbar.set)

    canvas.pack(side="top", fill="both", expand=True, padx=10, pady=(0, 0))
    h_scrollbar.pack(side="bottom", fill="x", padx=10)

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

    num_cols = config.getint("Columns", "default", fallback=3)
    display_mode = config.get("General", "checkbox_display_mode", fallback="regular")
    show_full_path = config.getboolean("General", "show_checkbox_full_path", fallback=True)

    for tab_name, checkbox_names in tabs_dict.items():
        section = ttk.Labelframe(scrollable, text=f" {tab_name} ", padding=8)
        section.pack(side="left", fill="y", padx=(0, 10), anchor="n")

        section_header = ttk.Frame(section)
        section_header.pack(fill="x", pady=(0, 4))

        sel_var = tk.BooleanVar(value=False)

        section_cb = ttk.Checkbutton(
            section_header, text="Выбрать всё",
            variable=sel_var, bootstyle="primary-round-toggle"
        )
        section_cb.pack(side="left")

        grid_frame = ttk.Frame(section)
        grid_frame.pack(fill="x")

        row = 0
        col = 0
        section_vars = {}

        for checkbox_name in checkbox_names:
            if not checkbox_name.strip():
                continue

            display_name = checkbox_name if show_full_path else os.path.basename(checkbox_name)
            display_name = os.path.splitext(display_name)[0]
            var = tk.BooleanVar(value=False)
            all_vars[checkbox_name] = var
            section_vars[checkbox_name] = var

            if display_mode == "rectangle":
                cb = RectangleCheckbox(grid_frame, display_name, var, "", "")
                cb.grid(row=row, column=col, sticky="nsew", padx=3, pady=2)
            elif display_mode == "expandable":
                cb = ExpandableWideRectangleCheckbox(grid_frame, display_name, var, "", "")
                cb.grid(row=row, column=col, columnspan=num_cols, sticky="nsew", padx=3, pady=2)
                col += num_cols
            elif display_mode == "sapphire":
                cb = SapphireCheckbox(grid_frame, display_name, var, "", "")
                cb.grid(row=row, column=col, columnspan=max(1, num_cols // 2), sticky="nsew", padx=3, pady=2)
                col += max(1, num_cols // 2)
            else:
                cb = ttk.Checkbutton(
                    grid_frame, text=display_name,
                    variable=var, style="Custom.TCheckbutton"
                )
                cb.grid(row=row, column=col, sticky="w", padx=5, pady=1)

            col += 1
            if col >= num_cols:
                col = 0
                row += 1

        if display_mode in ("rectangle", "expandable", "sapphire"):
            for c in range(num_cols):
                grid_frame.grid_columnconfigure(c, weight=1, uniform=f"sect_{tab_name}")

        svars = section_vars.copy()
        section_cb.config(command=lambda sv=sel_var, svars=svars: [v.set(sv.get()) for v in svars.values()])

    bind_mw(scrollable)

    bottom_frame = ttk.Frame(main)
    bottom_frame.pack(fill="x", padx=10, pady=(5, 10))

    def apply_all():
        selected = []
        for checkbox_name, var in all_vars.items():
            if var.get():
                for tn, names in tabs_dict.items():
                    if checkbox_name in names:
                        filepath = os.path.join("tweaks", button_name, tn, checkbox_name)
                        selected.append(filepath)
                        break

        if not selected:
            messagebox.showinfo("Информация", "Не выбрано ни одного твика")
            return

        count = len(selected)
        if not messagebox.askyesno("Подтверждение", f"Применить {count} выбранных твиков?"):
            return

        success = 0
        for filepath in selected:
            try:
                if not os.path.exists(filepath):
                    continue
                if filepath.endswith('.ps1'):
                    subprocess.Popen(['powershell.exe', '-ExecutionPolicy', 'Bypass', '-File', filepath])
                elif filepath.endswith('.reg'):
                    subprocess.Popen(f'reg import "{filepath}"', shell=True)
                elif filepath.endswith('.pow'):
                    subprocess.Popen(f'powercfg /import "{filepath}"', shell=True)
                else:
                    subprocess.Popen(f'Utils\\launcher.exe "{filepath}"', shell=True)
                success += 1
            except Exception as e:
                print(f"Ошибка при запуске {filepath}: {e}")

        messagebox.showinfo("Результат", f"✅ {success}/{count} выполнено")

    # apply_btn = ttk.Button(
    #     bottom_frame, text="Применить выбранные",
    #     bootstyle="success-outline", command=apply_all, width=22
    # )
    # apply_btn.pack(side="right")

    main.all_vars = all_vars
    main.apply_all = apply_all
    return main


"""
+------------------------------------+
| Функция для подтверждения          |
| переключения вкладки               |
+------------------------------------+
"""


def confirm_switch_tab(target_function):
    """Функция для подтверждения переключения вкладки"""
    # Проверяем настройку confirm_switch_tab_enabled
    if not config.getboolean("General", "confirm_switch_tab_enabled", fallback=True):
        target_function()
        return
    
    # Проверяем, есть ли выбранные чекбоксы
    selected_checkboxes = [name for name, var in checkboxes.items() if var.get()]

    if selected_checkboxes:
        # Создаем диалоговое окно подтверждения
        dialog = tk.Toplevel(root)
        dialog.title("Предупреждение")
        dialog.geometry("400x150")
        dialog.transient(root)
        dialog.grab_set()

        # Центрируем окно
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry("{}x{}+{}+{}".format(width, height, x, y))

        # Добавляем сообщение
        message = ttk.Label(
            dialog,
            text="У вас есть несохраненные изменения.\nХотите продолжить?",
            font=("Segoe UI", 10),
            justify="center",
        )
        message.pack(pady=20)

        # Фрейм для кнопок
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)

        def on_confirm():
            dialog.destroy()
            target_function()

        def on_cancel():
            dialog.destroy()

        # Кнопки
        confirm_button = ttk.Button(
            button_frame,
            text="Продолжить",
            command=on_confirm,
            bootstyle="success-outline",
        )
        confirm_button.pack(side="left", padx=5)

        cancel_button = ttk.Button(
            button_frame, text="Отмена", command=on_cancel, bootstyle="danger-outline"
        )
        cancel_button.pack(side="left", padx=5)

        # Устанавливаем фокус на кнопку отмены
        cancel_button.focus_set()

        # Ждем, пока окно будет закрыто
        dialog.wait_window()
    else:
        # Если нет выбранных чекбоксов, просто переключаемся
        target_function()


"""
+------------------------------------+
| Функция для переключения на        |
| главные вкладки                    |
+------------------------------------+
"""


def _read_output(process, config_name):
    """Вспомогательная функция для чтения вывода процесса в отдельном потоке"""
    try:
        for line in iter(process.stdout.readline, ''):
            if line:
                line = line.strip()
                if line:
                    logger.log_info(f"[{config_name}] {line}")
    except Exception as e:
        logger.log_error(f"Ошибка при чтении вывода процесса '{config_name}': {str(e)}")


def execute_with_logging(command, config_name, file_path=None, wait=True):
    """Выполняет команду с перехватом вывода консоли и логированием"""
    try:
        logger.log_info(f"Запуск конфига '{config_name}' - команда: {command}")
        if file_path:
            logger.log_info(f"Путь к файлу: {file_path}")
        
        # Выполняем команду с перехватом stdout и stderr
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='replace',
            bufsize=1,
            universal_newlines=True
        )
        
        if wait:
            # Для синхронных процессов читаем вывод в текущем потоке
            output_lines = []
            for line in iter(process.stdout.readline, ''):
                if line:
                    line = line.strip()
                    if line:
                        logger.log_info(f"[{config_name}] {line}")
                        output_lines.append(line)
            
            # Ждем завершения процесса
            process.wait()
            return_code = process.returncode
            
            logger.log_info(f"Конфиг '{config_name}' завершен с кодом возврата: {return_code}")
            if return_code != 0:
                logger.log_warning(f"Конфиг '{config_name}' завершился с ошибкой (код: {return_code})")
            
            return return_code, '\n'.join(output_lines)
        else:
            # Для фоновых процессов читаем вывод в отдельном потоке
            output_thread = threading.Thread(
                target=_read_output,
                args=(process, config_name),
                daemon=True
            )
            output_thread.start()
            logger.log_info(f"Конфиг '{config_name}' запущен в фоновом режиме (PID: {process.pid})")
            return None, None
    except Exception as e:
        error_msg = f"Ошибка при выполнении конфига '{config_name}': {str(e)}"
        logger.log_error(error_msg)
        print(error_msg)
        return None, None

def show_pro_version_dialog(config_name):
    """Показывает диалоговое окно о необходимости Pro версии"""
    try:
        # Создаем кастомное диалоговое окно
        dialog = Toplevel()
        dialog.title("Требуется Pro версия")
        dialog.geometry("450x250")
        dialog.resizable(False, False)
        
        # Центрируем окно
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')
        
        # Делаем окно модальным
        dialog.transient(dialog.master)
        dialog.grab_set()
        
        # Иконка информации
        info_label = Label(dialog, text="ℹ️", font=("Arial", 48), fg="#2196F3")
        info_label.pack(pady=10)
        
        # Заголовок
        title_label = Label(dialog, text="Конфигурации в бесплатной версии", 
                           font=("Arial", 14, "bold"), fg="#1565C0")
        title_label.pack(pady=5)
        
        # Текст сообщения
        message_text = f"Конфигурация '{config_name}' доступна только в PRO версии!\n\n"
        message_text += "Чтобы использовать все конфигурации и расширенные возможности,\n"
        message_text += "приобретите PRO версию Extreme Tweaker."
        
        message_label = Label(dialog, text=message_text, font=("Arial", 10), 
                             justify=tk.CENTER, wraplength=400)
        message_label.pack(pady=10)
        
        # Кнопки
        button_frame = Frame(dialog)
        button_frame.pack(pady=20)
        
        def buy_pro():
            webbrowser.open("https://t.me/all_tweaker")
            dialog.destroy()
        
        def close_dialog():
            dialog.destroy()
        
        # Кнопка покупки
        buy_button = Button(button_frame, text="💰 Приобрести PRO версию", 
                           command=buy_pro, 
                           bg="#4CAF50", fg="white", 
                           font=("Arial", 10, "bold"), padx=20, pady=5)
        buy_button.pack(side=tk.LEFT, padx=5)
        
        # Кнопка закрытия
        close_button = Button(button_frame, text="Закрыть", 
                             command=close_dialog, 
                             bg="#f44336", fg="white", 
                             font=("Arial", 10), padx=20, pady=5)
        close_button.pack(side=tk.LEFT, padx=5)
        
        # Ожидаем закрытия окна
        dialog.wait_window()
        
    except Exception as e:
        print(f"Error showing pro dialog: {e}")
        # Резервный вариант - простой messagebox
        result = messagebox.askyesno(
            "Требуется Pro версия",
            f"Конфигурация '{config_name}' доступна только в PRO версии!\n\nХотите перейти на сайт для приобретения PRO версии?"
        )
        if result:
            webbrowser.open("https://t.me/all_tweaker")

def run_config(config_name):
    """Запускает конфигурацию по имени"""
    logger.log_info(f"=== Запуск конфигурации: {config_name} ===")
    
    # Обработка специального конфига "Максимальная безопасная оптимизация"
    if config_name == "Максимальная безопасная оптимизация":
        # Запускаем все твики из вкладки "Максимальная безопасная оптимизация"
        novice_mode = config.getboolean("General", "novice_mode", fallback=False)
        if novice_mode and "Максимальная безопасная оптимизация" in tabs_novice:
            checkbox_names = tabs_novice["Максимальная безопасная оптимизация"]
            executed_count = 0
            logger.log_info(f"Найдено твиков для выполнения: {len(checkbox_names)}")
            
            for checkbox_name in checkbox_names:
                try:
                    # Формируем путь к скрипту (checkbox_name уже содержит относительный путь)
                    # Пробуем разные варианты путей
                    possible_paths = [
                        f"Configs\\{checkbox_name}",
                        f"user_data\\Configs\\{checkbox_name}",
                    ]
                    
                    tweak_path = None
                    for path in possible_paths:
                        if os.path.exists(path):
                            tweak_path = path
                            break
                    
                    if tweak_path and os.path.exists(tweak_path):
                        logger.log_info(f"Выполнение твика: {checkbox_name} (путь: {tweak_path})")
                        
                        # Выполняем файл в зависимости от расширения
                        if checkbox_name.endswith(('.bat', '.cmd')):
                            command = f'cmd /c "{tweak_path}"'
                            execute_with_logging(command, checkbox_name, tweak_path, wait=False)
                        elif checkbox_name.endswith('.exe'):
                            command = f'"{tweak_path}"'
                            execute_with_logging(command, checkbox_name, tweak_path, wait=False)
                        elif checkbox_name.endswith('.ps1'):
                            # Для PowerShell используем правильный формат команды
                            command = f'powershell.exe -ExecutionPolicy Bypass -File "{tweak_path}"'
                            execute_with_logging(command, checkbox_name, tweak_path, wait=False)
                        elif checkbox_name.endswith('.reg'):
                            command = f'reg import "{tweak_path}"'
                            execute_with_logging(command, checkbox_name, tweak_path, wait=False)
                        elif checkbox_name.endswith('.pow'):
                            command = f'powercfg /import "{tweak_path}"'
                            execute_with_logging(command, checkbox_name, tweak_path, wait=False)
                        executed_count += 1
                    else:
                        logger.log_warning(f"Твик не найден: {checkbox_name}")
                except Exception as e:
                    error_msg = f"Ошибка при выполнении {checkbox_name}: {str(e)}"
                    logger.log_error(error_msg)
                    print(error_msg)
            
            logger.log_info(f"Максимальная безопасная оптимизация применена! Выполнено твиков: {executed_count}")
            messagebox.showinfo("Успех", f"Максимальная безопасная оптимизация применена! Выполнено твиков: {executed_count}")
        else:
            warning_msg = "Максимальная безопасная оптимизация доступна только в режиме новичка"
            logger.log_warning(warning_msg)
            messagebox.showwarning("Предупреждение", warning_msg)
        logger.log_info(f"=== Завершение конфигурации: {config_name} ===")
        return
    
    # Сначала проверяем пользовательские конфиги
    user_config_path = os.path.join("user_data", "Configs", f"{config_name}.bat")
    if os.path.exists(user_config_path):
        logger.log_info(f"Найден пользовательский конфиг: {user_config_path}")
        command = f'"{user_config_path}"'
        return_code, output = execute_with_logging(command, config_name, user_config_path, wait=True)
        logger.log_info(f"=== Завершение конфигурации: {config_name} ===")
        return
    
    # Затем проверяем стандартные конфиги
    config_path = os.path.join("Configs", f"{config_name}.bat")
    if os.path.exists(config_path):
        logger.log_info(f"Найден стандартный конфиг: {config_path}")
        command = f'"{config_path}"'
        return_code, output = execute_with_logging(command, config_name, config_path, wait=True)
        logger.log_info(f"=== Завершение конфигурации: {config_name} ===")
    else:
        # Конфиг не найден - показываем сообщение о Pro версии
        error_msg = f"Файл конфигурации {config_name}.bat не найден ни в user_data/Configs, ни в Configs"
        logger.log_error(error_msg)
        print(error_msg)
        
        # Показываем сообщение о том, что конфиги есть только в Pro версии
        logger.log_info(f"Конфигурация '{config_name}' доступна только в PRO версии")
        show_pro_version_dialog(config_name)


def create_config_buttons(configs_list, parent_frame, columns=3, is_expert=False, is_author=False, 
                         is_active_user=False, is_pro_gamer=False, is_privacy=False, 
                         is_tweaker=False, is_os_build=False, is_user=False):
    """Создает кнопки конфигураций в сетке"""
    
    # Создаем кастомный стиль для оранжевой обводки
    style = ttk.Style()
    style.configure("Orange.TLabelframe", 
                   bordercolor="#f99926",
                   borderwidth=2,
                   relief="solid")
    style.configure("Orange.TLabelframe.Label", 
                   foreground="#D35400",
                   font=("Segoe UI", 10, "bold"))
    
    buttons_frame = ttk.Frame(parent_frame)
    buttons_frame.pack(fill="x", pady=10)
    
    for i, cfg in enumerate(configs_list):
        row = i // columns
        col = i % columns
        
        # Определяем стиль
        if is_author or is_expert or is_active_user or is_pro_gamer or is_privacy or is_tweaker or is_os_build or is_user:
            button_frame = ttk.Labelframe(
                buttons_frame, 
                text=f"⭐ {cfg['name']} ⭐",
                padding=10,
                style="Orange.TLabelframe"
            )
        else:
            button_frame = ttk.Labelframe(
                buttons_frame, 
                text=cfg["name"],
                padding=10
            )
        
        button_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Используем bootstyle из конфига
        btn_style = cfg["bootstyle"]
        
        # Для пользовательских конфигов используем filepath, если он есть
        if is_user and "filepath" in cfg:
            config_path = cfg["filepath"]
            btn = ttk.Button(
                button_frame,
                text=cfg.get("button_text", cfg["name"]),
                width=28,
                bootstyle=btn_style,
                command=lambda path=config_path: subprocess.call([path], shell=True)
            )
        else:
            btn = ttk.Button(
                button_frame,
                text=cfg.get("button_text", cfg["name"]),
                width=50,
                bootstyle=btn_style,
                command=lambda c=cfg["name"]: run_config(c)
            )
        btn.pack(pady=(10, 5), padx=10)

        description = ttk.Label(
            button_frame,
            text=cfg["description"],
            wraplength=320,
            justify="left",
            font=("Segoe UI", 9)
        )
        description.pack(fill="x", expand=True, padx=10, pady=(0, 10))

    # Настраиваем веса колонок
    for i in range(columns):
        buttons_frame.grid_columnconfigure(i, weight=1)
    
    # Настраиваем веса строк
    for i in range((len(configs_list) + columns - 1) // columns):
        buttons_frame.grid_rowconfigure(i, weight=1)


def switch_to_main():
    # Удаляем все существующие вкладки
    for tab in tab_control.tabs():
        tab_control.forget(tab)

    # Вкладка Быстрая оптимизация
    config_tab = ttk.Frame(tab_control)
    tab_control.add(config_tab, text="Быстрая оптимизация")

    config_frame = ttk.Frame(config_tab)    
    config_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Проверяем режим новичка
    novice_mode = config.getboolean("General", "novice_mode", fallback=False)
    
    # Добавляем информационное сообщение для новичков (компактное, не закрывающее интерфейс)
    if novice_mode:
        # Создаем сворачиваемый фрейм для подсказок
        novice_info_frame = ttk.Labelframe(config_frame, text="👋 Добро пожаловать, новичок!", padding=15)
        novice_info_frame.pack(fill="x", pady=(0, 20))
        
        # Компактный текст
        # novice_info_text = """💡 Вы в безопасном режиме. Начните с пресета "Максимальная безопасная оптимизация". Всегда делайте бэкап перед изменениями!"""
        novice_info_text = """🎯 Вы находитесь в режиме новичка - это безопасный режим работы с Extreme Tweaker!

💡 Полезные советы:
• Начните с пресета "Максимальная оптимизация" - он включает только проверенные и безопасные твики
• Перед применением любых изменений рекомендуется создать точку восстановления или бэкап системы
• Используйте поиск для быстрого нахождения нужных твиков
• Каждая вкладка имеет описание - читайте их для понимания назначения твиков
• Если что-то пошло не так, вы всегда можете вернуть изменения через вкладку "Исправления"

⚠️ Помните: Extreme Tweaker изменяет системные настройки. Всегда делайте бэкап перед применением изменений!

✅ В режиме новичка доступны только безопасные твики, которые не могут навредить вашей системе."""
        
        novice_info_label = ttk.Label(
            novice_info_frame,
            text=novice_info_text,
            font=("Segoe UI", 9),
            wraplength=1200,
            justify="left",
            foreground="#32FBE2"
        )
        novice_info_label.pack(anchor="w")

    # Список обычных конфигураций
    standard_configs = [
        {
            "name": "Базовая оптимизация",
            "bootstyle": "success-outline",
            "description": """Базовый набор оптимизаций для улучшения производительности Windows.
            
• Оптимизация служб Windows
• Очистка временных файлов
• Отключение ненужных компонентов
• Базовая настройка системы
• Оптимизация автозагрузки

Рекомендуется для начинающих пользователей.""",
        },
        {
            "name": "Основная оптимизация",
            "bootstyle": "info-outline",
            "description": """Расширенный набор оптимизаций для заметного улучшения производительности.
            
• Оптимизация всех служб Windows
• Глубокая очистка системы
• Отключение ненужных компонентов
• Настройка производительности
• Оптимизация автозагрузки
• Настройка визуальных эффектов
• Оптимизация памяти

Рекомендуется для большинства пользователей.""",
        },
        {
            "name": "Углубленная оптимизация",
            "bootstyle": "warning-outline",
            "description": """Продвинутый набор оптимизаций для максимальной производительности.
            
• Глубокая оптимизация всех служб
• Агрессивная очистка системы
• Отключение всех ненужных компонентов
• Максимальная настройка производительности
• Оптимизация всех системных параметров
• Отключение визуальных эффектов
• Настройка приоритетов процессов
• Оптимизация сети

Для опытных пользователей.""",
        },
        {
            "name": "Максимальная оптимизация",
            "bootstyle": "danger-outline",
            "description": """Экстремальный набор оптимизаций для достижения пиковой производительности.
            
• Полная оптимизация всех служб
• Максимальная очистка системы
• Отключение всех ненужных компонентов
• Экстремальная настройка производительности
• Оптимизация всех системных параметров
• Отключение всех визуальных эффектов
• Настройка приоритетов процессов
• Оптимизация сети и дисков
• Настройка реестра

Только для опытных пользователей!""",
        },
        {
            "name": "Радикальная оптимизация",
            "bootstyle": "dark-outline",
            "description": """Максимальный набор оптимизаций для достижения пиковой производительности.
            
• Глубокая оптимизация всех служб
• Агрессивная очистка системы
• Отключение всех ненужных компонентов
• Максимальная настройка производительности
• Оптимизация всех системных параметров
• Отключение визуальных эффектов
• Настройка приоритетов процессов
• Оптимизация сети и дисков
• Настройка реестра
• Отключение всех ненужных функций

ВНИМАНИЕ: Используйте только если вы уверены в своих действиях!""",
        }
    ]

    # Оптимизации от авторов (socde18, Антон, Олег AMPR) и экспертов Windows
    author_configs = [
        {
            "name": "Оптимизация от socde18",
            "bootstyle": "success-outline",
            "description": """⭐ ОПТИМИЗАЦИЯ ОТ АВТОРА ⭐

Категория: ✅ БЕЗОПАСНАЯ + ⭐ ЛУЧШАЯ (рекомендуется)

Что это:
Сбалансированный набор твиков, ориентированный на повышение отзывчивости Windows без “ломающих” изменений.

Что делает:
• Ускорение и “очистка” Windows без радикального вырезания компонентов
• Отключение второстепенных фоновых вещей (телеметрия/реклама/виджеты — где уместно)
• Настройки для более стабильного отклика интерфейса

Кому подходит:
• Всем пользователям (хорошая отправная точка)

Совет:
Если не знаешь с чего начать — начинай с этого конфига.""",
            "is_author": True,
        },
        {
        "name": "Оптимизация от Антона",
        "bootstyle": "danger-outline",
        "description": """⚡ ОПТИМИЗАЦИЯ ОТ АВТОРА ⚡

Категория: ⚠️ ОПАСНАЯ (максимально агрессивная)

Что внутри:
• Эксклюзивные настройки SHQBA для Fortnite и других конкурентных игр
• Патчи kHz и низкоуровневые оптимизации задержки ввода
• Полный контроль над приоритетами процессов (CSRSS, lsass, Winlogon)
• Агрессивное отключение телеметрии, служб и фоновых процессов

Почему "опасная":
• Глубокое вмешательство в системные процессы может привести к нестабильности
• Отключение критических служб безопасности
• Изменения на уровне драйверов и ядра системы
• Необратимые изменения в реестре

⚠️ Только для опытных пользователей с полным бэкапом системы!""",
        "is_author": True
        },
        {
            "name": "Оптимизация от Олега AMPR",
            "bootstyle": "success-outline",
            "description": """⭐ ОПТИМИЗАЦИЯ ОТ АВТОРА ⭐

Категория: ✅ БЕЗОПАСНАЯ

Что это:
Профессиональный, но в целом “бережный” набор оптимизаций для улучшения отзывчивости и стабильности системы.

Что делает:
• Настройка Windows и реестра без экстремальных low-level правок
• Отключение очевидно ненужных служб/фона
• Оптимизация памяти и общих системных параметров

Кому подходит:
• Большинству пользователей, кому нужен аккуратный тюнинг без риска




""",
            "is_author": True,
        },

                {
            "name": "Оптимизация от Хауди Хо",
            "bootstyle": "warning-outline",
            "description": """⭐ ЭКСПЕРТНАЯ ОПТИМИЗАЦИЯ ⭐

Категория: ✅ БЕЗОПАСНАЯ

Полноценный набор оптимизаций от эксперта для удаления лишнего и улучшения работы системы.
            
• Отключение телеметрии
• Деактивация ненужных служб
• Устранение бесполезных виджетов в Windows
• Очистка фоновых процессов
• Удаление встроенных UWP-приложений
• Очистка логов системы
• Оптимизация реестра

Рекомендуется для большинства пользователей.





""",
            "is_expert": True,
        },
        {
            "name": "Оптимизация от Igromanoff",
            "bootstyle": "info-outline",
            "description": """⭐ ЭКСПЕРТНАЯ ОПТИМИЗАЦИЯ ⭐

Категория: ⭐ ЛУЧШАЯ (игровая)

Профессиональный набор оптимизаций от эксперта для игровых систем.
            
• Оптимизация для игр
• Отключение ненужных служб
• Настройка производительности GPU
• Оптимизация памяти
• Отключение фоновых процессов
• Настройка приоритетов
• Оптимизация сети для игр

Рекомендуется для геймеров.""",
            "is_expert": True,
        },
        {
            "name": "Оптимизация от MartyFiles",
            "bootstyle": "info-outline",
            "description": """⭐ ЭКСПЕРТНАЯ ОПТИМИЗАЦИЯ ⭐

Категория: ✅ БЕЗОПАСНАЯ

Пакет твиков для ускорения повседневной работы системы. Оптимизирует работу с файлами: ускоряет открытие папок, запуск Windows, настраивает частоту мерцания курсора, управляет файлом гибернации и зарезервированным хранилищем. Не влияет напрямую на FPS в играх, но делает работу в Windows значительно более отзывчивой и комфортной.

Кому подходит:
• Всем, кому нужна “живость” Windows без рискованных отключений
""",
            "is_expert": True,
        },
        {
            "name": "Оптимизация от Марка Аддерли",
            "bootstyle": "info-outline",
            "description": """⭐ ЭКСПЕРТНАЯ ОПТИМИЗАЦИЯ ⭐

Категория: ✅ БЕЗОПАСНАЯ

Глубокий набор оптимизаций от эксперта для максимальной производительности.
            
• Глубокая оптимизация Windows
• Настройка системных параметров
• Оптимизация служб
• Улучшение производительности
• Очистка системы
• Оптимизация памяти

Рекомендуется для опытных пользователей.
""",
            "is_expert": True,
        },
        {
            "name": "Оптимизация от Ancels",
            "bootstyle": "danger-outline",
            "description": """⭐ ЭКСПЕРТНАЯ ОПТИМИЗАЦИЯ ⭐

Категория: ⭐ ЛУЧШАЯ

Комплексный набор оптимизаций от эксперта для улучшения работы системы.
            
• Комплексная оптимизация системы
• Очистка и настройка
• Отключение телеметрии
• Оптимизация автозагрузки
• Настройка производительности
• Оптимизация реестра

Рекомендуется для всех пользователей.
""",
            "is_expert": True,
        },
        {
            "name": "Оптимизация от DE3NAKE",
            "bootstyle": "warning-outline",
            "description": """⭐ ЭКСПЕРТНАЯ ОПТИМИЗАЦИЯ ⭐

Категория: ⚠️ ОПАСНАЯ (low-level)

Набор низкоуровневых системных твиков от опытного твикера, направленных на достижение ультра-низкой задержки. Включает критичные правки: отключение HPET, DEP, Fair Share CPU, IoLatencyCap, настройку таймера (SetTimerResolution), оптимизацию USB, BCDEdit-твики и тонкую настройку приоритетов ядра. Это продвинутый инструмент для энтузиастов, желающих минимизировать каждую микросекунду системной задержки.

Почему “опасная”:
• В пакете есть отключение защитных и загрузочных параметров (DEP/BCD/таймеры), что может повлиять на стабильность и совместимость.




""",
            "is_expert": True,
        },
        {
            "name": "Оптимизация от QQNWR",
            "bootstyle": "danger-outline",
            "description": """⭐ ЭКСПЕРТНАЯ ОПТИМИЗАЦИЯ ⭐

Категория: ⚠️ ОПАСНАЯ (агрессивная)

Что внутри:
• мощный и всеобъемлющий пакет оптимизаций, известный своей агрессивностью: CPU/FPS/InputLag, OpenGL, урезанные драйверы NVIDIA, обширные твики реестра под разный объём ОЗУ, снижение задержки ввода через kHz-патчи и Win32PrioritySeparation, очистка, CMD-твики, CPU/GPU, power plans, RAM, приоритеты CSRSS/lsass/Winlogon, Data Queue Size, kHz-патчи.
• игровой пакет: CPU pack, OpenGL, общие твики, реестр под RAM, очистка/оптимизация Windows, сеть, модуль xz (всё-в-одном).
• экспериментальные/нишевые твики: MarkC MouseFix (поведение ускорения как Win2000/95/98), BIOS/Windows low-level, драйверы/активаторы.

Почему “опасная”:
• Пакет может глубоко менять систему и драйверный слой. Рекомендуется только опытным пользователям с бэкапом.""",
            "is_author": True,
        },
    ]

    # Лучшие твики из популярных твикеров и сборок
    tweaker_configs = [
        {
            "name": "Оптимизация от 123",
            "bootstyle": "warning-outline",
            "description": """⭐ ОПТИМИЗАЦИЯ: 123 ⭐

    Категория: ⚖️ СБАЛАНСИРОВАННАЯ ОПТИМИЗАЦИЯ

    Комплексный набор оптимизаций от пользователя 123. Сбалансированные настройки для улучшения работы Windows.

    Количество твиков: 6 (уникальных: 3)

    Основные улучшения:
    • Очистка системы от временных файлов
    • Общая оптимизация системы
    • Улучшение отзывчивости системы
    • Настройка визуальных эффектов
    • Ускорение работы Windows

    ✅ Рекомендуется для всех пользователей, желающих улучшить работу системы.""",
            "is_user": True,
            "username": "123"
        },
        {
            "name": "Оптимизация от 666",
            "bootstyle": "danger-outline",
            "description": """⭐ ОПТИМИЗАЦИЯ: 666 ⭐

    Категория: ⚠️ НИЗКОУРОВНЕВАЯ ОПТИМИЗАЦИЯ

    Набор низкоуровневых системных твиков от пользователя 666. Включает критические правки системы.

    Количество твиков: 22 (уникальных: 11)

    Основные улучшения:
    • Оптимизация драйверов оборудования
    • Общая оптимизация системы
    • Настройка реестра Windows
    • Улучшение отзывчивости системы
    • Настройка визуальных эффектов

    ⚠️ Требует осторожности. Рекомендуется только опытным пользователям.""",
            "is_user": True,
            "username": "666"
        },
        {
            "name": "Оптимизация от APHEC",
            "bootstyle": "danger-outline",
            "description": """⭐ ОПТИМИЗАЦИЯ: APHEC ⭐

    Категория: ⚠️ АГРЕССИВНАЯ ОПТИМИЗАЦИЯ

    Агрессивный набор оптимизаций от пользователя APHEC. Включает глубокие системные правки для максимальной производительности.

    Количество твиков: 20 (уникальных: 10)

    Основные улучшения:
    • Улучшение производительности в играх
    • Снижение задержки ввода
    • Общая оптимизация системы
    • Улучшение отзывчивости системы
    • Настройка визуальных эффектов

    ⚠️ Требует осторожности. Рекомендуется только опытным пользователям.""",
            "is_user": True,
            "username": "APHEC"
        },
        {
            "name": "Оптимизация от ASUS",
            "bootstyle": "success-outline",
            "description": """⭐ ОПТИМИЗАЦИЯ: ASUS ⭐

    Категория: 🔹 БАЗОВАЯ ОПТИМИЗАЦИЯ

    Минимальный набор оптимизаций от пользователя ASUS. Базовые настройки для улучшения работы системы.

    Количество твиков: 0 (уникальных: 0)

    Основные улучшения:
    • Улучшение отзывчивости системы
    • Настройка визуальных эффектов
    • Ускорение работы Windows
    • Оптимизация системных служб

    ✅ Рекомендуется для всех пользователей, желающих улучшить работу системы.""",
            "is_user": True,
            "username": "ASUS"
        },
        {
            "name": "Оптимизация от Admin",
            "bootstyle": "danger-outline",
            "description": """⭐ ОПТИМИЗАЦИЯ: Admin ⭐

    Категория: ⚠️ НИЗКОУРОВНЕВАЯ ОПТИМИЗАЦИЯ

    Набор низкоуровневых системных твиков от пользователя Admin. Включает критические правки системы.

    Количество твиков: 12 (уникальных: 6)

    Основные улучшения:
    • Оптимизация драйверов оборудования
    • Настройка реестра Windows
    • Общая оптимизация системы
    • Улучшение отзывчивости системы
    • Настройка визуальных эффектов

    ⚠️ Требует осторожности. Рекомендуется только опытным пользователям.""",
            "is_user": True,
            "username": "Admin"
        },
        {
            "name": "Оптимизация от Alex",
            "bootstyle": "success-outline",
            "description": """⭐ ОПТИМИЗАЦИЯ: Alex ⭐

    Категория: 🔹 БАЗОВАЯ ОПТИМИЗАЦИЯ

    Минимальный набор оптимизаций от пользователя Alex. Базовые настройки для улучшения работы системы.

    Количество твиков: 0 (уникальных: 0)

    Основные улучшения:
    • Улучшение отзывчивости системы
    • Настройка визуальных эффектов
    • Ускорение работы Windows
    • Оптимизация системных служб

    ✅ Рекомендуется для всех пользователей, желающих улучшить работу системы.""",
            "is_user": True,
            "username": "Alex"
        },
        {
            "name": "Оптимизация от Chichkanov",
            "bootstyle": "warning-outline",
            "description": """⭐ ОПТИМИЗАЦИЯ: Chichkanov ⭐

    Категория: ⚖️ СБАЛАНСИРОВАННАЯ ОПТИМИЗАЦИЯ

    Комплексный набор оптимизаций от пользователя Chichkanov. Сбалансированные настройки для улучшения работы Windows.

    Количество твиков: 8 (уникальных: 4)

    Основные улучшения:
    • Настройка сетевых параметров
    • Улучшение отзывчивости системы
    • Настройка визуальных эффектов
    • Ускорение работы Windows
    • Оптимизация системных служб

    ✅ Рекомендуется для всех пользователей, желающих улучшить работу системы.""",
            "is_user": True,
            "username": "Chichkanov"
        },
        {
            "name": "Оптимизация от Hentai",
            "bootstyle": "success-outline",
            "description": """⭐ ОПТИМИЗАЦИЯ: Hentai ⭐

    Категория: 🔹 БАЗОВАЯ ОПТИМИЗАЦИЯ

    Минимальный набор оптимизаций от пользователя Hentai. Базовые настройки для улучшения работы системы.

    Количество твиков: 0 (уникальных: 0)

    Основные улучшения:
    • Улучшение отзывчивости системы
    • Настройка визуальных эффектов
    • Ускорение работы Windows
    • Оптимизация системных служб

    ✅ Рекомендуется для всех пользователей, желающих улучшить работу системы.""",
            "is_user": True,
            "username": "Hentai"
        },
        {
            "name": "Оптимизация от PC",
            "bootstyle": "warning-outline",
            "description": """⭐ ОПТИМИЗАЦИЯ: PC ⭐

    Категория: ⚖️ СБАЛАНСИРОВАННАЯ ОПТИМИЗАЦИЯ

    Комплексный набор оптимизаций от пользователя PC. Сбалансированные настройки для улучшения работы Windows.

    Количество твиков: 13 (уникальных: 8)

    Основные улучшения:
    • Оптимизация графических настроек
    • Настройка сетевых параметров
    • Общая оптимизация системы
    • Улучшение отзывчивости системы
    • Настройка визуальных эффектов

    ✅ Рекомендуется для всех пользователей, желающих улучшить работу системы.""",
            "is_user": True,
            "username": "PC"
        },
        {
            "name": "Оптимизация от Santo",
            "bootstyle": "success-outline",
            "description": """⭐ ОПТИМИЗАЦИЯ: Santo ⭐

    Категория: 🔹 БАЗОВАЯ ОПТИМИЗАЦИЯ

    Минимальный набор оптимизаций от пользователя Santo. Базовые настройки для улучшения работы системы.

    Количество твиков: 1 (уникальных: 1)

    Основные улучшения:
    • Оптимизация использования памяти
    • Очистка системы от временных файлов
    • Улучшение отзывчивости системы
    • Настройка визуальных эффектов
    • Ускорение работы Windows

    ✅ Рекомендуется для всех пользователей, желающих улучшить работу системы.""",
            "is_user": True,
            "username": "Santo"
        },
        {
            "name": "Оптимизация от StizaR",
            "bootstyle": "success-outline",
            "description": """⭐ ОПТИМИЗАЦИЯ: StizaR ⭐

    Категория: 🔹 БАЗОВАЯ ОПТИМИЗАЦИЯ

    Минимальный набор оптимизаций от пользователя StizaR. Базовые настройки для улучшения работы системы.

    Количество твиков: 0 (уникальных: 0)

    Основные улучшения:
    • Улучшение отзывчивости системы
    • Настройка визуальных эффектов
    • Ускорение работы Windows
    • Оптимизация системных служб

    ✅ Рекомендуется для всех пользователей, желающих улучшить работу системы.""",
            "is_user": True,
            "username": "StizaR"
        },
        {
            "name": "Оптимизация от StizaR81",
            "bootstyle": "success-outline",
            "description": """⭐ ОПТИМИЗАЦИЯ: StizaR81 ⭐

    Категория: 🔹 БАЗОВАЯ ОПТИМИЗАЦИЯ

    Минимальный набор оптимизаций от пользователя StizaR81. Базовые настройки для улучшения работы системы.

    Количество твиков: 0 (уникальных: 0)

    Основные улучшения:
    • Улучшение отзывчивости системы
    • Настройка визуальных эффектов
    • Ускорение работы Windows
    • Оптимизация системных служб

    ✅ Рекомендуется для всех пользователей, желающих улучшить работу системы.""",
            "is_user": True,
            "username": "StizaR81"
        },
        {
            "name": "Оптимизация от Vlad",
            "bootstyle": "success-outline",
            "description": """⭐ ОПТИМИЗАЦИЯ: Vlad ⭐

    Категория: 🔹 БАЗОВАЯ ОПТИМИЗАЦИЯ

    Минимальный набор оптимизаций от пользователя Vlad. Базовые настройки для улучшения работы системы.

    Количество твиков: 4 (уникальных: 2)

    Основные улучшения:
    • Оптимизация схем электропитания
    • Улучшение отзывчивости системы
    • Настройка визуальных эффектов
    • Ускорение работы Windows
    • Оптимизация системных служб

    ✅ Рекомендуется для всех пользователей, желающих улучшить работу системы.""",
            "is_user": True,
            "username": "Vlad"
        },
        {
            "name": "Оптимизация от X-Files",
            "bootstyle": "success-outline",
            "description": """⭐ ОПТИМИЗАЦИЯ: X-Files ⭐

    Категория: 🔹 БАЗОВАЯ ОПТИМИЗАЦИЯ

    Минимальный набор оптимизаций от пользователя X-Files. Базовые настройки для улучшения работы системы.

    Количество твиков: 0 (уникальных: 0)

    Основные улучшения:
    • Улучшение отзывчивости системы
    • Настройка визуальных эффектов
    • Ускорение работы Windows
    • Оптимизация системных служб

    ✅ Рекомендуется для всех пользователей, желающих улучшить работу системы.""",
            "is_user": True,
            "username": "X-Files"
        },
        {
            "name": "Оптимизация от Xpanitel",
            "bootstyle": "success-outline",
            "description": """⭐ ОПТИМИЗАЦИЯ: Xpanitel ⭐

    Категория: 🔹 БАЗОВАЯ ОПТИМИЗАЦИЯ

    Минимальный набор оптимизаций от пользователя Xpanitel. Базовые настройки для улучшения работы системы.

    Количество твиков: 2 (уникальных: 1)

    Основные улучшения:
    • Оптимизация графических настроек
    • Улучшение отзывчивости системы
    • Настройка визуальных эффектов
    • Ускорение работы Windows
    • Оптимизация системных служб

    ✅ Рекомендуется для всех пользователей, желающих улучшить работу системы.""",
            "is_user": True,
            "username": "Xpanitel"
        },
        {
            "name": "Оптимизация от YourCat",
            "bootstyle": "success-outline",
            "description": """⭐ ОПТИМИЗАЦИЯ: YourCat ⭐

    Категория: 🔹 БАЗОВАЯ ОПТИМИЗАЦИЯ

    Минимальный набор оптимизаций от пользователя YourCat. Базовые настройки для улучшения работы системы.

    Количество твиков: 0 (уникальных: 0)

    Основные улучшения:
    • Улучшение отзывчивости системы
    • Настройка визуальных эффектов
    • Ускорение работы Windows
    • Оптимизация системных служб

    ✅ Рекомендуется для всех пользователей, желающих улучшить работу системы.""",
            "is_user": True,
            "username": "YourCat"
        },
        {
            "name": "Оптимизация от afoni",
            "bootstyle": "success-outline",
            "description": """⭐ ОПТИМИЗАЦИЯ: afoni ⭐

    Категория: 🔹 БАЗОВАЯ ОПТИМИЗАЦИЯ

    Минимальный набор оптимизаций от пользователя afoni. Базовые настройки для улучшения работы системы.

    Количество твиков: 2 (уникальных: 1)

    Основные улучшения:
    • Улучшение отзывчивости системы
    • Настройка визуальных эффектов
    • Ускорение работы Windows
    • Оптимизация системных служб

    ✅ Рекомендуется для всех пользователей, желающих улучшить работу системы.""",
            "is_user": True,
            "username": "afoni"
        },
        {
            "name": "Оптимизация от hsed",
            "bootstyle": "success-outline",
            "description": """⭐ ОПТИМИЗАЦИЯ: hsed ⭐

    Категория: 🔹 БАЗОВАЯ ОПТИМИЗАЦИЯ

    Минимальный набор оптимизаций от пользователя hsed. Базовые настройки для улучшения работы системы.

    Количество твиков: 0 (уникальных: 0)

    Основные улучшения:
    • Улучшение отзывчивости системы
    • Настройка визуальных эффектов
    • Ускорение работы Windows
    • Оптимизация системных служб

    ✅ Рекомендуется для всех пользователей, желающих улучшить работу системы.""",
            "is_user": True,
            "username": "hsed"
        },
        {
            "name": "Оптимизация от isoro",
            "bootstyle": "success-outline",
            "description": """⭐ ОПТИМИЗАЦИЯ: isoro ⭐

    Категория: 🔹 БАЗОВАЯ ОПТИМИЗАЦИЯ

    Минимальный набор оптимизаций от пользователя isoro. Базовые настройки для улучшения работы системы.

    Количество твиков: 2 (уникальных: 1)

    Основные улучшения:
    • Общая оптимизация системы
    • Улучшение отзывчивости системы
    • Настройка визуальных эффектов
    • Ускорение работы Windows
    • Оптимизация системных служб

    ✅ Рекомендуется для всех пользователей, желающих улучшить работу системы.""",
            "is_user": True,
            "username": "isoro"
        },
        {
            "name": "Оптимизация от kalit",
            "bootstyle": "success-outline",
            "description": """⭐ ОПТИМИЗАЦИЯ: kalit ⭐

    Категория: 🔹 БАЗОВАЯ ОПТИМИЗАЦИЯ

    Минимальный набор оптимизаций от пользователя kalit. Базовые настройки для улучшения работы системы.

    Количество твиков: 0 (уникальных: 0)

    Основные улучшения:
    • Улучшение отзывчивости системы
    • Настройка визуальных эффектов
    • Ускорение работы Windows
    • Оптимизация системных служб

    ✅ Рекомендуется для всех пользователей, желающих улучшить работу системы.""",
            "is_user": True,
            "username": "kalit"
        },
        {
            "name": "Оптимизация от lyash",
            "bootstyle": "success-outline",
            "description": """⭐ ОПТИМИЗАЦИЯ: lyash ⭐

    Категория: 🔹 БАЗОВАЯ ОПТИМИЗАЦИЯ

    Минимальный набор оптимизаций от пользователя lyash. Базовые настройки для улучшения работы системы.

    Количество твиков: 0 (уникальных: 0)

    Основные улучшения:
    • Улучшение отзывчивости системы
    • Настройка визуальных эффектов
    • Ускорение работы Windows
    • Оптимизация системных служб

    ✅ Рекомендуется для всех пользователей, желающих улучшить работу системы.""",
            "is_user": True,
            "username": "lyash"
        },
        {
            "name": "Оптимизация от maxi",
            "bootstyle": "success-outline",
            "description": """⭐ ОПТИМИЗАЦИЯ: maxi ⭐

    Категория: 🔹 БАЗОВАЯ ОПТИМИЗАЦИЯ

    Минимальный набор оптимизаций от пользователя maxi. Базовые настройки для улучшения работы системы.

    Количество твиков: 4 (уникальных: 2)

    Основные улучшения:
    • Отключение телеметрии и слежения
    • Оптимизация схем электропитания
    • Улучшение отзывчивости системы
    • Настройка визуальных эффектов
    • Ускорение работы Windows

    ✅ Рекомендуется для всех пользователей, желающих улучшить работу системы.""",
            "is_user": True,
            "username": "maxi"
        },
        {
            "name": "Оптимизация от sergey",
            "bootstyle": "warning-outline",
            "description": """⭐ ОПТИМИЗАЦИЯ: sergey ⭐

    Категория: ⚖️ СБАЛАНСИРОВАННАЯ ОПТИМИЗАЦИЯ

    Комплексный набор оптимизаций от пользователя sergey. Сбалансированные настройки для улучшения работы Windows.

    Количество твиков: 6 (уникальных: 3)

    Основные улучшения:
    • Улучшение отзывчивости системы
    • Настройка визуальных эффектов
    • Ускорение работы Windows
    • Оптимизация системных служб

    ✅ Рекомендуется для всех пользователей, желающих улучшить работу системы.""",
            "is_user": True,
            "username": "sergey"
        },
        {
            "name": "Оптимизация от silver gloria",
            "bootstyle": "warning-outline",
            "description": """⭐ ОПТИМИЗАЦИЯ: silver gloria ⭐

    Категория: ⚖️ СБАЛАНСИРОВАННАЯ ОПТИМИЗАЦИЯ

    Комплексный набор оптимизаций от пользователя silver gloria. Сбалансированные настройки для улучшения работы Windows.

    Количество твиков: 10 (уникальных: 10)

    Основные улучшения:
    • Оптимизация графических настроек
    • Настройка реестра Windows
    • Улучшение отзывчивости системы
    • Настройка визуальных эффектов
    • Ускорение работы Windows

    ✅ Рекомендуется для всех пользователей, желающих улучшить работу системы.""",
            "is_user": True,
            "username": "silver gloria"
        },
        {
            "name": "Оптимизация от sirenfy",
            "bootstyle": "success-outline",
            "description": """⭐ ОПТИМИЗАЦИЯ: sirenfy ⭐

    Категория: 🔹 БАЗОВАЯ ОПТИМИЗАЦИЯ

    Минимальный набор оптимизаций от пользователя sirenfy. Базовые настройки для улучшения работы системы.

    Количество твиков: 0 (уникальных: 0)

    Основные улучшения:
    • Улучшение отзывчивости системы
    • Настройка визуальных эффектов
    • Ускорение работы Windows
    • Оптимизация системных служб

    ✅ Рекомендуется для всех пользователей, желающих улучшить работу системы.""",
            "is_user": True,
            "username": "sirenfy"
        },
        {
            "name": "Оптимизация от wretz",
            "bootstyle": "success-outline",
            "description": """⭐ ОПТИМИЗАЦИЯ: wretz ⭐

    Категория: 🔹 БАЗОВАЯ ОПТИМИЗАЦИЯ

    Минимальный набор оптимизаций от пользователя wretz. Базовые настройки для улучшения работы системы.

    Количество твиков: 0 (уникальных: 0)

    Основные улучшения:
    • Улучшение отзывчивости системы
    • Настройка визуальных эффектов
    • Ускорение работы Windows
    • Оптимизация системных служб

    ✅ Рекомендуется для всех пользователей, желающих улучшить работу системы.""",
            "is_user": True,
            "username": "wretz"
        },
        {
            "name": "Оптимизация от Администратора",
            "bootstyle": "danger-outline",
            "description": """⭐ ОПТИМИЗАЦИЯ: Администратор ⭐

    Категория: ⚠️ АГРЕССИВНАЯ ОПТИМИЗАЦИЯ

    Агрессивный набор оптимизаций от пользователя Администратор. Включает глубокие системные правки для максимальной производительности.

    Количество твиков: 16 (уникальных: 8)

    Основные улучшения:
    • Оптимизация драйверов оборудования
    • Оптимизация графических настроек
    • Оптимизация использования памяти
    • Улучшение отзывчивости системы
    • Настройка визуальных эффектов

    ⚠️ Требует осторожности. Рекомендуется только опытным пользователям.""",
            "is_user": True,
            "username": "Администратор"
        },
        {
            "name": "Оптимизация от Чебоксарского",
            "bootstyle": "warning-outline",
            "description": """⭐ ОПТИМИЗАЦИЯ: Чебоксарский ⭐

    Категория: ⚖️ СБАЛАНСИРОВАННАЯ ОПТИМИЗАЦИЯ

    Комплексный набор оптимизаций от Чебоксарского пользователя. Сбалансированные настройки для улучшения работы Windows.

    Количество твиков: 8 (уникальных: 4)

    Основные улучшения:
    • Настройка сетевых параметров
    • Улучшение отзывчивости системы
    • Настройка визуальных эффектов
    • Ускорение работы Windows
    • Оптимизация системных служб

    ✅ Рекомендуется для всех пользователей, желающих улучшить работу системы.""",
            "is_user": True,
            "username": "Чебоксарский"
        }
    ]

    # Создаем скроллируемый контейнер
    canvas = tk.Canvas(config_frame)
    scrollbar = ttk.Scrollbar(config_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    # Важно: сохраняем id "окна" внутри Canvas, чтобы корректно управлять размерами
    scroll_window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    def _update_main_scrollregion():
        """Обновляет scrollregion строго по размеру контента (убирает 'пустое поле')."""
        try:
            canvas.update_idletasks()
            scrollable_frame.update_idletasks()
        except Exception:
            pass

        # Реальная требуемая высота контента
        try:
            content_h = scrollable_frame.winfo_reqheight()
        except Exception:
            content_h = 1

        # Ширина canvas (чтобы embedded frame растягивался по ширине)
        try:
            cw = canvas.winfo_width()
        except Exception:
            cw = 1

        # Пока canvas ещё не размечен, winfo_width() может быть 1 — не затираем ширину окна до 1px.
        if cw <= 1:
            return
        if content_h < 1:
            content_h = 1

        try:
            canvas.itemconfig(scroll_window_id, width=cw)
        except Exception:
            pass

        # scrollregion: строго по контенту (без искусственного "запаса")
        canvas.configure(scrollregion=(0, 0, cw, content_h))

    # Обновляем scrollregion при изменении контента
    scrollable_frame.bind("<Configure>", lambda e: _update_main_scrollregion(), add="+")
    
    # Обработка скролла мыши (самый надежный вариант для ttk/ttkbootstrap на Windows):
    # глобально слушаем колесо и скроллим ТОЛЬКО когда курсор находится внутри scrollable_frame.
    def _is_descendant(widget, ancestor):
        """True если widget находится внутри ancestor по цепочке master."""
        try:
            w = widget
            while w is not None:
                if w == ancestor:
                    return True
                w = getattr(w, "master", None)
        except Exception:
            return False
        return False

    def _on_global_mousewheel(event):
        # Где сейчас курсор
        try:
            w = root.winfo_containing(event.x_root, event.y_root)
        except Exception:
            w = None

        # Скроллим только если курсор внутри прокручиваемой области "Быстрая оптимизация"
        if w is None or not _is_descendant(w, scrollable_frame):
            return

        delta = getattr(event, "delta", 0) or 0
        if not delta:
            return
        canvas.yview_scroll(int(-1 * (delta / 120)), "units")

    # Важно: по проекту есть места, которые делают unbind_all("<MouseWheel>") или перезаписывают bind_all,
    # поэтому делаем "самовосстановление" — при наведении на область снова привязываем.
    def _ensure_main_mousewheel_bound(event=None):
        try:
            root.bind_all("<MouseWheel>", _on_global_mousewheel, add="+")
        except Exception:
            pass

    _ensure_main_mousewheel_bound()
    canvas.bind("<Enter>", _ensure_main_mousewheel_bound, add="+")
    scrollable_frame.bind("<Enter>", _ensure_main_mousewheel_bound, add="+")
    
    # Обновление ширины embedded frame и scrollregion при изменении размера canvas
    canvas.bind("<Configure>", lambda e: _update_main_scrollregion(), add="+")

    # Стартовый пересчет делаем после pack(), иначе canvas.winfo_width() часто == 1 и контент "исчезает"
    root.after(0, _update_main_scrollregion)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # # Верхний фрейм с описанием и конфигом от socde18а (внутри скроллируемого контейнера)
    # top_info_frame = ttk.Frame(scrollable_frame)
    # top_info_frame.pack(fill="x", pady=(0, 20), padx=10)
    
    # # Настраиваем grid для равномерного распределения
    # top_info_frame.grid_columnconfigure(0, weight=3, minsize=500)
    # top_info_frame.grid_columnconfigure(1, weight=2, minsize=350)
    
#     # Левая часть - описание твикера
#     description_frame = ttk.Labelframe(top_info_frame, text="О твикере Extreme", padding=15)
#     description_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
    
#     description_text = ttk.Label(
#         description_frame,
#         text="""Extreme - это база, которая позволяет внести в систему огромное количество глобальных твиков. Не просто "ускорить ПК", а точечно настроить под себя.

# ✅ Открытый исходный код - вы всегда можете посмотреть КОНКРЕТНО какие изменения вносятся в реестр и систему. Никаких скрытых действий!

# ✅ Признание экспертов - некоторые наши твики используют такие известные личности как Igromanoff и DE3NAKE. Они проверяли, тестировали и используют наши твики.

# ✅ Универсальность - собраны лучшие твики из Hone, BoosterX и других проектов. Один инструмент вместо десятка.

# ✅ Для слабых ПК - реально помогает дать вторую жизнь старому железу за счет удаления всего лишнего.

# Можно отключить телеметрию, ненужные службы, виджеты Windows 11, убрать скрытые фоновые процессы, удалить мусорные UWP-приложения, очистить логи и восстановить Windows Store.

# ⚠️ ВАЖНО: Это не "волшебная кнопка". Требует понимания что вы отключаете. Начинайте с базовых пресетов!
# """,
#         wraplength=480,
#         justify="left",
#         font=("Segoe UI", 10)
#     )
#     description_text.pack(anchor="w", fill="x")

    # # Документация по конфигам (короткая “карта” что выбирать)
    # configs_docs_frame = ttk.Labelframe(scrollable_frame, text="📚 Документация по конфигам", padding=15)
    # configs_docs_frame.pack(fill="x", pady=(0, 20), padx=10)

#     configs_docs_text = ttk.Label(
#         configs_docs_frame,
#         text="""Конфиги — это готовые пакеты твиков (обычно .bat/набор действий), которые применяют сразу группу настроек Windows.

# Как выбирать:
# • Если ты не уверен — начинай с ✅ безопасных и делай изменения поэтапно.
# • ⚠️ Опасные конфиги меняют low-level параметры (BCD/таймеры/защиты/драйверные штуки) — их применяют только опытные пользователи.
# • ⭐ Лучшие — это те, что чаще всего дают хороший баланс/результат по отзывам и практике.

# ✅ Безопасные (рекомендуем большинству):
# • Марк Аддерли — глубокая, но в целом “бережная” оптимизация без экстремальных low-level правок.
# • MartyFiles — ускоряет повседневную работу Windows (проводник/запуск/визуальные мелочи), не про FPS напрямую.
# • socde18 — сбалансированный набор, хороший старт и часто лучший выбор “по умолчанию”.
# • Олег AMPR — аккуратная оптимизация системы/реестра/служб без жёсткого “вырезания”.
# • Хауди Хо — чистка и отключение лишнего (телеметрия/виджеты/UWP) в разумных пределах.

# ⚠️ Опасные (только с бэкапом/пониманием):
# • De3nake — low-level твики ради минимальной задержки: HPET/DEP/таймеры/BCD/USB/приоритеты ядра.
# • Антон — “heavy” пакеты (kenma/qqnwr/эксперименты): агрессивные твики реестра, kHz-патчи, возможные вмешательства в драйверный слой.

# ⭐ Лучшие (если хочешь “топ” варианты):
# • Ancels — комплексный экспертный пакет, часто даёт заметный эффект, но может быть агрессивнее “безопасных”.
# • Igromanoff (Игроманов) — сильный игровой набор: упор на отклик/фон/приоритеты/сеть под игры.
# • socde18 — лучший стартовый баланс и простой выбор без лишних рисков.

# Важно:
# • Перед применением любых конфигов желательно создать точку восстановления или бэкап.
# • Если что-то пошло не так — используй вкладку “Исправления” для отката/фиксов.""",
#         wraplength=1200,
#         justify="left",
#         font=("Segoe UI", 10),
#         foreground="#32FBE2"
#     )
#     configs_docs_text.pack(anchor="w", fill="x")
    
    # # Правая часть - конфиг от socde18а и кнопки
    # right_action_frame = ttk.Labelframe(top_info_frame, text="⭐ Рекомендуется", padding=15)
    # right_action_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
    
    # # Конфиг от socde18а
    # skidonchik_config = author_configs[0]  # Первый конфиг - от socde18а
    
    # # Заголовок конфига
    # skidonchik_title = ttk.Label(
    #     right_action_frame,
    #     text="Оптимизация от socde18а",
    #     font=("Segoe UI", 10, "bold")
    # )
    # skidonchik_title.pack(pady=(0, 8))
    
    # skidonchik_button = ttk.Button(
    #     right_action_frame,
    #     text="🚀 Запустить",
    #     bootstyle=skidonchik_config["bootstyle"],
    #     width=25,
    #     command=lambda: show_novice_warning(skidonchik_config["name"]) if novice_mode else run_config(skidonchik_config["name"])
    # )
    # skidonchik_button.pack(pady=(0, 10))

    # def show_novice_warning(config_name):
    #     """Показать предупреждение для новичков"""
    #     result = messagebox.askyesno(
    #         "⚠️ Внимание! Режим новичка",
    #         f"Конфигурация '{config_name}' может сломать систему!\n\n"
    #         "Этот конфиг содержит агрессивные оптимизации, которые могут:\n"
    #         "• Нарушить работу Windows\n"
    #         "• Привести к нестабильности системы\n"
    #         "• Вызвать проблемы с драйверами\n\n"
    #         "Рекомендуется:\n"
    #         "• Создать точку восстановления\n"
    #         "• Сделать бэкап важных данных\n"
    #         "• Использовать только если понимаете последствия\n\n"
    #         "Вы уверены, что хотите продолжить?",
    #         icon='warning'
    #     )
    #     if result:
    #         run_config(config_name)
    
    # # Краткое описание конфига
    # skidonchik_desc = ttk.Label(
    #     right_action_frame,
    #     text="Профессиональный набор оптимизаций от автора для улучшения работы системы.",
    #     wraplength=340,
    #     justify="left",
    #     font=("Segoe UI", 8),
    #     foreground="gray"
    # )
    # skidonchik_desc.pack(pady=(0, 15))
    
    # # Разделитель
    # separator = ttk.Separator(right_action_frame, orient="horizontal")
    # separator.pack(fill="x", pady=(0, 15))
    
    # # Кнопки для перехода
    # nav_label = ttk.Label(
    #     right_action_frame,
    #     text="Быстрая навигация:",
    #     font=("Segoe UI", 9, "bold")
    # )
    # nav_label.pack(pady=(0, 8))
    
    # optimization_btn = ttk.Button(
    #     right_action_frame,
    #     text="⚙️ Оптимизация",
    #     bootstyle="danger-outline",
    #     width=25,
    #     command=switch_to_optimization
    # )
    # optimization_btn.pack(pady=(0, 8))
    
    # settings_btn = ttk.Button(
    #     right_action_frame,
    #     text="🔧 Настройки",
    #     bootstyle="info-outline",
    #     width=25,
    #     command=switch_to_settings
    # )
    # settings_btn.pack(pady=(0, 8))

    # donat_btn = ttk.Button(
    #     right_action_frame,
    #     text="☕ Поддержать",
    #     bootstyle="warning-outline",
    #     width=25,
    #     command=open_donat
    # )
    # donat_btn.pack(pady=(0, 5))

    # Загружаем пользовательские конфиги из папки user_data\Configs
    user_configs = []
    user_configs_dir = "user_data/Configs"
    if os.path.exists(user_configs_dir):
        for filename in os.listdir(user_configs_dir):
            if filename.endswith('.bat'):
                config_name = filename[:-4]  # Убираем расширение .bat
                user_configs.append({
                    "name": config_name,
                    "bootstyle": "primary-outline",
                    "description": f"Пользовательский конфиг: {config_name}",
                    "is_user": True,
                    "filepath": os.path.join(user_configs_dir, filename)
                })

    # Секция пользовательских конфигов (после right_action_frame, до author_configs)
    if user_configs:
        user_label = ttk.Label(
            scrollable_frame,
            text="📁 ПОЛЬЗОВАТЕЛЬСКИЕ КОНФИГИ 📁",
            font=("Segoe UI", 16, "bold")
        )
        user_label.pack(anchor="w", pady=(20, 10), padx=10)
        
        user_frame = ttk.Labelframe(
            scrollable_frame,
            text="Ваши пользовательские конфиги",
            padding=15
        )
        user_frame.pack(fill="x", padx=10, pady=5)
        
        # Создаем кнопки конфигов с отображением содержания
        buttons_frame = ttk.Frame(user_frame)
        buttons_frame.pack(fill="x", pady=10)
        
        for i, cfg in enumerate(user_configs):
            row = i // 3
            col = i % 3
            
            button_frame = ttk.Labelframe(
                buttons_frame, 
                text=f"⭐ {cfg['name']} ⭐",
                padding=10
            )
            button_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            btn_style = cfg["bootstyle"]
            config_path = cfg["filepath"]
            btn = ttk.Button(
                button_frame,
                text=cfg["name"],
                width=28,
                bootstyle=btn_style,
                command=lambda path=config_path: subprocess.call([path], shell=True)
            )
            btn.pack(pady=(10, 5), padx=10)

            # Читаем содержимое конфига
            config_content = ""
            try:
                if os.path.exists(config_path):
                    with open(config_path, "r", encoding="utf-8", errors="ignore") as f:
                        content_lines = f.readlines()[:50]  # Берем первые 50 строк
                        config_content = "".join(content_lines)
                        if len(content_lines) == 50:
                            config_content += "\n... (показаны первые 50 строк)"
            except Exception:
                config_content = "Не удалось прочитать содержимое файла"
            
            # Создаем фрейм с прокруткой для содержимого
            content_scroll_frame = ttk.Frame(button_frame)
            content_scroll_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
            
            # Canvas для прокрутки
            canvas = tk.Canvas(content_scroll_frame, height=150)
            scrollbar = ttk.Scrollbar(content_scroll_frame, orient="vertical", command=canvas.yview)
            scrollable_content = ttk.Frame(canvas)
            
            scrollable_content.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_content, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Текст с содержимым
            content_text = tk.Text(
                scrollable_content,
                wrap=tk.WORD,
                width=30,
                height=8,
                font=("Consolas", 8),
                bg="#1e1e1e",
                fg="#d4d4d4",
                insertbackground="#d4d4d4",
                relief=tk.FLAT,
                padx=5,
                pady=5
            )
            content_text.insert("1.0", config_content)
            content_text.config(state=tk.DISABLED)
            content_text.pack(fill="both", expand=True)
            
            # Привязываем прокрутку колесиком мыши
            def on_mousewheel(event):
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            canvas.bind_all("<MouseWheel>", on_mousewheel)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
        
        # Настраиваем веса колонок
        for i in range(3):
            buttons_frame.grid_columnconfigure(i, weight=1)
        
        # Настраиваем веса строк
        for i in range((len(user_configs) + 2) // 3):
            buttons_frame.grid_rowconfigure(i, weight=1)

    # В режиме новичка показываем только разрешенные конфиги
    if novice_mode:
        # Фильтруем стандартные конфиги - оставляем только "Базовая оптимизация"
        filtered_standard_configs = [c for c in standard_configs if c["name"] == "Базовая оптимизация"]
        
        # Добавляем "Максимальная оптимизация" как отдельный конфиг
        safe_optimization_config = {
            "name": "Максимальная оптимизация",
            "bootstyle": "danger-outline",
            "description": """Максимальный набор безопасных оптимизаций для начинающих пользователей.
            
• Безопасная оптимизация служб
• Очистка временных файлов
• Оптимизация DirectX
• Отключение телеметрии
• Базовая настройка системы

Рекомендуется для новичков.""",
        }
        filtered_standard_configs.append(safe_optimization_config)
        
        # Фильтруем экспертные конфиги - оставляем только "Хауди Хо", "Марк Аддерли" и "MartyFiles"
        filtered_expert_configs = [
            c for c in author_configs 
            if "Хауди Хо" in c["name"] or "Марка Аддерли" in c["name"] or "MartyFiles" in c["name"]
        ]
        
        # Показываем только базовую оптимизацию
        standard_label = ttk.Label(
            scrollable_frame,
            text="⚡ Безопасные оптимизации ⚡",
            font=("Segoe UI", 14, "bold")
        )
        standard_label.pack(anchor="w", pady=(20, 5), padx=10)
        create_config_buttons(filtered_standard_configs, scrollable_frame, columns=3)
        
        # # Показываем сборки Windows
        # os_build_label = ttk.Label(
        #     scrollable_frame,
        #     text="💻 Превращение Windows в сборки 💻",
        #     font=("Segoe UI", 16, "bold")
        # )
        # os_build_label.pack(anchor="w", pady=(20, 10), padx=10)
        # os_build_frame = ttk.Labelframe(
        #     scrollable_frame,
        #     text="Настройки для превращения Windows в ReviOS, AtlasOS, Flibustier, MakuOS",
        #     padding=15
        # )
        # os_build_frame.pack(fill="x", padx=10, pady=5)
        # create_config_buttons(os_build_configs, os_build_frame, columns=2, is_os_build=True)
    else:
        # Секция оптимизаций от авторов (вверху)
        author_label = ttk.Label(
            scrollable_frame,
            # text="⭐ ОПТИМИЗАЦИИ ОТ АВТОРОВ ⭐",
            text="ОПТИМИЗАЦИИ ОТ ЭКСПЕРТОВ В WINDOWS ⭐",
            # text="ОПТИМИЗАЦИИ ОТ ЭКСПЕРТОВ В WINDOWS ⭐", 
            font=("Segoe UI", 16, "bold")
        )
        author_label.pack(anchor="w", pady=(10, 10), padx=10)
        
        author_frame = ttk.Labelframe(
            scrollable_frame,
            text="Доступно только в Pro версии",
            padding=15
        )
        author_frame.pack(fill="x", padx=10, pady=5)
        
        create_config_buttons(author_configs, author_frame, columns=4, is_author=True)

        # Секция лучших твиков из популярных твикеров
        tweaker_label = ttk.Label(
            scrollable_frame,
            text="🚀 ПОЛЬЗОВАТЕЛЬСКИЕ КОНФИГИ ОТ СООБЩЕСТВА EXTREME TWEAKER И ALL TWEAKER 🚀",
            font=("Segoe UI", 16, "bold")
        )
        tweaker_label.pack(anchor="w", pady=(20, 10), padx=10)
        
        tweaker_frame = ttk.Labelframe(
            scrollable_frame,
            text="Доступно только в Pro версии",
            padding=15
        )
        tweaker_frame.pack(fill="x", padx=10, pady=5)
        
        create_config_buttons(tweaker_configs, tweaker_frame, columns=4, is_tweaker=True)

    # Создаем основной контейнер для главной вкладки (с динамической загрузкой)
    main_tab = ttk.Frame(tab_control)

    # Добавляем остальные вкладки из tabs_main (если нужно)
    developer_mode = config.getboolean("General", "developer_mode", fallback=False)
    dangerous_main_tabs = ["Анонимность", "Приватность"]
  

    # Проходим по всем элементам словаря tabs_main
    novice_mode = config.getboolean("General", "novice_mode", fallback=False)
    tabs_to_use_main = tabs_main_novice if novice_mode else tabs_main
    
    frames_mode = config.getboolean("General", "frames_instead_of_tabs", fallback=False)

    if frames_mode:
        combined = {}
        for tab_name, checkbox_names in tabs_to_use_main.items():
            if tab_name != "Главная":
                if not novice_mode and not developer_mode and tab_name in dangerous_main_tabs:
                    continue
                combined[tab_name] = checkbox_names
        if combined:
            try:
                cons_frame = create_consolidated_optimization_tab(tab_control, combined, config, "Главная")
                tab_control.add(cons_frame, text="Все твики")
            except Exception as e:
                print(f"Ошибка создания консолидированной вкладки: {e}")
                import traceback; traceback.print_exc()
    else:
        for tab_name, checkbox_names in tabs_to_use_main.items():
            if tab_name != "Главная":
                if not novice_mode and not developer_mode and tab_name in dangerous_main_tabs:
                    continue
                tab = ttk.Frame(tab_control)
                tab_control.add(tab, text=tab_name)
                placeholder = ttk.Label(
                    tab,
                    text="Загрузка содержимого...",
                    font=("Segoe UI", 12),
                    foreground="#32FBE2",
                )
                placeholder.pack(expand=True)
                tab.tab_info = {
                    "name": tab_name,
                    "checkbox_names": checkbox_names,
                    "loaded": False,
                }

    # Проверяем, есть ли вкладки в tab_control
    if tab_control.tabs():
        tab_control.select(0)


"""
+------------------------------------+
| Функция для переключения на        |
| вкладки с драйверами               |
+------------------------------------+
"""


def switch_to_drivers():
    # Проверяем режим разработчика
    developer_mode = config.getboolean("General", "developer_mode", fallback=False)
    if not developer_mode:
        messagebox.showwarning(
            "Режим разработчика отключен",
            "Вкладка 'Драйвера' доступна только в режиме разработчика.\n\nВключите режим разработчика в Настройки → Дополнительно → Режим разработчика"
        )
        return

    # Удаляем все существующие вкладки
    for tab in tab_control.tabs():
        tab_control.forget(tab)

    frames_mode = config.getboolean("General", "frames_instead_of_tabs", fallback=False)
    if frames_mode:
        if tabs_1:
            try:
                cons_frame = create_consolidated_optimization_tab(tab_control, tabs_1, config, "Драйверы")
                tab_control.add(cons_frame, text="Драйверы")
            except Exception as e:
                print(f"Ошибка создания вкладки драйверов: {e}")
                import traceback; traceback.print_exc()
    else:
        for tab_name, checkbox_names in tabs_1.items():
            tab_frame = ttk.Frame(tab_control)
            tab_control.add(tab_frame, text=tab_name)

            placeholder = ttk.Label(
                tab_frame,
                text="Загрузка содержимого...",
                font=("Segoe UI", 12),
                foreground="#666666",
            )
            placeholder.pack(expand=True)

            tab_frame.tab_info = {
                "name": tab_name,
                "checkbox_names": checkbox_names,
                "loaded": False,
            }

    # Выбираем первую вкладку
    if tab_control.tabs():
        tab_control.select(0)


"""
+------------------------------------+
| Функция для переключения на        |
| вкладку оптимизации                |
+------------------------------------+
"""

from optimization_tab import create_optimization_tab
# from services_manager import create_services_tab

def switch_to_optimization():
    # Удаляем все существующие вкладки
    for tab in tab_control.tabs():
        tab_control.forget(tab)

    developer_mode = config.getboolean("General", "developer_mode", fallback=False)
    novice_mode = config.getboolean("General", "novice_mode", fallback=False)
    frames_mode = config.getboolean("General", "frames_instead_of_tabs", fallback=False)
    dangerous_tabs = ["Максимальная оптимизация", "Хардкор оптимизация", "Остальное"]

    tabs_to_use = tabs_novice if novice_mode else tabs
    filtered_tabs = {}
    for tab_name, checkbox_names in tabs_to_use.items():
        if not novice_mode and not developer_mode and tab_name in dangerous_tabs:
            continue
        if tab_name == "Службы":
            continue
        filtered_tabs[tab_name] = checkbox_names

    if frames_mode:
        # Вкладка оптимизации (vendor)
        try:
            optimization_frame = create_optimization_tab(tab_control, config)
            tab_control.add(optimization_frame, text="Оптимизация")
        except Exception as e:
            print(f"Ошибка при создании вкладки оптимизации: {e}")
            import traceback; traceback.print_exc()

        # Все оптимизации как фреймы в одной вкладке
        if filtered_tabs:
            try:
                consolidated_frame = create_consolidated_optimization_tab(tab_control, filtered_tabs, config, "Оптимизация")
                tab_control.add(consolidated_frame, text="Все оптимизации")
            except Exception as e:
                print(f"Ошибка при создании вкладки 'Все оптимизации': {e}")
                import traceback; traceback.print_exc()
    else:
        # Традиционные вкладки для каждой категории
        try:
            optimization_frame = create_optimization_tab(tab_control, config)
            tab_control.add(optimization_frame, text="Оптимизация")
        except Exception as e:
            print(f"Ошибка при создании вкладки оптимизации: {e}")
            import traceback; traceback.print_exc()

        for tab_name, checkbox_names in filtered_tabs.items():
            tab_frame = ttk.Frame(tab_control)
            tab_control.add(tab_frame, text=tab_name)
            placeholder = ttk.Label(tab_frame, text="Загрузка содержимого...", font=("Segoe UI", 12), foreground="#32FBE2")
            placeholder.pack(expand=True)
            tab_frame.tab_info = {
                "name": tab_name,
                "checkbox_names": checkbox_names,
                "loaded": False,
            }

    if tab_control.tabs():
        tab_control.select(0)


"""
+------------------------------------+
| Функция для переключения на        |
| вкладку электропитания             |
+------------------------------------+
"""


def switch_to_power():
    # Проверяем режим разработчика
    developer_mode = config.getboolean("General", "developer_mode", fallback=False)
    if not developer_mode:
        messagebox.showwarning(
            "Режим разработчика отключен",
            "Вкладка 'Электропитание' доступна только в режиме разработчика.\n\nВключите режим разработчика в Настройки → Дополнительно → Режим разработчика"
        )
        return

    # Удаляем все существующие вкладки
    for tab in tab_control.tabs():
        tab_control.forget(tab)

    # Добавляем специальную вкладку с таблицей
    power_tab = create_power_tab()
    tab_control.add(power_tab, text="Электропитание")

    # Добавляем остальные вкладки из tabs_2 (если нужно)
    developer_mode = config.getboolean("General", "developer_mode", fallback=False)
    dangerous_power_tabs = ["Адские режимы электропитания", "Схемы где ЗАГРУЖЕННОСТЬ ПРОЦЕССОРА 100%", "Все планы электропитания"]
    
    frames_mode = config.getboolean("General", "frames_instead_of_tabs", fallback=False)

    if frames_mode:
        filtered_power = {}
        for tab_name, checkbox_names in tabs_2.items():
            if tab_name != "Электропитание" and not (not developer_mode and tab_name in dangerous_power_tabs):
                filtered_power[tab_name] = checkbox_names
        if filtered_power:
            try:
                cons_frame = create_consolidated_optimization_tab(tab_control, filtered_power, config, "Электропитание")
                tab_control.add(cons_frame, text="Все схемы")
            except Exception as e:
                print(f"Ошибка создания консолидированной вкладки: {e}")
                import traceback; traceback.print_exc()
    else:
        for tab_name, checkbox_names in tabs_2.items():
            if tab_name != "Электропитание":
                if not developer_mode and tab_name in dangerous_power_tabs:
                    continue
                tab_frame = ttk.Frame(tab_control)
                tab_control.add(tab_frame, text=tab_name)

                placeholder = ttk.Label(
                    tab_frame,
                    text="Загрузка содержимого...",
                    font=("Segoe UI", 12),
                    foreground="#32FBE2",
                )
                placeholder.pack(expand=True)

                tab_frame.tab_info = {
                    "name": tab_name,
                    "checkbox_names": checkbox_names,
                    "loaded": False,
                }

    # Выбираем вкладку с таблицей
    tab_control.select(power_tab)


"""
+------------------------------------+
| Функция для переключения на        |
| вкладку с исправлениями            |
+------------------------------------+
"""


def switch_to_fixes():
    # Удаляем все существующие вкладки
    for tab in tab_control.tabs():
        tab_control.forget(tab)

    # Создаем вкладку исправлений
    from tweaks.fixes_tab import create_fixes_tab

    fixes_tab = create_fixes_tab(tab_control)

    # Выбираем вкладку исправлений
    tab_control.select(fixes_tab)


def switch_to_game_mode():
    for tab in tab_control.tabs():
        tab_control.forget(tab)
    from tweaks.game_mode_tab import create_game_mode_tab
    game_tab = create_game_mode_tab(tab_control)
    tab_control.select(game_tab)


"""
+------------------------------------+
| Функция для переключения на        |
| вкладку с очисткой                 |
+------------------------------------+
"""

# Импортируем из tabs_beta.py
from tabs_beta import tabs_uninstall
from app_uninstaller import create_app_uninstall_tab  # Импортируем функцию создания вкладки

# В вашей функции switch_to_clean():

def switch_to_clean():
    # Удаляем все существующие вкладки
    for tab in tab_control.tabs():
        tab_control.forget(tab)

    # Создаем вкладку с удалением приложений (в стиле Win 10 Tweaker)
    # Используем список из tabs_uninstall["Удаление программ"]
    uninstall_frame = create_app_uninstall_tab(
        tab_control, 
        config, 
        tabs_uninstall["Удаление программ"]  # Передаем список скриптов
    )
    tab_control.add(uninstall_frame, text="Приложения")
    
    # Добавляем остальные вкладки из tabs
    developer_mode = config.getboolean("General", "developer_mode", fallback=False)
    dangerous_clean_tabs = ["Очистка", "Удалить приложения (новая версия)", "Удалить приложения (старая версия)"]

    # Добавляем новые вкладки из tabs_4
    novice_mode = config.getboolean("General", "novice_mode", fallback=False)
    tabs_to_use_4 = tabs_4_novice if novice_mode else tabs_4
    
    frames_mode = config.getboolean("General", "frames_instead_of_tabs", fallback=False)

    if frames_mode:
        filtered_clean = {}
        for tab_name, checkbox_names in tabs_to_use_4.items():
            if not novice_mode and not developer_mode and tab_name in dangerous_clean_tabs:
                continue
            filtered_clean[tab_name] = checkbox_names
        if filtered_clean:
            try:
                cons_frame = create_consolidated_optimization_tab(tab_control, filtered_clean, config, "Очистка")
                tab_control.add(cons_frame, text="Все очистки")
            except Exception as e:
                print(f"Ошибка создания консолидированной вкладки: {e}")
                import traceback; traceback.print_exc()
    else:
        for tab_name, checkbox_names in tabs_to_use_4.items():
            if not novice_mode and not developer_mode and tab_name in dangerous_clean_tabs:
                continue
            tab_frame = ttk.Frame(tab_control)
            tab_control.add(tab_frame, text=tab_name)

            placeholder = ttk.Label(
                tab_frame,
                text="Загрузка содержимого...",
                font=("Segoe UI", 12),
                foreground="#32FBE2",
            )
            placeholder.pack(expand=True)

            tab_frame.tab_info = {
                "name": tab_name,
                "checkbox_names": checkbox_names,
                "loaded": False,
            }

    # Выбираем первую вкладку
    if tab_control.tabs():
        tab_control.select(0)

def switch_to_other():
    # Проверяем режим разработчика
    developer_mode = config.getboolean("General", "developer_mode", fallback=False)
    if not developer_mode:
        messagebox.showwarning(
            "Режим разработчика отключен",
            "Вкладка 'Другое' доступна только в режиме разработчика.\n\nВключите режим разработчика в Настройки → Дополнительно → Режим разработчика"
        )
        return
    
    # Удаляем все существующие вкладки
    for tab in tab_control.tabs():
        tab_control.forget(tab)

    tabs_to_use_other = {}
    for tn, names in tabs_uninstall.items():
        tabs_to_use_other[tn] = names
    for tn, names in tabs_5.items():
        tabs_to_use_other[tn] = names

    frames_mode = config.getboolean("General", "frames_instead_of_tabs", fallback=False)
    if frames_mode:
        if tabs_to_use_other:
            try:
                cons_frame = create_consolidated_optimization_tab(tab_control, tabs_to_use_other, config, "Другое")
                tab_control.add(cons_frame, text="Другое")
            except Exception as e:
                print(f"Ошибка создания консолидированной вкладки: {e}")
                import traceback; traceback.print_exc()
    else:
        for tab_name, checkbox_names in tabs_to_use_other.items():
            tab_frame = ttk.Frame(tab_control)
            tab_control.add(tab_frame, text=tab_name)
            placeholder = ttk.Label(
                tab_frame,
                text="Загрузка содержимого...",
                font=("Segoe UI", 12),
                foreground="#32FBE2",
            )
            placeholder.pack(expand=True)
            tab_frame.tab_info = {
                "name": tab_name,
                "checkbox_names": checkbox_names,
                "loaded": False,
            }

    # Выбираем первую вкладку
    if tab_control.tabs():
        tab_control.select(0)

"""
+------------------------------------+
| Функция для переключения на         |
| минималистичную вкладку             |
+------------------------------------+
"""


def switch_to_minimal():
    switch_to_game_mode()


"""
+------------------------------------+
| Функция для отображения информации |
| о версии программы                 |
+------------------------------------+
"""


def switch_to_settings():
    # Удаляем все существующие вкладки
    for tab in tab_control.tabs():
        tab_control.forget(tab)

    # Проверяем режим новичка
    novice_mode = config.getboolean("General", "novice_mode", fallback=False)
    
    # Если режим новичка включен, показываем только специальную вкладку
    if novice_mode:
        # Создаем специальную вкладку для режима новичка
        novice_settings_tab = ttk.Frame(tab_control)
        tab_control.add(novice_settings_tab, text="Настройки")
        
        # Создаем основной контейнер с отступами
        novice_settings_frame = ttk.Frame(novice_settings_tab, padding=20)
        novice_settings_frame.pack(fill="both", expand=True)
        
        # Заголовок настроек
        novice_settings_title = ttk.Label(
            novice_settings_frame, text="Настройки (Режим новичка)", font=("Segoe UI", 16, "bold")
        )
        novice_settings_title.pack(anchor="w", pady=(0, 20))
        
        # Информационное сообщение
        info_label = ttk.Label(
            novice_settings_frame,
            text="В режиме новичка доступны только базовые настройки для вашей безопасности.",
            font=("Segoe UI", 10),
            foreground="gray"
        )
        info_label.pack(anchor="w", pady=(0, 20))
        
        # Секция внешнего вида (только тема)
        appearance_section_novice = ttk.Labelframe(novice_settings_frame, text="Внешний вид", padding=15)
        appearance_section_novice.pack(fill="x", pady=(0, 15))
        
        ttk.Label(appearance_section_novice, text="Тема оформления:", font=("Segoe UI", 10)).pack(
            anchor="w", pady=(0, 5)
        )
        theme_dropdown_novice = ttk.Combobox(
            appearance_section_novice,
            textvariable=theme_var,
            values=root.style.theme_names(),
            width=30,
        )
        theme_dropdown_novice.pack(anchor="w", pady=(0, 10))
        theme_dropdown_novice.bind("<<ComboboxSelected>>", update_theme)
        
        # Секция режима новичка
        mode_section_novice = ttk.Labelframe(novice_settings_frame, text="Режим работы", padding=15)
        mode_section_novice.pack(fill="x", pady=(0, 15))
        
        ttk.Label(mode_section_novice, text="Режим новичка:", font=("Segoe UI", 10)).pack(
            anchor="w", pady=(0, 5)
        )
        novice_mode_var_novice = tk.StringVar(
            value="Включено" if config.getboolean("General", "novice_mode", fallback=False) else "Выключено"
        )
        novice_mode_dropdown_novice = ttk.Combobox(
            mode_section_novice,
            textvariable=novice_mode_var_novice,
            values=["Включено", "Выключено"],
            width=30,
        )
        novice_mode_dropdown_novice.pack(anchor="w", pady=(0, 10))
        
        def update_novice_mode_from_settings(event=None):
            new_value = novice_mode_var_novice.get() == "Включено"
            if not new_value:  # Если выключаем режим новичка
                config["General"]["novice_mode"] = "False"
                with open("user_data//settings.ini", "w", encoding="cp1251") as configfile:
                    config.write(configfile)
                messagebox.showinfo(
                    "Настройка применена",
                    "Режим новичка выключен. Перезапустите программу для применения изменений."
                )
        
        novice_mode_dropdown_novice.bind("<<ComboboxSelected>>", update_novice_mode_from_settings)
        
        return
    
    # Создаем вкладку основных настроек (обычный режим)
    settings1_tab = ttk.Frame(tab_control)
    tab_control.add(settings1_tab, text="Настройки")

    # Создаем canvas и scrollbar для прокрутки
    settings_canvas = tk.Canvas(settings1_tab)
    settings_scrollbar = ttk.Scrollbar(settings1_tab, orient="vertical", command=settings_canvas.yview)
    settings_scrollable_frame = ttk.Frame(settings_canvas)

    def update_scroll_region(event=None):
        settings_canvas.update_idletasks()
        settings_canvas.configure(scrollregion=settings_canvas.bbox("all"))
    
    settings_scrollable_frame.bind("<Configure>", update_scroll_region)

    settings_canvas.create_window((0, 0), window=settings_scrollable_frame, anchor="nw")
    settings_canvas.configure(yscrollcommand=settings_scrollbar.set)
    
    # Обновляем область прокрутки при изменении размера canvas
    def configure_canvas(event):
        canvas_width = event.width
        settings_canvas.itemconfig(settings_canvas.find_all()[0], width=canvas_width)
        update_scroll_region()
    settings_canvas.bind("<Configure>", configure_canvas)

    # Привязываем прокрутку мышкой
    def _on_mousewheel(event):
        settings_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def _bind_to_mousewheel(event):
        settings_canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def _unbind_from_mousewheel(event):
        settings_canvas.unbind_all("<MouseWheel>")
    
    settings_canvas.bind("<Enter>", _bind_to_mousewheel)
    settings_canvas.bind("<Leave>", _unbind_from_mousewheel)

    settings_canvas.pack(side="left", fill="both", expand=True)
    settings_scrollbar.pack(side="right", fill="y")

    # Создаем основной контейнер с отступами
    settings_frame = ttk.Frame(settings_scrollable_frame, padding=20)
    settings_frame.pack(fill="both", expand=True)

    # Заголовок настроек
    settings_title = ttk.Label(
        settings_frame, text="Настройки приложения", font=("Segoe UI", 16, "bold")
    )
    settings_title.pack(anchor="w", pady=(0, 20))

    # Контейнер для трех колонок
    columns_container = ttk.Frame(settings_frame)
    columns_container.pack(fill="both", expand=True)

    # Левая колонка (внешний вид)
    left_column = ttk.Frame(columns_container)
    left_column.pack(side="left", fill="both", expand=True, padx=(0, 15))

    # Средняя колонка (режимы работы и безопасность)
    middle_column = ttk.Frame(columns_container)
    middle_column.pack(side="left", fill="both", expand=True, padx=(0, 15))

    # Правая колонка (дополнительно)
    right_column = ttk.Frame(columns_container)
    right_column.pack(side="left", fill="both", expand=True)

    # Группируем настройки в секции
    appearance_section = ttk.Labelframe(left_column, text="Внешний вид", padding=15)
    appearance_section.pack(fill="x", pady=(0, 15))

    ttk.Label(appearance_section, text="Шрифт:", font=("Segoe UI", 10)).pack(
        anchor="w", pady=(0, 5)
    )
    font_family_dropdown = ttk.Combobox(
        appearance_section,
        textvariable=font_family_var,
        values=font_family_values,
        width=30,
    )
    font_family_dropdown.pack(anchor="w", pady=(0, 10))

    # Фрейм для размера шрифта с полем ввода и кнопкой OK
    font_size_frame = ttk.Frame(appearance_section)
    font_size_frame.pack(anchor="w", pady=(0, 10), fill="x")
    
    ttk.Label(font_size_frame, text="Размер шрифта:", font=("Segoe UI", 10)).pack(
        anchor="w", pady=(0, 5)
    )
    
    font_size_input_frame = ttk.Frame(font_size_frame)
    font_size_input_frame.pack(anchor="w", fill="x")
    
    font_size_entry_var = tk.StringVar(value=str(font_size_var.get()))
    font_size_entry = ttk.Entry(
        font_size_input_frame,
        width=10,
        textvariable=font_size_entry_var
    )
    font_size_entry.pack(side="left", padx=(0, 5))
    
    def apply_font_size():
        try:
            new_size = int(font_size_entry_var.get())
            if 8 <= new_size <= 72:  # Разумные пределы
                font_size_var.set(new_size)
                update_font()
            else:
                messagebox.showerror("Ошибка", "Размер шрифта должен быть от 8 до 72")
                font_size_entry_var.set(str(font_size_var.get()))
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное число")
            font_size_entry_var.set(str(font_size_var.get()))
    
    font_size_ok_btn = ttk.Button(
        font_size_input_frame,
        text="OK",
        command=apply_font_size,
        width=5
    )
    font_size_ok_btn.pack(side="left")
    
    font_size_entry.bind("<Return>", lambda e: apply_font_size())
    
    # Настройка размера шрифта кнопок быстрого доступа
    ttk.Label(appearance_section, text="Размер шрифта кнопок:", font=("Segoe UI", 10)).pack(
        anchor="w", pady=(10, 5)
    )
    
    quick_button_font_size_input_frame = ttk.Frame(appearance_section)
    quick_button_font_size_input_frame.pack(anchor="w", fill="x", pady=(0, 10))
    
    quick_button_font_size_entry_var = tk.StringVar(value=str(quick_button_font_size_var.get()))
    quick_button_font_size_entry = ttk.Entry(
        quick_button_font_size_input_frame,
        width=10,
        textvariable=quick_button_font_size_entry_var
    )
    quick_button_font_size_entry.pack(side="left", padx=(0, 5))
    
    def apply_quick_button_font_size():
        try:
            new_size = int(quick_button_font_size_entry_var.get())
            if 8 <= new_size <= 72:  # Разумные пределы
                quick_button_font_size_var.set(new_size)
                update_button_style()  # Обновляем стиль кнопок
                config["General"]["quick_button_font_size"] = str(new_size)
                with open("user_data//settings.ini", "w", encoding="cp1251") as configfile:
                    config.write(configfile)
            else:
                messagebox.showerror("Ошибка", "Размер шрифта должен быть от 8 до 72")
                quick_button_font_size_entry_var.set(str(quick_button_font_size_var.get()))
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное число")
            quick_button_font_size_entry_var.set(str(quick_button_font_size_var.get()))
    
    quick_button_font_size_ok_btn = ttk.Button(
        quick_button_font_size_input_frame,
        text="OK",
        command=apply_quick_button_font_size,
        width=5
    )
    quick_button_font_size_ok_btn.pack(side="left")
    
    quick_button_font_size_entry.bind("<Return>", lambda e: apply_quick_button_font_size())

    ttk.Label(appearance_section, text="Тема оформления:", font=("Segoe UI", 10)).pack(
        anchor="w", pady=(0, 5)
    )
    theme_dropdown = ttk.Combobox(
        appearance_section,
        textvariable=theme_var,
        values=root.style.theme_names(),
        width=30,
    )
    theme_dropdown.pack(anchor="w", pady=(0, 10))

    # Секция редактора тем
    theme_editor_frame = ttk.Frame(appearance_section)
    theme_editor_frame.pack(fill="x", pady=(10, 0))

    ttk.Label(theme_editor_frame, text="Редактор тем:", font=("Segoe UI", 10)).pack(
        side="left", padx=(0, 10)
    )

    theme_editor_btn = ttk.Button(
        theme_editor_frame,
        text="Открыть редактор",
        bootstyle="danger-outline",
        command=lambda: subprocess.run(["python", "-m", "ttkcreator"]),
    )
    theme_editor_btn.pack(side="left")

    # Секция настроек режима новичка/разработчика (в средней колонке)
    mode_settings_section = ttk.Labelframe(middle_column, text="Режимы работы и безопасность", padding=15)
    mode_settings_section.pack(fill="x", pady=(0, 15))

    # Секция настроек Telegram (удалена, username перенесен в вкладку Телеметрия)

    # Секция дополнительных настроек (перенесена в правую колонку)
    additional_section = ttk.Labelframe(right_column, text="Дополнительно", padding=15)
    additional_section.pack(fill="x", pady=(0, 15))

    ttk.Label(additional_section, text="Подсказки:", font=("Segoe UI", 10)).pack(
        anchor="w", pady=(0, 5)
    )
    tooltip_control_dropdown = ttk.Combobox(
        additional_section,
        textvariable=tooltip_control_var,
        values=["Включено", "Выключено"],
        width=30,
    )
    tooltip_control_dropdown.pack(anchor="w", pady=(0, 10))


    # Создаем переменную для хранения режима отображения чекбоксов
    current_mode = config.get("General", "checkbox_display_mode", fallback="regular")
    mode_map = {
        "regular": "All Tweaker",
        "rectangle": "Hone",
        "expandable": "BoosterX",
        "sapphire": "Sapphire"
    }
    checkbox_display_mode_var = tk.StringVar(
        value=mode_map.get(current_mode, "All Tweaker")
    )

    # Выпадающий список для выбора режима отображения чекбоксов
    ttk.Label(
        additional_section, text="Режим отображения чекбоксов:", font=("Segoe UI", 10)
    ).pack(anchor="w", pady=(0, 5))
    checkbox_display_mode_dropdown = ttk.Combobox(
        additional_section,
        textvariable=checkbox_display_mode_var,
        values=["All Tweaker", "Hone", "BoosterX", "Sapphire"],
        width=30,
    )
    checkbox_display_mode_dropdown.pack(anchor="w", pady=(0, 10))

    # Функция для обновления режима отображения чекбоксов
    def update_checkbox_display_mode(event=None):
        selected_text = checkbox_display_mode_var.get()
        reverse_map = {
            "All Tweaker": "regular",
            "Hone": "rectangle",
            "BoosterX": "expandable",
            "Sapphire": "sapphire"
        }
        new_value = reverse_map.get(selected_text, "regular")
        config["General"]["checkbox_display_mode"] = new_value
        with open("user_data//settings.ini", "w", encoding="cp1251") as configfile:
            config.write(configfile)
        # Показываем сообщение о необходимости перезагрузки вкладки
        messagebox.showinfo(
            "Настройка применена",
            "Режим отображения чекбоксов изменен. Переключитесь на другую вкладку и обратно, чтобы увидеть изменения."
        )

    # Привязываем событие выбора
    checkbox_display_mode_dropdown.bind("<<ComboboxSelected>>", update_checkbox_display_mode)

    # Фреймы вместо вкладок
    frames_var = tk.StringVar(
        value="Включено" if config.getboolean("General", "frames_instead_of_tabs", fallback=True) else "Выключено"
    )
    ttk.Label(
        additional_section, text="Фреймы вместо вкладок:", font=("Segoe UI", 10)
    ).pack(anchor="w", pady=(0, 5))
    frames_dropdown = ttk.Combobox(
        additional_section,
        textvariable=frames_var,
        values=["Включено", "Выключено"],
        width=30,
    )
    frames_dropdown.pack(anchor="w", pady=(0, 10))

    def update_frames_mode(event=None):
        val = frames_var.get() == "Включено"
        config["General"]["frames_instead_of_tabs"] = str(val)
        with open("user_data//settings.ini", "w", encoding="cp1251") as f:
            config.write(f)
        messagebox.showinfo(
            "Настройка применена",
            "Режим отображения изменен. Переключитесь на другую вкладку и обратно, чтобы увидеть изменения."
        )
    frames_dropdown.bind("<<ComboboxSelected>>", update_frames_mode)

    # Полный путь в названиях чекбоксов
    show_path_var = tk.StringVar(
        value="Включено" if config.getboolean("General", "show_checkbox_full_path", fallback=True) else "Выключено"
    )
    ttk.Label(
        additional_section, text="Полный путь в названиях чекбоксов:", font=("Segoe UI", 10)
    ).pack(anchor="w", pady=(0, 5))
    show_path_dropdown = ttk.Combobox(
        additional_section,
        textvariable=show_path_var,
        values=["Включено", "Выключено"],
        width=30,
    )
    show_path_dropdown.pack(anchor="w", pady=(0, 10))

    def update_show_path(event=None):
        val = show_path_var.get() == "Включено"
        config["General"]["show_checkbox_full_path"] = str(val)
        with open("user_data//settings.ini", "w", encoding="cp1251") as f:
            config.write(f)
        messagebox.showinfo(
            "Настройка применена",
            "Настройка сохранена. Переключитесь на другую вкладку и обратно, чтобы увидеть изменения."
        )
    show_path_dropdown.bind("<<ComboboxSelected>>", update_show_path)

    # Количество колонок
    columns_var = tk.StringVar(value=config.get("Columns", "default", fallback="3"))
    ttk.Label(
        additional_section, text="Количество колонок:", font=("Segoe UI", 10)
    ).pack(anchor="w", pady=(0, 5))
    columns_dropdown = ttk.Combobox(
        additional_section,
        textvariable=columns_var,
        values=["1", "2", "3", "4", "5", "6"],
        width=30,
    )
    columns_dropdown.pack(anchor="w", pady=(0, 10))

    def update_columns(event=None):
        val = columns_var.get()
        config["Columns"]["default"] = val
        with open("user_data//settings.ini", "w", encoding="cp1251") as f:
            config.write(f)
        messagebox.showinfo(
            "Настройка применена",
            "Количество колонок изменено. Переключитесь на другую вкладку и обратно, чтобы увидеть изменения."
        )
    columns_dropdown.bind("<<ComboboxSelected>>", update_columns)

    # Новая функция для обновления полноэкранного режима
    def update_fullscreen(event=None):
        new_value = fullscreen_var.get() == "Включено"
        root.attributes("-fullscreen", new_value)
        config["Window"]["fullscreen"] = str(new_value)
        with open("user_data//settings.ini", "w", encoding="cp1251") as configfile:
            config.write(configfile)
        if not new_value:
            root.geometry("1280x720")

    fullscreen_options = ["Включено", "Выключено"]
    ttk.Label(
        additional_section, text="Полноэкранный режим:", font=("Segoe UI", 10)
    ).pack(anchor="w", pady=(0, 5))
    fullscreen_dropdown = ttk.Combobox(
        additional_section,
        textvariable=fullscreen_var,
        values=fullscreen_options,
        width=30,
    )
    fullscreen_dropdown.pack(anchor="w", pady=(0, 10))

    # Привязываем событие выбора
    fullscreen_dropdown.bind("<<ComboboxSelected>>", update_fullscreen)

    # # Настройка видимости верхнего меню
    # show_top_panel_var = tk.StringVar(
    #     value="Включено"
    #     if config.getboolean("General", "show_top_panel", fallback=True)
    #     else "Выключено"
    # )
    # ttk.Label(
    #     additional_section, text="Показывать верхнее меню:", font=("Segoe UI", 10)
    # ).pack(anchor="w", pady=(0, 5))
    # show_top_panel_dropdown = ttk.Combobox(
    #     additional_section,
    #     textvariable=show_top_panel_var,
    #     values=["Включено", "Выключено"],
    #     width=30,
    # )
    # show_top_panel_dropdown.pack(anchor="w", pady=(0, 10))

    # def update_top_panel_visibility(event=None):
    #     new_value = show_top_panel_var.get() == "Включено"
    #     config["General"]["show_top_panel"] = str(new_value)
    #     with open("user_data//settings.ini", "w", encoding="cp1251") as configfile:
    #         config.write(configfile)
    #     # Применяем изменения сразу
    #     if new_value:
    #         # Упаковываем top_panel перед content_container
    #         top_panel.pack(fill="x", pady=(0, 20), before=content_container)
    #     else:
    #         top_panel.pack_forget()

    # show_top_panel_dropdown.bind("<<ComboboxSelected>>", update_top_panel_visibility)

    # # Настройка видимости бокового меню
    # show_sidebar_var = tk.StringVar(
    #     value="Включено"
    #     if config.getboolean("General", "show_sidebar", fallback=True)
    #     else "Выключено"
    # )
    # ttk.Label(
    #     additional_section, text="Показывать боковое меню:", font=("Segoe UI", 10)
    # ).pack(anchor="w", pady=(0, 5))
    # show_sidebar_dropdown = ttk.Combobox(
    #     additional_section,
    #     textvariable=show_sidebar_var,
    #     values=["Включено", "Выключено"],
    #     width=30,
    # )
    # show_sidebar_dropdown.pack(anchor="w", pady=(0, 10))

    # def update_sidebar_visibility(event=None):
    #     new_value = show_sidebar_var.get() == "Включено"
    #     config["General"]["show_sidebar"] = str(new_value)
    #     with open("user_data//settings.ini", "w", encoding="cp1251") as configfile:
    #         config.write(configfile)
    #     # Применяем изменения сразу
    #     if new_value:
    #         # Упаковываем sidebar перед tab_control, чтобы он был слева
    #         sidebar.pack(side="left", fill="y", padx=(0, 20), before=tab_control)
    #     else:
    #         sidebar.pack_forget()

    # show_sidebar_dropdown.bind("<<ComboboxSelected>>", update_sidebar_visibility)

    # # Настройка автообновления
    # auto_update_var = tk.StringVar(
    #     value="Включено"
    #     if config.getboolean("General", "auto_update_enabled", fallback=True)
    #     else "Выключено"
    # )
    # ttk.Label(
    #     additional_section, text="Автообновление:", font=("Segoe UI", 10)
    # ).pack(anchor="w", pady=(10, 5))
    # auto_update_dropdown = ttk.Combobox(
    #     additional_section,
    #     textvariable=auto_update_var,
    #     values=["Включено", "Выключено"],
    #     width=30,
    # )
    # auto_update_dropdown.pack(anchor="w", pady=(0, 10))

    # def update_auto_update(event=None):
    #     new_value = auto_update_var.get() == "Включено"
    #     config["General"]["auto_update_enabled"] = str(new_value)
    #     with open("user_data//settings.ini", "w", encoding="cp1251") as configfile:
    #         config.write(configfile)

    # auto_update_dropdown.bind("<<ComboboxSelected>>", update_auto_update)

    # # Привязываем события к элементам управления
    # font_family_dropdown.bind("<<ComboboxSelected>>", update_font)
    # theme_dropdown.bind("<<ComboboxSelected>>", update_theme)
    # tooltip_control_dropdown.bind("<<ComboboxSelected>>", update_tooltip_state)

    # Настройка начальной вкладки
    ttk.Label(
        additional_section, text="Начальная вкладка:", font=("Segoe UI", 10)
    ).pack(anchor="w", pady=(0, 5))
    initial_tab_dropdown = ttk.Combobox(
        additional_section,
        textvariable=initial_tab_var,
        values=[
            "Главная",
            "Минимальный вид",
            "Оптимизация",
            "Драйверы",
            "Электропитание",
            "Другое",
            "Очистка",
            "Исправления",
            "Настройки",
            "Обновления",
            "Версия",
        ],
        width=30,
    )
    initial_tab_dropdown.pack(anchor="w", pady=(0, 10))

    def update_initial_tab(event=None):
        # Словарь для сопоставления пользовательских названий с именами функций
        tab_mapping = {
            "Главная": "switch_to_main_wrapper",
            "Минимальный вид": "switch_to_minimal_wrapper",
            "Оптимизация": "switch_to_optimization_wrapper",
            "Драйверы": "switch_to_drivers_wrapper",
            "Электропитание": "switch_to_power_wrapper",
            "Другое": "switch_to_other_wrapper",
            "Очистка": "switch_to_clean_wrapper",
            "Исправления": "switch_to_fixes_wrapper",
            # "Настройки": "switch_to_settings_wrapper",
            # "Антон AI": "switch_to_gpt_wrapper",
        }

        # Получаем выбранное пользовательское название и преобразуем его в имя функции
        selected_tab = initial_tab_var.get()
        function_name = tab_mapping.get(selected_tab, "switch_to_main_wrapper")

        config["General"]["initial_tab"] = function_name
        with open("user_data//settings.ini", "w", encoding="cp1251") as configfile:
            config.write(configfile)

    initial_tab_dropdown.bind("<<ComboboxSelected>>", update_initial_tab)

    # # Настройка отключения рекламы
    # ad_enabled_var = tk.StringVar(
    #     value="Включено"
    #     if config.getboolean("General", "ad_enabled", fallback=True)
    #     else "Выключено"
    # )
    # ttk.Label(
    #     additional_section, text="Показывать рекламу:", font=("Segoe UI", 10)
    # ).pack(anchor="w", pady=(0, 5))
    # ad_enabled_dropdown = ttk.Combobox(
    #     additional_section,
    #     textvariable=ad_enabled_var,
    #     values=["Включено", "Выключено"],
    #     width=30,
    # )
    # ad_enabled_dropdown.pack(anchor="w", pady=(0, 10))

    # def update_ad_enabled(event=None):
    #     new_value = ad_enabled_var.get() == "Включено"
    #     config["General"]["ad_enabled"] = str(new_value)
    #     with open("user_data//settings.ini", "w", encoding="cp1251") as configfile:
    #         config.write(configfile)

    # ad_enabled_dropdown.bind("<<ComboboxSelected>>", update_ad_enabled)

    # Настройка режима новичка
    novice_mode_var = tk.StringVar(
        value="Включено"
        if config.getboolean("General", "novice_mode", fallback=False)
        else "Выключено"
    )
    # ttk.Label(
    #     mode_settings_section, text="Режим новичка:", font=("Segoe UI", 10)
    # ).pack(anchor="w", pady=(0, 5))
    novice_mode_dropdown = ttk.Combobox(
        mode_settings_section,
        textvariable=novice_mode_var,
        values=["Включено", "Выключено"],
        width=30,
    )
    # novice_mode_dropdown.pack(anchor="w", pady=(0, 10))

    # Настройка режима разработчика
    developer_mode_var = tk.StringVar(
        value="Включено"
        if config.getboolean("General", "developer_mode", fallback=False)
        else "Выключено"
    )
    # ttk.Label(
    #     mode_settings_section, text="Режим разработчика:", font=("Segoe UI", 10)
    # ).pack(anchor="w", pady=(0, 5))
    developer_mode_dropdown = ttk.Combobox(
        mode_settings_section,
        textvariable=developer_mode_var,
        values=["Включено", "Выключено"],
        width=30,
    )
    # developer_mode_dropdown.pack(anchor="w", pady=(0, 10))

    # Настройка offer_backup
    offer_backup_enabled_var = tk.StringVar(
        value="Включено"
        if config.getboolean("General", "offer_backup_enabled", fallback=True)
        else "Выключено"
    )
    # ttk.Label(
    #     mode_settings_section, text="Предлагать создание бэкапа реестра:", font=("Segoe UI", 10)
    # ).pack(anchor="w", pady=(0, 5))
    offer_backup_enabled_dropdown = ttk.Combobox(
        mode_settings_section,
        textvariable=offer_backup_enabled_var,
        values=["Включено", "Выключено"],
        width=30,
    )
    # offer_backup_enabled_dropdown.pack(anchor="w", pady=(0, 10))

    # Настройка confirm_switch_tab
    confirm_switch_tab_enabled_var = tk.StringVar(
        value="Включено"
        if config.getboolean("General", "confirm_switch_tab_enabled", fallback=True)
        else "Выключено"
    )
    ttk.Label(
        mode_settings_section, text="Подтверждение переключения вкладок:", font=("Segoe UI", 10)
    ).pack(anchor="w", pady=(0, 5))
    confirm_switch_tab_enabled_dropdown = ttk.Combobox(
        mode_settings_section,
        textvariable=confirm_switch_tab_enabled_var,
        values=["Включено", "Выключено"],
        width=30,
    )
    confirm_switch_tab_enabled_dropdown.pack(anchor="w", pady=(0, 10))

    # Функция для синхронизации настроек
    def sync_mode_settings():
        """Синхронизирует настройки режимов и безопасности"""
        # offer_backup_enabled_dropdown.set("Включено" if config.getboolean("General", "offer_backup_enabled", fallback=True) else "Выключено")
        # confirm_switch_tab_enabled_dropdown.set("Включено" if config.getboolean("General", "confirm_switch_tab_enabled", fallback=True) else "Выключено")
        # developer_mode_dropdown.set("Включено" if config.getboolean("General", "developer_mode", fallback=False) else "Выключено")
        # novice_mode_dropdown.set("Включено" if config.getboolean("General", "novice_mode", fallback=False) else "Выключено")
        pass

    def update_novice_mode(event=None):
        new_value = novice_mode_var.get() == "Включено"
        config["General"]["novice_mode"] = str(new_value)
        # Если включаем режим новичка, автоматически включаем другие настройки и выключаем режим разработчика
        if new_value:
            config["General"]["developer_mode"] = "False"
            config["General"]["offer_backup_enabled"] = "True"
            config["General"]["confirm_switch_tab_enabled"] = "True"
            sync_mode_settings()
        # При выключении режима новичка другие настройки НЕ меняются
        with open("user_data//settings.ini", "w", encoding="cp1251") as configfile:
            config.write(configfile)
        messagebox.showinfo(
            "Настройка применена",
            "Режим новичка изменен. Перезапустите программу для применения изменений."
        )

    novice_mode_dropdown.bind("<<ComboboxSelected>>", update_novice_mode)

    def update_developer_mode(event=None):
        new_value = developer_mode_var.get() == "Включено"
        config["General"]["developer_mode"] = str(new_value)
        # Если включаем режим разработчика, выключаем режим новичка
        if new_value:
            config["General"]["novice_mode"] = "False"
            sync_mode_settings()
        # Если выключаем режим разработчика, не меняем другие настройки
        with open("user_data//settings.ini", "w", encoding="cp1251") as configfile:
            config.write(configfile)
        messagebox.showinfo(
            "Настройка применена",
            "Режим разработчика изменен. Перезапустите программу для применения изменений."
        )

    developer_mode_dropdown.bind("<<ComboboxSelected>>", update_developer_mode)

    def update_offer_backup_enabled(event=None):
        new_value = offer_backup_enabled_var.get() == "Включено"
        config["General"]["offer_backup_enabled"] = str(new_value)
        # Если включаем, включаем все остальные настройки безопасности
        if new_value:
            config["General"]["confirm_switch_tab_enabled"] = "True"
            config["General"]["developer_mode"] = "False"
            config["General"]["novice_mode"] = "False"
            sync_mode_settings()
        # Если выключаем, выключаем все остальные настройки безопасности и включаем режим разработчика
        else:
            config["General"]["confirm_switch_tab_enabled"] = "False"
            config["General"]["developer_mode"] = "True"
            config["General"]["novice_mode"] = "False"
            sync_mode_settings()
        with open("user_data//settings.ini", "w", encoding="cp1251") as configfile:
            config.write(configfile)

    offer_backup_enabled_dropdown.bind("<<ComboboxSelected>>", update_offer_backup_enabled)

    def update_confirm_switch_tab_enabled(event=None):
        new_value = confirm_switch_tab_enabled_var.get() == "Включено"
        config["General"]["confirm_switch_tab_enabled"] = str(new_value)
        # Если включаем, включаем все остальные настройки безопасности
        if new_value:
            config["General"]["offer_backup_enabled"] = "True"
            config["General"]["developer_mode"] = "False"
            config["General"]["novice_mode"] = "False"
            sync_mode_settings()
        # Если выключаем, выключаем все остальные настройки безопасности и включаем режим разработчика
        else:
            config["General"]["offer_backup_enabled"] = "False"
            config["General"]["developer_mode"] = "True"
            config["General"]["novice_mode"] = "False"
            sync_mode_settings()
        with open("user_data//settings.ini", "w", encoding="cp1251") as configfile:
            config.write(configfile)

    confirm_switch_tab_enabled_dropdown.bind("<<ComboboxSelected>>", update_confirm_switch_tab_enabled)

    # Настройка способа запуска твиков
    tweak_execution_mode_var = tk.StringVar(
        value=config.get("General", "tweak_execution_mode", fallback="default")
    )
    ttk.Label(
        mode_settings_section, text="Способ запуска твиков:", font=("Segoe UI", 10)
    ).pack(anchor="w", pady=(0, 5))
    tweak_execution_mode_dropdown = ttk.Combobox(
        mode_settings_section,
        textvariable=tweak_execution_mode_var,
        values=["default", "no_launcher", "launcher", "powerrun", "cmd", "create_config_and_run"],
        width=30,
    )
    tweak_execution_mode_dropdown.pack(anchor="w", pady=(0, 10))
    
    # Описание режимов запуска
    execution_mode_descriptions = {
        "default": "По умолчанию (как в функции по дефолту)",
        "no_launcher": "Без launcher (только cmd /c)",
        "launcher": "С launcher (Utils\\launcher.exe)",
        "powerrun": "Через PowerRun (Utils\\PowerRun.exe)",
        "cmd": "Через cmd /c (только cmd /c)",
        "create_config_and_run": "Создать конфиг и запустить твики"
    }
    
    execution_mode_label = ttk.Label(
        mode_settings_section,
        text=execution_mode_descriptions.get(tweak_execution_mode_var.get(), ""),
        font=("Segoe UI", 9),
        foreground="gray"
    )
    execution_mode_label.pack(anchor="w", pady=(0, 10))
    
    def update_tweak_execution_mode(event=None):
        new_value = tweak_execution_mode_var.get()
        config["General"]["tweak_execution_mode"] = new_value
        with open("user_data//settings.ini", "w", encoding="cp1251") as configfile:
            config.write(configfile)
        # Обновляем описание
        execution_mode_label.config(
            text=execution_mode_descriptions.get(new_value, "")
        )
        messagebox.showinfo(
            "Настройка применена",
            "Способ запуска твиков изменен."
        )
    
    tweak_execution_mode_dropdown.bind("<<ComboboxSelected>>", update_tweak_execution_mode)

    # # Добавляем вкладку "Остальное"
    # other_tab = ttk.Frame(tab_control)
    # tab_control.add(other_tab, text="Остальное")

    # # Создаем основной контейнер с отступами
    # other_frame = ttk.Frame(other_tab, padding=20)
    # other_frame.pack(fill="both", expand=True)

    # # Заголовок
    # other_title = ttk.Label(
    #     other_frame, text="Дополнительные настройки", font=("Segoe UI", 16, "bold")
    # )
    # other_title.pack(anchor="w", pady=(0, 20))

    # # Контейнер для двух колонок
    # other_columns_container = ttk.Frame(other_frame)
    # other_columns_container.pack(fill="both", expand=True)

    # # Левая колонка
    # other_left_column = ttk.Frame(other_columns_container)
    # other_left_column.pack(side="left", fill="both", expand=True, padx=(0, 15))

    # # Правая колонка
    # other_right_column = ttk.Frame(other_columns_container)
    # other_right_column.pack(side="right", fill="both", expand=True)

    # # Секция управления конфигурациями в левой колонке
    # config_section = ttk.Labelframe(
    #     other_left_column, text="Управление конфигурациями", padding=15
    # )
    # config_section.pack(fill="x", pady=(0, 15))

    # # Выпадающий список файлов конфигурации
    # config_file_dropdown = ttk.Combobox(
    #     config_section,
    #     textvariable=config_file_var,
    #     values=config_file_values,
    #     width=width,
    #     font=("Segoe UI", 10),
    # )
    # config_file_dropdown.pack(side="left", padx=5)

    # # Кнопка выполнения конфига
    # execute_config_button = ttk.Button(
    #     config_section,
    #     text="Выполнить конфиг",
    #     bootstyle="danger-outline",
    #     command=execute_config,
    # )
    # execute_config_button.pack(side="left", padx=5)

    # # Секция настроек колонок в левой колонке
    # columns_settings_frame = ttk.Labelframe(
    #     other_left_column, text="Настройки колонок", padding=15
    # )
    # columns_settings_frame.pack(fill="x", pady=(0, 15))

    # # Кнопка открытия настроек колонок
    # open_columns_settings_button = ttk.Button(
    #     columns_settings_frame,
    #     text="Открыть настройки колонок",
    #     bootstyle="danger-outline",
    #     command=open_columns_settings_window,
    # )
    # open_columns_settings_button.pack(side="left", padx=5)

    # # Добавляем фрейм для кнопок экспорта/импорта в правую колонку
    # import_export_section = ttk.Labelframe(
    #     other_right_column, text="Импорт/Экспорт", padding=15
    # )
    # import_export_section.pack(fill="x", expand=False, pady=(0, 0))

    # # Добавляем фрейм для кнопок экспорта/импорта
    # settings_buttons_frame = ttk.Frame(import_export_section)
    # settings_buttons_frame.pack(fill="x", pady=(0, 0))

    # # Кнопка экспорта настроек
    # export_button = ttk.Button(
    #     settings_buttons_frame,
    #     text="Экспорт настроек",
    #     bootstyle="success-outline",
    #     command=export_settings,
    # )
    # export_button.pack(side="left", padx=5)

    # # Кнопка импорта настроек
    # import_button = ttk.Button(
    #     settings_buttons_frame,
    #     text="Импорт настроек",
    #     bootstyle="success-outline",
    #     command=lambda: import_settings() and root.destroy() and root.quit(),
    # )
    # import_button.pack(side="left", padx=5)

#     # Добавляем вкладку для управления элементами
#     elements_tab = ttk.Frame(tab_control)
#     tab_control.add(elements_tab, text="Интегратор")

#     # Создаем основной контейнер с отступами
#     elements_container = ttk.Frame(elements_tab, padding=15)
#     elements_container.pack(fill="both", expand=True)

#     # Заголовок
#     ttk.Label(
#         elements_container,
#         text="Добавить элементы в контекстное меню Windows",
#         font=("Segoe UI", 14, "bold"),
#     ).pack(anchor="w", pady=(0, 5))

#     # Описание
#     ttk.Label(
#         elements_container,
#         text="Здесь вы можете добавить программы, файлы, папки и ссылки\nв контекстное меню рабочего стола Windows",
#         font=("Segoe UI", 10),
#     ).pack(anchor="w", pady=(0, 15))

#     # Программа для добавления
#     program_frame = ttk.Labelframe(
#         elements_container,
#         text="Программа, файл, папка или ссылка для добавления",
#         padding=10,
#     )
#     program_frame.pack(fill="x", pady=(0, 10))

#     program_entry = ttk.Entry(program_frame)
#     program_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

#     def select_program():
#         filename = filedialog.askopenfilename(
#             title="Выберите элемент для добавления",
#             filetypes=[
#                 ("Все файлы", "*.*"),
#                 ("EXE файлы", "*.exe"),
#                 ("BAT файлы", "*.bat"),
#             ],
#         )
#         if filename:
#             program_entry.delete(0, tk.END)
#             program_entry.insert(0, filename)

#     ttk.Button(program_frame, text="...", width=3, command=select_program).pack(
#         side="right"
#     )

#     # Значок для добавления
#     icon_frame = ttk.Labelframe(
#         elements_container, text="Значок для пункта меню (необязательно)", padding=10
#     )
#     icon_frame.pack(fill="x", pady=(0, 10))

#     icon_entry = ttk.Entry(icon_frame)
#     icon_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

#     def select_icon():
#         filename = filedialog.askopenfilename(
#             title="Выберите значок",
#             filetypes=[
#                 ("ICO файлы", "*.ico"),
#                 ("EXE файлы", "*.exe"),
#                 ("Все файлы", "*.*"),
#             ],
#         )
#         if filename:
#             icon_entry.delete(0, tk.END)
#             icon_entry.insert(0, filename)

#     ttk.Button(icon_frame, text="...", width=3, command=select_icon).pack(side="right")

#     # Положение элемента
#     position_frame = ttk.Labelframe(
#         elements_container, text="Расположение в контекстном меню", padding=10
#     )
#     position_frame.pack(fill="x", pady=(0, 10))

#     position = tk.StringVar(value="Сверху")
#     ttk.Radiobutton(
#         position_frame, text="Сверху", variable=position, value="Сверху"
#     ).pack(side="left", padx=5)
#     ttk.Radiobutton(
#         position_frame, text="По центру", variable=position, value="По центру"
#     ).pack(side="left", padx=5)
#     ttk.Radiobutton(
#         position_frame, text="Снизу", variable=position, value="Снизу"
#     ).pack(side="left", padx=5)

#     # Название пункта в меню
#     menu_frame = ttk.Labelframe(
#         elements_container, text="Название пункта в контекстном меню", padding=10
#     )
#     menu_frame.pack(fill="x", pady=(0, 10))

#     menu_entry = ttk.Entry(menu_frame)
#     menu_entry.pack(fill="x")

#     def create_reg_file():
#         # Получаем значения из полей ввода
#         program_path = program_entry.get()
#         icon_path = icon_entry.get()
#         menu_name = menu_entry.get()
#         position_value = position.get()

#         # Проверяем, что все поля заполнены
#         if not all([program_path, menu_name]):
#             tk.messagebox.showerror(
#                 "Ошибка", "Пожалуйста, заполните все обязательные поля"
#             )
#             return

#         # Преобразуем положение в формат реестра
#         position_map = {"Сверху": "Top", "По центру": "Middle", "Снизу": "Bottom"}
#         reg_position = position_map.get(position_value, "Top")

#         # Создаем директорию, если она не существует
#         os.makedirs("telemetry\\user_data\\context_menu", exist_ok=True)

#         # Создаем имя файла на основе названия пункта меню
#         safe_filename = "".join(
#             c for c in menu_name if c.isalnum() or c in (" ", "-", "_")
#         ).strip()
#         reg_file_path = f"telemetry\\user_data\\context_menu\\{safe_filename}.reg"

#         # Создаем содержимое reg-файла
#         reg_content = f"""Windows Registry Editor Version 5.00

# [HKEY_LOCAL_MACHINE\\SOFTWARE\\Classes\\DesktopBackground\\Shell\\{menu_name}]
# "Icon"="{icon_path}"
# "Position"="{reg_position}"

# [HKEY_LOCAL_MACHINE\\SOFTWARE\\Classes\\DesktopBackground\\Shell\\{menu_name}\\command]
# @="explorer {program_path}"

# [HKEY_LOCAL_MACHINE\\SOFTWARE\\Classes\\DesktopBackground\\Shell\\{menu_name}\\{menu_name}]
# """

#         # Записываем файл
#         try:
#             with open(reg_file_path, "w", encoding="utf-8") as f:
#                 f.write(reg_content)
#             print("Успех", f"Reg-файл успешно создан:\n{reg_file_path}")
#             subprocess.call(f"Utils\\PowerRun.exe {reg_file_path}", shell=True)
#             print("Успех", "Reg-файл успешно применен")

#             # Очищаем поля ввода
#             program_entry.delete(0, tk.END)
#             icon_entry.delete(0, tk.END)
#             menu_entry.delete(0, tk.END)
#             position.set("Сверху")
#         except Exception as e:
#             print("Ошибка", f"Не удалось создать reg-файл:\n{str(e)}")

#     # Кнопка добавления/изменения
#     ttk.Button(
#         elements_container,
#         text="Добавить в контекстное меню",
#         bootstyle="success-outline",
#         width=25,
#         command=create_reg_file,
#     ).pack(anchor="e", pady=(10, 10))

#     # Фрейм для удаления элементов
#     delete_frame = ttk.Labelframe(
#         elements_container, text="Удаление элементов из контекстного меню", padding=10
#     )
#     delete_frame.pack(fill="x", pady=(0, 10))

#     # Создаем список для элементов меню
#     menu_items_frame = ttk.Frame(delete_frame)
#     menu_items_frame.pack(fill="x", pady=(0, 10))

#     menu_items_list = ttk.Treeview(
#         menu_items_frame, columns=("name",), show="headings", height=10
#     )  # Увеличиваем высоту до 10 строк
#     menu_items_list.heading("name", text="Название элемента")
#     menu_items_list.column("name", width=400)
#     menu_items_list.pack(side="left", fill="x", expand=True)

#     # Добавляем скроллбар
#     scrollbar = ttk.Scrollbar(
#         menu_items_frame, orient="vertical", command=menu_items_list.yview
#     )
#     scrollbar.pack(side="right", fill="y")
#     menu_items_list.configure(yscrollcommand=scrollbar.set)

#     def refresh_menu_items():
#         # Очищаем список
#         for item in menu_items_list.get_children():
#             menu_items_list.delete(item)

#         try:
#             # Запускаем PowerShell команду для получения элементов контекстного меню
#             cmd = 'powershell -Command "Get-ChildItem -Path HKLM:\\SOFTWARE\\Classes\\DesktopBackground\\Shell | Select-Object PSChildName"'
#             result = subprocess.check_output(cmd, shell=True, text=True)

#             # Разбираем вывод и добавляем элементы в список
#             for line in result.splitlines():
#                 if (
#                     line.strip()
#                     and not line.startswith("PSChildName")
#                     and not line.strip() == "-----------"
#                 ):
#                     menu_items_list.insert("", "end", values=(line.strip(),))
#         except Exception as e:
#             print(f"Ошибка при получении списка элементов: {str(e)}")

#     def delete_menu_item():
#         selected = menu_items_list.selection()
#         if not selected:
#             # tk.messagebox.showerror("Ошибка", "Выберите элемент для удаления")
#             print("Ошибка", "Выберите элемент для удаления")
#             return

#         item = menu_items_list.item(selected[0])
#         menu_name = item["values"][0]

#         if tk.messagebox.askyesno(
#             "Подтверждение",
#             f"Вы уверены, что хотите удалить '{menu_name}' из контекстного меню?",
#         ):
#             try:
#                 # Создаем временный reg-файл для удаления
#                 reg_content = f"""Windows Registry Editor Version 5.00

# [-HKEY_LOCAL_MACHINE\\SOFTWARE\\Classes\\DesktopBackground\\Shell\\{menu_name}]"""

#                 temp_file = (
#                     f"telemetry\\user_data\\context_menu\\delete_{menu_name}.reg"
#                 )
#                 os.makedirs(os.path.dirname(temp_file), exist_ok=True)

#                 with open(temp_file, "w", encoding="utf-8") as f:
#                     f.write(reg_content)

#                 # Применяем reg-файл
#                 subprocess.call(f"Utils\\PowerRun.exe {temp_file}", shell=True)

#                 # Обновляем список
#                 refresh_menu_items()

#                 # tk.messagebox.showinfo("Успех", f"Элемент '{menu_name}' успешно удален")
#                 print("Успех", f"Элемент '{menu_name}' успешно удален")
#             except Exception as e:
#                 # tk.messagebox.showerror("Ошибка", f"Не удалось удалить элемент:\n{str(e)}")
#                 print("Ошибка", f"Не удалось удалить элемент:\n{str(e)} ")

#     # Кнопки управления
#     buttons_frame = ttk.Frame(delete_frame)
#     buttons_frame.pack(fill="x", pady=(0, 5))

#     ttk.Button(
#         buttons_frame,
#         text="Обновить список",
#         bootstyle="danger-outline",
#         width=20,
#         command=refresh_menu_items,
#     ).pack(side="left", padx=5)

#     ttk.Button(
#         buttons_frame,
#         text="Удалить выбранное",
#         bootstyle="danger-outline",
#         width=20,
#         command=delete_menu_item,
#     ).pack(side="left", padx=5)

#     # Добавляем вкладку "Режим разработчика" (только если режим разработчика включен)
#     developer_mode = config.getboolean("General", "developer_mode", fallback=False)
#     if developer_mode:
#         developer_tab = ttk.Frame(tab_control)
#         tab_control.add(developer_tab, text="Режим разработчика")
        
#         # Создаем Canvas и Scrollbar для прокрутки
#         developer_canvas = tk.Canvas(developer_tab)
#         developer_scrollbar = ttk.Scrollbar(developer_tab, orient="vertical", command=developer_canvas.yview)
#         developer_scrollable_frame = ttk.Frame(developer_canvas)
        
#         developer_scrollable_frame.bind(
#             "<Configure>",
#             lambda e: developer_canvas.configure(scrollregion=developer_canvas.bbox("all"))
#         )
        
#         developer_canvas.create_window((0, 0), window=developer_scrollable_frame, anchor="nw")
#         developer_canvas.configure(yscrollcommand=developer_scrollbar.set)
        
#         def on_developer_mousewheel(event):
#             developer_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
#         developer_canvas.bind_all("<MouseWheel>", on_developer_mousewheel)
        
#         def configure_developer_scroll_region(event):
#             canvas_width = event.width
#             canvas_items = developer_canvas.find_all()
#             if canvas_items:
#                 developer_canvas.itemconfig(canvas_items[0], width=canvas_width)
#             developer_canvas.configure(scrollregion=developer_canvas.bbox("all"))
        
#         developer_canvas.bind('<Configure>', configure_developer_scroll_region)
        
#         developer_canvas.pack(side="left", fill="both", expand=True)
#         developer_scrollbar.pack(side="right", fill="y")
        
#         # Создаем основной контейнер
#         developer_frame = ttk.Frame(developer_scrollable_frame, padding=20)
#         developer_frame.pack(fill="both", expand=True)
        
#         # Заголовок
#         developer_title = ttk.Label(
#             developer_frame, text="Инструменты разработчика", font=("Segoe UI", 16, "bold")
#         )
#         developer_title.pack(anchor="w", pady=(0, 20))
        
#         # Импортируем функции разработчика
#         try:
#             from tweaks.developer_tools import (
#                 clear_tweaks,
#                 remove_attributes_and_delete_files,
#                 remove_numbers_and_points_from_start,
#                 convert_reg_to_bat,
#                 remove_pause_and_exit_from_bat,
#                 create_tabs_file,
#                 translate_tweaks
#             )
#         except ImportError as e:
#             error_label = ttk.Label(
#                 developer_frame,
#                 text=f"Ошибка импорта модуля developer_tools: {e}",
#                 font=("Segoe UI", 10),
#                 foreground="red"
#             )
#             error_label.pack(anchor="w", pady=(0, 20))
        
#         # Секция очистки твиков
#         cleanup_section = ttk.Labelframe(developer_frame, text="Очистка твиков", padding=15)
#         cleanup_section.pack(fill="x", pady=(0, 15))
        
#         # Секция удаления файлов по расширениям
#         delete_files_section = ttk.Labelframe(developer_frame, text="Удаление файлов по расширениям", padding=15)
#         delete_files_section.pack(fill="x", pady=(0, 15))
        
#         ttk.Label(
#             delete_files_section,
#             text="Удалить все файлы с указанными расширениями",
#             font=("Segoe UI", 10),
#             wraplength=600,
#             justify="left"
#         ).pack(anchor="w", pady=(0, 10))
        
#         delete_target_dir_var = tk.StringVar(value="tweaks")
#         ttk.Label(delete_files_section, text="Целевая директория:", font=("Segoe UI", 10)).pack(anchor="w", pady=(0, 5))
#         delete_target_dir_entry = ttk.Entry(delete_files_section, textvariable=delete_target_dir_var, width=50)
#         delete_target_dir_entry.pack(anchor="w", pady=(0, 10))
        
#         extensions_var = tk.StringVar(value=".lnk, .ico, .txt, .png, .jpg, .exe, .ini")
#         ttk.Label(delete_files_section, text="Расширения (через запятую):", font=("Segoe UI", 10)).pack(anchor="w", pady=(0, 5))
#         extensions_entry = ttk.Entry(delete_files_section, textvariable=extensions_var, width=50)
#         extensions_entry.pack(anchor="w", pady=(0, 10))
        
#         def execute_delete_files():
#             target_dir = delete_target_dir_var.get()
#             extensions_str = extensions_var.get()
#             if not target_dir or not extensions_str:
#                 messagebox.showerror("Ошибка", "Заполните все поля")
#                 return
#             extensions = [ext.strip() for ext in extensions_str.split(",")]
#             if messagebox.askyesno("Подтверждение", f"Удалить файлы с расширениями {extensions} в директории {target_dir}?"):
#                 try:
#                     result = remove_attributes_and_delete_files(target_dir, extensions)
#                     messagebox.showinfo(
#                         "Удаление завершено",
#                         f"Удалено файлов: {result['deleted_count']}\nОшибок: {len(result['errors'])}"
#                     )
#                 except Exception as e:
#                     messagebox.showerror("Ошибка", f"Ошибка при удалении: {e}")
        
#         ttk.Button(
#             delete_files_section,
#             text="Удалить файлы",
#             bootstyle="danger-outline",
#             command=execute_delete_files
#         ).pack(anchor="w", pady=(0, 10))
        
#         # Секция удаления чисел и точек из начала имен
#         rename_section = ttk.Labelframe(developer_frame, text="Удаление чисел и точек из начала имен", padding=15)
#         rename_section.pack(fill="x", pady=(0, 15))
        
#         ttk.Label(
#             rename_section,
#             text="Удалить числа и точки из начала имен файлов и папок",
#             font=("Segoe UI", 10),
#             wraplength=600,
#             justify="left"
#         ).pack(anchor="w", pady=(0, 10))
        
#         rename_target_dir_var = tk.StringVar(value="tweaks")
#         ttk.Label(rename_section, text="Целевая директория:", font=("Segoe UI", 10)).pack(anchor="w", pady=(0, 5))
#         rename_target_dir_entry = ttk.Entry(rename_section, textvariable=rename_target_dir_var, width=50)
#         rename_target_dir_entry.pack(anchor="w", pady=(0, 10))
        
#         def execute_rename():
#             target_dir = rename_target_dir_var.get()
#             if not target_dir:
#                 messagebox.showerror("Ошибка", "Укажите целевую директорию")
#                 return
#             if messagebox.askyesno("Подтверждение", f"Удалить числа и точки из начала имен в директории {target_dir}?"):
#                 try:
#                     result = remove_numbers_and_points_from_start(target_dir)
#                     messagebox.showinfo(
#                         "Переименование завершено",
#                         f"Переименовано файлов: {result['renamed_files']}\n"
#                         f"Переименовано папок: {result['renamed_dirs']}\n"
#                         f"Удалено пустых папок: {result['deleted_empty_dirs']}\n"
#                         f"Ошибок: {len(result['errors'])}"
#                     )
#                 except Exception as e:
#                     messagebox.showerror("Ошибка", f"Ошибка при переименовании: {e}")
        
#         ttk.Button(
#             rename_section,
#             text="Выполнить переименование",
#             bootstyle="warning-outline",
#             command=execute_rename
#         ).pack(anchor="w", pady=(0, 10))
        
#         # Секция конвертации .reg в .bat
#         convert_section = ttk.Labelframe(developer_frame, text="Конвертация .reg файлов в .bat", padding=15)
#         convert_section.pack(fill="x", pady=(0, 15))
        
#         ttk.Label(
#             convert_section,
#             text="Рекурсивно конвертировать все .reg файлы в .bat",
#             font=("Segoe UI", 10),
#             wraplength=600,
#             justify="left"
#         ).pack(anchor="w", pady=(0, 10))
        
#         convert_target_dir_var = tk.StringVar(value=".")
#         ttk.Label(convert_section, text="Целевая директория:", font=("Segoe UI", 10)).pack(anchor="w", pady=(0, 5))
#         convert_target_dir_entry = ttk.Entry(convert_section, textvariable=convert_target_dir_var, width=50)
#         convert_target_dir_entry.pack(anchor="w", pady=(0, 10))
        
#         reg_convert_path_var = tk.StringVar(value="RegConvert.exe")
#         ttk.Label(convert_section, text="Путь к RegConvert.exe:", font=("Segoe UI", 10)).pack(anchor="w", pady=(0, 5))
#         reg_convert_path_entry = ttk.Entry(convert_section, textvariable=reg_convert_path_var, width=50)
#         reg_convert_path_entry.pack(anchor="w", pady=(0, 10))
        
#         def execute_convert():
#             target_dir = convert_target_dir_var.get()
#             reg_convert_path = reg_convert_path_var.get()
#             if not target_dir or not reg_convert_path:
#                 messagebox.showerror("Ошибка", "Заполните все поля")
#                 return
#             if messagebox.askyesno("Подтверждение", f"Конвертировать .reg файлы в .bat в директории {target_dir}?"):
#                 try:
#                     result = convert_reg_to_bat(target_dir, reg_convert_path)
#                     messagebox.showinfo(
#                         "Конвертация завершена",
#                         f"Сконвертировано файлов: {result['converted_count']}\nОшибок: {result['error_count']}"
#                     )
#                 except Exception as e:
#                     messagebox.showerror("Ошибка", f"Ошибка при конвертации: {e}")
        
#         ttk.Button(
#             convert_section,
#             text="Выполнить конвертацию",
#             bootstyle="info-outline",
#             command=execute_convert
#         ).pack(anchor="w", pady=(0, 10))
        
#         # Секция удаления pause и exit из bat файлов
#         remove_pause_section = ttk.Labelframe(developer_frame, text="Удаление pause и exit из bat файлов", padding=15)
#         remove_pause_section.pack(fill="x", pady=(0, 15))
        
#         ttk.Label(
#             remove_pause_section,
#             text="Удалить строки 'pause' и 'exit' из всех .bat и .cmd файлов",
#             font=("Segoe UI", 10),
#             wraplength=600,
#             justify="left"
#         ).pack(anchor="w", pady=(0, 10))
        
#         remove_pause_target_dir_var = tk.StringVar(value="tweaks")
#         ttk.Label(remove_pause_section, text="Целевая директория:", font=("Segoe UI", 10)).pack(anchor="w", pady=(0, 5))
#         remove_pause_target_dir_entry = ttk.Entry(remove_pause_section, textvariable=remove_pause_target_dir_var, width=50)
#         remove_pause_target_dir_entry.pack(anchor="w", pady=(0, 10))
        
#         def execute_remove_pause():
#             target_dir = remove_pause_target_dir_var.get()
#             if not target_dir:
#                 messagebox.showerror("Ошибка", "Укажите целевую директорию")
#                 return
#             if messagebox.askyesno("Подтверждение", f"Удалить pause и exit из bat файлов в директории {target_dir}?"):
#                 try:
#                     result = remove_pause_and_exit_from_bat(target_dir)
#                     messagebox.showinfo(
#                         "Обработка завершена",
#                         f"Обработано файлов: {result['processed_count']}\nОшибок: {len(result['errors'])}"
#                     )
#                 except Exception as e:
#                     messagebox.showerror("Ошибка", f"Ошибка при обработке: {e}")
        
#         ttk.Button(
#             remove_pause_section,
#             text="Выполнить обработку",
#             bootstyle="warning-outline",
#             command=execute_remove_pause
#         ).pack(anchor="w", pady=(0, 10))
        
#         # Секция создания tabs.py
#         create_tabs_section = ttk.Labelframe(developer_frame, text="Создание файла tabs.py", padding=15)
#         create_tabs_section.pack(fill="x", pady=(0, 15))
        
#         ttk.Label(
#             create_tabs_section,
#             text="Создать файл tabs.py со структурой каталогов",
#             font=("Segoe UI", 10),
#             wraplength=600,
#             justify="left"
#         ).pack(anchor="w", pady=(0, 10))
        
#         create_tabs_target_dir_var = tk.StringVar(value=".")
#         ttk.Label(create_tabs_section, text="Целевая директория:", font=("Segoe UI", 10)).pack(anchor="w", pady=(0, 5))
#         create_tabs_target_dir_entry = ttk.Entry(create_tabs_section, textvariable=create_tabs_target_dir_var, width=50)
#         create_tabs_target_dir_entry.pack(anchor="w", pady=(0, 10))
        
#         output_file_var = tk.StringVar(value="tabs.py")
#         ttk.Label(create_tabs_section, text="Имя выходного файла:", font=("Segoe UI", 10)).pack(anchor="w", pady=(0, 5))
#         output_file_entry = ttk.Entry(create_tabs_section, textvariable=output_file_var, width=50)
#         output_file_entry.pack(anchor="w", pady=(0, 10))
        
#         def execute_create_tabs():
#             target_dir = create_tabs_target_dir_var.get()
#             output_file = output_file_var.get()
#             if not target_dir or not output_file:
#                 messagebox.showerror("Ошибка", "Заполните все поля")
#                 return
#             if messagebox.askyesno("Подтверждение", f"Создать файл {output_file} в директории {target_dir}?"):
#                 try:
#                     result = create_tabs_file(target_dir, output_file)
#                     if result['output_path']:
#                         messagebox.showinfo(
#                             "Файл создан",
#                             f"Файл создан: {result['output_path']}\nКоличество tabs: {result.get('tabs_count', 0)}"
#                         )
#                     else:
#                         messagebox.showerror("Ошибка", f"Не удалось создать файл. Ошибки: {result['errors']}")
#                 except Exception as e:
#                     messagebox.showerror("Ошибка", f"Ошибка при создании файла: {e}")
        
#         ttk.Button(
#             create_tabs_section,
#             text="Создать tabs.py",
#             bootstyle="success-outline",
#             command=execute_create_tabs
#         ).pack(anchor="w", pady=(0, 10))
        
#         # Секция перевода твиков
#         translate_section = ttk.Labelframe(developer_frame, text="Перевод твиков", padding=15)
#         translate_section.pack(fill="x", pady=(0, 15))
        
#         ttk.Label(
#             translate_section,
#             text="Перевести названия файлов и папок с английского на русский язык",
#             font=("Segoe UI", 10),
#             wraplength=600,
#             justify="left"
#         ).pack(anchor="w", pady=(0, 10))
        
#         ttk.Label(
#             translate_section,
#             text="Файлы с расширением .pow пропускаются. Защищенные слова (CPU, GPU, RAM и т.д.) не переводятся.",
#             font=("Segoe UI", 9),
#             foreground="gray",
#             wraplength=600,
#             justify="left"
#         ).pack(anchor="w", pady=(0, 10))
        
#         translate_target_dir_var = tk.StringVar(value="tweaks")
#         ttk.Label(translate_section, text="Целевая директория:", font=("Segoe UI", 10)).pack(anchor="w", pady=(0, 5))
#         translate_target_dir_entry = ttk.Entry(translate_section, textvariable=translate_target_dir_var, width=50)
#         translate_target_dir_entry.pack(anchor="w", pady=(0, 10))
        
#         dest_language_var = tk.StringVar(value="ru")
#         ttk.Label(translate_section, text="Целевой язык (код языка, например: ru, en, de):", font=("Segoe UI", 10)).pack(anchor="w", pady=(0, 5))
#         dest_language_entry = ttk.Entry(translate_section, textvariable=dest_language_var, width=50)
#         dest_language_entry.pack(anchor="w", pady=(0, 10))
        
#         def execute_translate():
#             target_dir = translate_target_dir_var.get()
#             dest_language = dest_language_var.get().strip()
#             if not target_dir:
#                 messagebox.showerror("Ошибка", "Укажите целевую директорию")
#                 return
#             if not dest_language:
#                 dest_language = "ru"
#             if messagebox.askyesno("Подтверждение", f"Перевести названия файлов и папок в директории {target_dir} на язык {dest_language}?"):
#                 try:
#                     result = translate_tweaks(target_dir, dest_language)
#                     if result['errors']:
#                         error_msg = "\n".join(result['errors'][:5])  # Показываем первые 5 ошибок
#                         if len(result['errors']) > 5:
#                             error_msg += f"\n... и еще {len(result['errors']) - 5} ошибок"
#                         messagebox.showwarning(
#                             "Перевод завершен с ошибками",
#                             f"Переименовано файлов: {result['renamed_files']}\n"
#                             f"Переименовано папок: {result['renamed_dirs']}\n\n"
#                             f"Ошибки:\n{error_msg}"
#                         )
#                     else:
#                         messagebox.showinfo(
#                             "Перевод завершен",
#                             f"Переименовано файлов: {result['renamed_files']}\n"
#                             f"Переименовано папок: {result['renamed_dirs']}"
#                         )
#                 except Exception as e:
#                     messagebox.showerror("Ошибка", f"Ошибка при переводе: {e}")
        
#         ttk.Button(
#             translate_section,
#             text="Выполнить перевод",
#             bootstyle="info-outline",
#             command=execute_translate
#         ).pack(anchor="w", pady=(0, 10))
    
    # # Добавляем вкладки из tabs_6
    # if "tabs_6" in globals():
    #     novice_mode = config.getboolean("General", "novice_mode", fallback=False)
    #     # В режиме новичка используем безопасные твики из tabs_6_novice
    #     tabs_to_use_6 = tabs_6_novice if novice_mode else tabs_6
        
    #     for tab_name, checkbox_names in tabs_to_use_6.items():
    #         tab_frame = ttk.Frame(tab_control)
    #         tab_control.add(tab_frame, text=tab_name)

    #         # Создаем метку-заполнитель
    #         placeholder = ttk.Label(
    #             tab_frame,
    #             text="Загрузка содержимого...",
    #             font=("Segoe UI", 12),
    #             foreground="#32FBE2",
    #         )
    #         placeholder.pack(expand=True)

    #         # Сохраняем информацию о вкладке
    #         tab_frame.tab_info = {
    #             "name": tab_name,
    #             "checkbox_names": checkbox_names,
    #             "loaded": False,
    #         }

#     # Добавляем вкладку телеметрии
#     telemetry_tab = ttk.Frame(tab_control)
#     tab_control.add(telemetry_tab, text="Обратная связь")
#     # tab_control.add(telemetry_tab, text="Телеметрия")

#     # Создаем Canvas и Scrollbar для прокрутки всей вкладки
#     telemetry_canvas = tk.Canvas(telemetry_tab)
#     telemetry_scrollbar_main = ttk.Scrollbar(telemetry_tab, orient="vertical", command=telemetry_canvas.yview)
#     telemetry_scrollable_frame = ttk.Frame(telemetry_canvas)
    
#     telemetry_scrollable_frame.bind(
#         "<Configure>",
#         lambda e: telemetry_canvas.configure(scrollregion=telemetry_canvas.bbox("all"))
#     )
    
#     telemetry_canvas.create_window((0, 0), window=telemetry_scrollable_frame, anchor="nw")
#     telemetry_canvas.configure(yscrollcommand=telemetry_scrollbar_main.set)
    
#     def on_telemetry_mousewheel(event):
#         telemetry_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
#     telemetry_canvas.bind_all("<MouseWheel>", on_telemetry_mousewheel)
    
#     # Обновление размера окна canvas при изменении размера canvas
#     def configure_telemetry_scroll_region(event):
#         canvas_width = event.width
#         canvas_items = telemetry_canvas.find_all()
#         if canvas_items:
#             telemetry_canvas.itemconfig(canvas_items[0], width=canvas_width)
#         telemetry_canvas.configure(scrollregion=telemetry_canvas.bbox("all"))
    
#     telemetry_canvas.bind('<Configure>', configure_telemetry_scroll_region)
    
#     telemetry_canvas.pack(side="left", fill="both", expand=True)
#     telemetry_scrollbar_main.pack(side="right", fill="y")

#     # Создаем основной контейнер с отступами
#     telemetry_frame = ttk.Frame(telemetry_scrollable_frame, padding=20)
#     telemetry_frame.pack(fill="both", expand=True)

#     # Заголовок
#     telemetry_title = ttk.Label(
#         telemetry_frame, text="Обратная связь", font=("Segoe UI", 16, "bold")
#         # telemetry_frame, text="Телеметрия и обратная связь", font=("Segoe UI", 16, "bold")
#     )
#     telemetry_title.pack(anchor="w", pady=(0, 20))

#     # Контейнер для двух колонок
#     columns_container = ttk.Frame(telemetry_frame)
#     columns_container.pack(fill="both", expand=True)

#     # Левая колонка (телеметрия)
#     left_column = ttk.Frame(columns_container)
#     left_column.pack(side="left", fill="both", expand=True, padx=(0, 15))

#     # Правая колонка (обратная связь)
#     right_column = ttk.Frame(columns_container)
#     right_column.pack(side="right", fill="both", expand=True)

#     # Секция телеметрии
#     telemetry_section = ttk.Labelframe(left_column, text="Телеметрия", padding=15)
#     telemetry_section.pack(fill="x", expand=False)

#     # Заголовок
#     ttk.Label(
#         telemetry_section, text="Отправка телеметрии", font=("Segoe UI", 14, "bold")
#     ).pack(anchor="w", pady=(0, 5))

#     # Описание
#     description_text = """Отправка данных о работе программы и настроек для улучшения функциональности и внешнего вида.

# Отправляемые данные:

# • Сообщения об успешном запуске программы
# • Сообщения об ошибках
# • Лог-файлы
# • Настройки Extreme
# • Запущенные твики
# • Время запуска
# • Имя пользователя и версия Windows
# • Список установленных программ для вкладки PostInstall"""

#     ttk.Label(
#         telemetry_section,
#         text=description_text,
#         font=("Segoe UI", 10),
#         wraplength=500,
#         justify="left",
#     ).pack(anchor="w", pady=(0, 10))

#     # Создаем переменную для хранения состояния отправки телеметрии при закрытии
#     send_telemetry_on_close_var = tk.StringVar(
#         value="Включено"
#         if config.getboolean("Telemetry", "send_on_close", fallback=True)
#         else "Выключено"
#     )

#     # Выпадающий список для выбора отправки телеметрии при закрытии
#     ttk.Label(
#         telemetry_section, text="Отправлять телеметрию:", font=("Segoe UI", 10)
#     ).pack(anchor="w", pady=(0, 5))
#     telemetry_on_close_dropdown = ttk.Combobox(
#         telemetry_section,
#         textvariable=send_telemetry_on_close_var,
#         values=["Включено", "Выключено"],
#         width=30,
#     )
#     telemetry_on_close_dropdown.pack(anchor="w", pady=(0, 10))

#     # Функция для обновления настройки отправки телеметрии при закрытии
#     def update_telemetry_on_close(event=None):
#         new_value = send_telemetry_on_close_var.get() == "Включено"
#         config["Telemetry"]["send_on_close"] = str(new_value)
#         with open("user_data//settings.ini", "w", encoding="cp1251") as configfile:
#             config.write(configfile)

#     # Привязываем событие выбора
#     telemetry_on_close_dropdown.bind("<<ComboboxSelected>>", update_telemetry_on_close)

#     # Секция управления Windows Firewall
#     firewall_section = ttk.Labelframe(telemetry_section, text="Управление Windows Firewall", padding=15)
#     firewall_section.pack(fill="x", pady=(15, 0))

#     ttk.Label(
#         firewall_section,
#         text="Управление доступом в интернет для файлов твикера через Windows Firewall",
#         font=("Segoe UI", 10),
#         wraplength=500,
#         justify="left",
#     ).pack(anchor="w", pady=(0, 10))

#     # Функция для включения Windows Firewall
#     def enable_firewall():
#         try:
#             result = subprocess.run(
#                 ["netsh", "advfirewall", "set", "allprofiles", "state", "on"],
#                 capture_output=True,
#                 text=True,
#                 shell=True
#             )
#             if result.returncode == 0:
#                 messagebox.showinfo("Успех", "Windows Firewall включен")
#             else:
#                 messagebox.showerror("Ошибка", f"Не удалось включить Windows Firewall:\n{result.stderr}")
#         except Exception as e:
#             messagebox.showerror("Ошибка", f"Ошибка при включении Windows Firewall: {str(e)}")

#     # Функция для блокировки доступа в интернет
#     def block_internet_access():
#         try:
#             # Включаем firewall сначала
#             enable_firewall()
            
#             # Получаем путь к исполняемым файлам
#             exe_files = []
#             if os.path.exists("Extreme.exe"):
#                 exe_files.append(("Extreme.exe", os.path.abspath("Extreme.exe")))
#             if os.path.exists("Updater.exe"):
#                 exe_files.append(("Updater.exe", os.path.abspath("Updater.exe")))
#             if os.path.exists("Utils/busybox.exe"):
#                 exe_files.append(("busybox.exe", os.path.abspath("Utils/busybox.exe")))
            
#             blocked_count = 0
#             for exe_name, exe_path in exe_files:
#                 # Создаем правило блокировки для исходящих подключений
#                 rule_name = f"Block_{exe_name}_Outbound"
#                 result = subprocess.run(
#                     [
#                         "netsh", "advfirewall", "firewall", "add", "rule",
#                         f"name={rule_name}",
#                         f"dir=out",
#                         "action=block",
#                         f"program={exe_path}",
#                         "enable=yes"
#                     ],
#                     capture_output=True,
#                     text=True,
#                     shell=True
#                 )
#                 if result.returncode == 0:
#                     blocked_count += 1
#                 else:
#                     # Если правило уже существует, обновляем его
#                     subprocess.run(
#                         [
#                             "netsh", "advfirewall", "firewall", "set", "rule",
#                             f"name={rule_name}",
#                             "new", "enable=yes", "action=block"
#                         ],
#                         capture_output=True,
#                         text=True,
#                         shell=True
#                     )
#                     blocked_count += 1
            
#             if blocked_count > 0:
#                 messagebox.showinfo("Успех", f"Доступ в интернет заблокирован для {blocked_count} файл(ов)")
#             else:
#                 messagebox.showwarning("Предупреждение", "Не найдено файлов для блокировки")
#         except Exception as e:
#             messagebox.showerror("Ошибка", f"Ошибка при блокировке доступа: {str(e)}")

#     # Функция для разрешения доступа в интернет
#     def allow_internet_access():
#         try:
#             # Получаем путь к исполняемым файлам
#             exe_files = []
#             if os.path.exists("Extreme.exe"):
#                 exe_files.append(("Extreme.exe", os.path.abspath("Extreme.exe")))
#             if os.path.exists("Updater.exe"):
#                 exe_files.append(("Updater.exe", os.path.abspath("Updater.exe")))
#             if os.path.exists("Utils/busybox.exe"):
#                 exe_files.append(("busybox.exe", os.path.abspath("Utils/busybox.exe")))
            
#             allowed_count = 0
#             for exe_name, exe_path in exe_files:
#                 # Создаем правило разрешения для исходящих подключений
#                 rule_name = f"Allow_{exe_name}_Outbound"
#                 result = subprocess.run(
#                     [
#                         "netsh", "advfirewall", "firewall", "add", "rule",
#                         f"name={rule_name}",
#                         f"dir=out",
#                         "action=allow",
#                         f"program={exe_path}",
#                         "enable=yes"
#                     ],
#                     capture_output=True,
#                     text=True,
#                     shell=True
#                 )
#                 if result.returncode == 0:
#                     allowed_count += 1
#                 else:
#                     # Если правило уже существует, обновляем его
#                     subprocess.run(
#                         [
#                             "netsh", "advfirewall", "firewall", "set", "rule",
#                             f"name={rule_name}",
#                             "new", "enable=yes", "action=allow"
#                         ],
#                         capture_output=True,
#                         text=True,
#                         shell=True
#                     )
#                     allowed_count += 1
                
#                 # Удаляем правило блокировки, если оно существует
#                 block_rule_name = f"Block_{exe_name}_Outbound"
#                 subprocess.run(
#                     [
#                         "netsh", "advfirewall", "firewall", "delete", "rule",
#                         f"name={block_rule_name}"
#                     ],
#                     capture_output=True,
#                     text=True,
#                     shell=True
#                 )
            
#             if allowed_count > 0:
#                 messagebox.showinfo("Успех", f"Доступ в интернет разрешен для {allowed_count} файл(ов)")
#             else:
#                 messagebox.showwarning("Предупреждение", "Не найдено файлов для разрешения")
#         except Exception as e:
#             messagebox.showerror("Ошибка", f"Ошибка при разрешении доступа: {str(e)}")

#     # Кнопки управления firewall
#     firewall_buttons_frame = ttk.Frame(firewall_section)
#     firewall_buttons_frame.pack(fill="x", pady=(0, 10))

#     ttk.Button(
#         firewall_buttons_frame,
#         text="🔒 Заблокировать доступ в интернет",
#         bootstyle="danger-outline",
#         command=block_internet_access,
#     ).pack(side="left", padx=(0, 10))

#     ttk.Button(
#         firewall_buttons_frame,
#         text="✅ Разрешить доступ в интернет",
#         bootstyle="success-outline",
#         command=allow_internet_access,
#     ).pack(side="left", padx=(0, 10))

#     ttk.Button(
#         firewall_buttons_frame,
#         text="⚙️ Включить Windows Firewall",
#         bootstyle="warning-outline",
#         command=enable_firewall,
#     ).pack(side="left")

#     # Секция обратной связи
#     feedback_section = ttk.Labelframe(left_column, text="Обратная связь", padding=15)
#     feedback_section.pack(fill="x", expand=False, pady=(15, 0))

#     # Заголовок
#     ttk.Label(
#         feedback_section,
#         text="Отправить сообщение разработчику",
#         font=("Segoe UI", 14, "bold"),
#     ).pack(anchor="w", pady=(0, 5))

#     # Описание
#     ttk.Label(
#         feedback_section,
#         text="Вы можете отправить сообщение разработчику с предложениями по улучшению программы или сообщением об ошибках.",
#         font=("Segoe UI", 10),
#         wraplength=500,
#         justify="left",
#     ).pack(anchor="w", pady=(0, 10))

#     # Создаем текстовое поле для сообщения
#     message_text = tk.Text(feedback_section, height=5, width=50, font=("Segoe UI", 10))
#     message_text.pack(fill="x", pady=(0, 10))

#     # Создаем фрейм для кнопок загрузки файлов
#     file_buttons_frame = ttk.Frame(feedback_section)
#     file_buttons_frame.pack(fill="x", pady=(0, 10))

#     # Глобальные переменные для хранения путей к файлам
#     global attached_file, attached_image
#     attached_file = None
#     attached_image = None

#     # Функция для загрузки файла
#     def attach_file():
#         global attached_file
#         file_path = filedialog.askopenfilename(
#             title="Выберите файл", filetypes=[("Все файлы", "*.*")]
#         )
#         if file_path:
#             attached_file = file_path
#             print(f"Файл прикреплен: {os.path.basename(file_path)}")

#     # Функция для загрузки изображения
#     def attach_image():
#         global attached_image
#         image_path = filedialog.askopenfilename(
#             title="Выберите изображение",
#             filetypes=[("Изображения", "*.png *.jpg *.jpeg *.bmp *.gif")],
#         )
#         if image_path:
#             attached_image = image_path
#             print(f"Изображение прикреплено: {os.path.basename(image_path)}")

#     # Кнопка для загрузки файла
#     ttk.Button(
#         file_buttons_frame,
#         text="Прикрепить файл",
#         bootstyle="info-outline",
#         command=attach_file,
#     ).pack(side="left", padx=5)

#     # Кнопка для загрузки изображения
#     ttk.Button(
#         file_buttons_frame,
#         text="Прикрепить изображение",
#         bootstyle="info-outline",
#         command=attach_image,
#     ).pack(side="left", padx=5)

#     # Функция для отправки сообщения
#     def send_feedback():
#         global attached_file, attached_image
#         message = message_text.get("1.0", "end-1c").strip()
#         if not message and not attached_file and not attached_image:
#             print("Предупреждение: Пожалуйста, введите сообщение или прикрепите файл")
#             return

#         try:
#             from telemetry.telemetry_manager import TelemetryManager

#             manager = TelemetryManager()

#             # Логируем начало отправки обратной связи
#             logger.logger.info("Отправка обратной связи...")

#             # Отправляем сообщение с префиксом "Обратная связь от пользователя:"
#             # автоматически собираем информацию о пользователе
#             try:
#                 windows_username = os.getenv('USERNAME', 'unknown')
#             except Exception:
#                 windows_username = 'unknown'
            
#             user_info = (
#                 f"👤 Пользователь: #{windows_username}\n"
#             )
#             user_info += (
#                 f"💻 Версия Extreme: {version}\n"
#                 f"🐍 Python версия: {sys.version}\n"
#             )

#             # объединяем информацию с сообщением от пользователя
#             full_message = f"Обратная связь от пользователя:\n{message}\n\n{user_info}"

#             # отправляем сообщение
#             if manager.send_message(full_message):
#                 logger.logger.info("Сообщение обратной связи успешно отправлено")
#                 print("Сообщение успешно отправлено!")

#                 # Отправляем файл, если он прикреплен
#                 if attached_file:
#                     if manager.send_telegram(attached_file):
#                         logger.logger.info(
#                             f"Файл {os.path.basename(attached_file)} успешно отправлен"
#                         )
#                         print("Файл успешно отправлен!")
#                     else:
#                         logger.logger.error(
#                             f"Ошибка отправки файла {os.path.basename(attached_file)}"
#                         )
#                         print("Ошибка: Не удалось отправить файл")

#                 # Отправляем изображение, если оно прикреплено
#                 if attached_image:
#                     if manager.send_telegram(attached_image):
#                         logger.logger.info(
#                             f"Изображение {os.path.basename(attached_image)} успешно отправлено"
#                         )
#                         print("Изображение успешно отправлено!")
#                     else:
#                         logger.logger.error(
#                             f"Ошибка отправки изображения {os.path.basename(attached_image)}"
#                         )
#                         print("Ошибка: Не удалось отправить изображение")

#                 # Очищаем форму
#                 message_text.delete("1.0", "end")
#                 attached_file = None
#                 attached_image = None
#             else:
#                 logger.logger.error("Ошибка отправки сообщения обратной связи")
#                 print("Ошибка: Не удалось отправить сообщение")
#         except Exception as e:
#             logger.logger.error(f"Ошибка при отправке обратной связи: {str(e)}")
#             print(f"Ошибка: Произошла ошибка при отправке: {str(e)}")

#     # Кнопка отправки доната
#     ttk.Button(
#         file_buttons_frame,
#         text="Отправить донат",
#         bootstyle="warning-outline",
#         command=open_donat,
#     ).pack(side="left", padx=5)

#     # Кнопка отправки сообщения
#     ttk.Button(
#         file_buttons_frame,
#         text="Отправить сообщение",
#         bootstyle="success-outline",
#         command=send_feedback,
#     ).pack(side="left", padx=5)

#     # Кнопка для выбора сборки Windows
#     ttk.Button(
#         file_buttons_frame,
#         text="Проголовать",
#         bootstyle="success-outline",
#         command=lambda: WindowsVoteWindow(root),
#     ).pack(side="left", padx=5)


# # Функция для открытия окна настроек колонок
# def open_columns_settings_window():
#     # Создаем новое окно
#     columns_window = ttk.Toplevel()
#     columns_window.title("Настройка количества колонок")
#     columns_window.geometry("600x600")

#     # Создаем контейнер с отступами
#     columns_container = ttk.Frame(columns_window, padding=20)
#     columns_container.pack(fill="both", expand=True)

#     # Заголовок
#     ttk.Label(
#         columns_container,
#         text="Настройка количества колонок",
#         font=("Segoe UI", 14, "bold"),
#     ).pack(anchor="w", pady=(0, 5))

#     # Описание
#     ttk.Label(
#         columns_container,
#         text="Настройте количество колонок для каждой вкладки",
#         font=("Segoe UI", 10),
#     ).pack(anchor="w", pady=(0, 15))

#     # Фрейм для добавления новых колонок
#     add_column_frame = ttk.Labelframe(
#         columns_container, text="Добавить новую вкладку", padding=10
#     )
#     add_column_frame.pack(fill="x", pady=(0, 15))

#     # Поля для ввода новой колонки
#     ttk.Label(add_column_frame, text="Название вкладки:").pack(side="left", padx=5)
#     new_col_name = ttk.Entry(add_column_frame, width=20)
#     new_col_name.pack(side="left", padx=5)

#     ttk.Label(add_column_frame, text="Кол-во колонок:").pack(side="left", padx=5)
#     new_col_count = ttk.Spinbox(add_column_frame, from_=1, to=6, width=3)
#     new_col_count.set(config.get("Columns", "default", fallback=3))
#     new_col_count.pack(side="left", padx=5)

#     # Создаем Treeview для отображения настроек
#     table_container = ttk.Frame(columns_container)
#     table_container.pack(fill="both", expand=True)

#     columns = ("Вкладка", "Колонок")
#     tree = ttk.Treeview(
#         table_container,
#         columns=columns,
#         show="headings",
#         selectmode="browse",
#         height=10,
#     )

#     # Настраиваем колонки
#     tree.heading("Вкладка", text="Вкладка", anchor="w")
#     tree.heading("Колонок", text="Колонок", anchor="center")
#     tree.column("Вкладка", width=250, anchor="w")
#     tree.column("Колонок", width=100, anchor="center")

#     # Добавляем скроллбар
#     scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=tree.yview)
#     tree.configure(yscrollcommand=scrollbar.set)

#     # Упаковываем элементы
#     tree.pack(side="left", fill="both", expand=True)
#     scrollbar.pack(side="right", fill="y")

#     # Заполняем таблицу данными
#     for section in config["Columns"]:
#         tree.insert("", "end", values=(str(section), config["Columns"][section]))

#     def add_new_column():
#         name = new_col_name.get().strip()
#         cols = new_col_count.get()

#         if not name:
#             tk.messagebox.showerror("Ошибка", "Введите название вкладки")
#             return

#         if name in config["Columns"]:
#             tk.messagebox.showerror("Ошибка", "Вкладка с таким именем уже существует")
#             return

#         try:
#             cols = int(cols)
#             if not 1 <= cols <= 6:
#                 raise ValueError
#         except ValueError:
#             tk.messagebox.showerror("Ошибка", "Введите число от 1 до 6")
#             return

#         # Добавляем в конфиг и таблицу
#         config["Columns"][name] = str(cols)
#         tree.insert("", "end", values=(name, cols))

#         # Очищаем поля ввода
#         new_col_name.delete(0, "end")
#         new_col_count.set(3)

#         # Сохраняем изменения
#         with open("user_data//settings.ini", "w", encoding="cp1251") as configfile:
#             config.write(configfile)

#     ttk.Button(
#         add_column_frame,
#         text="Добавить",
#         command=add_new_column,
#         bootstyle="success-outline",
#     ).pack(side="left", padx=5)

#     # Фрейм для управления
#     control_frame = ttk.Frame(columns_container)
#     control_frame.pack(fill="x", pady=(10, 0))

#     # Элементы управления
#     ttk.Label(control_frame, text="Кол-во колонок:").pack(side="left", padx=5)
#     spinbox = ttk.Spinbox(control_frame, from_=1, to=6, width=5)
#     spinbox.pack(side="left", padx=5)

#     def update_selected():
#         selected = tree.selection()
#         if selected:
#             new_value = spinbox.get()
#             item = tree.item(selected[0])
#             tab_name = str(item["values"][0])

#             # Обновляем конфиг и дерево
#             config["Columns"][tab_name] = new_value
#             tree.item(selected[0], values=(tab_name, new_value))

#             # Сохраняем изменения
#             with open("user_data//settings.ini", "w", encoding="cp1251") as configfile:
#                 config.write(configfile)

#     def reset_to_default():
#         # Значения по умолчанию для колонок
#         default_columns = {
#             "default": 3,
#         }

#         # Обновляем конфиг и очищаем дерево
#         config["Columns"] = default_columns
#         tree.delete(*tree.get_children())

#         # Заполняем таблицу заново
#         for section in config["Columns"]:
#             tree.insert("", "end", values=(str(section), config["Columns"][section]))

#         # Сохраняем изменения
#         with open("user_data//settings.ini", "w", encoding="cp1251") as configfile:
#             config.write(configfile)

#     # Добавляем кнопки
#     ttk.Button(
#         control_frame,
#         text="Сбросить",
#         command=reset_to_default,
#         bootstyle="danger-outline",
#     ).pack(side="left", padx=5)

#     ttk.Button(
#         control_frame,
#         text="Применить",
#         command=update_selected,
#         bootstyle="success-outline",
#     ).pack(side="left", padx=5)

#     # Кнопка закрытия
#     ttk.Button(
#         control_frame,
#         text="Закрыть",
#         command=columns_window.destroy,
#         bootstyle="info-outline",
#     ).pack(side="left", padx=5)


def switch_to_gpt():
    pass
    # """Переключает на вкладку Антон AI"""
    # # Удаляем все существующие вкладки
    # for tab in tab_control.tabs():
    #     tab_control.forget(tab)

    # # Создаем новую вкладку для чата
    # gpt_tab = ttk.Frame(tab_control)
    # tab_control.add(gpt_tab, text="Антон AI")

#     # Создаем новую вкладку для сохраненных файлов
#     saved_code_tab = ttk.Frame(tab_control)
#     tab_control.add(saved_code_tab, text="Сохраненные файлы")

#     # Создаем основной контейнер для чата
#     main_container = ttk.Frame(gpt_tab)
#     main_container.pack(fill="both", expand=True, padx=10, pady=10)

#     # Создаем текстовое поле для вывода сообщений
#     chat_display = tk.Text(
#         main_container, wrap=tk.WORD, height=20, font=("Segoe UI", 10)
#     )
#     chat_display.pack(fill="both", expand=True, pady=(0, 10))

#     # Добавляем скроллбар
#     scrollbar = ttk.Scrollbar(chat_display, command=chat_display.yview)
#     scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
#     chat_display.config(yscrollcommand=scrollbar.set)

#     # Создаем фрейм для ввода
#     input_frame = ttk.Frame(main_container)
#     input_frame.pack(fill="x")

#     # Создаем поле ввода
#     input_field = ttk.Entry(input_frame, font=("Segoe UI", 10))
#     input_field.pack(side="left", fill="x", expand=True, padx=(0, 5))

#     # Создаем кнопку отправки
#     send_button = ttk.Button(input_frame, text="Отправить", bootstyle="success-outline")
#     send_button.pack(side="right")

#     # Создаем контейнер для сохраненных файлов
#     saved_code_container = ttk.Frame(saved_code_tab)
#     saved_code_container.pack(fill="both", expand=True, padx=10, pady=10)

#     # Создаем список файлов
#     file_listbox = tk.Listbox(saved_code_container, font=("Segoe UI", 10))
#     file_listbox.pack(side="left", fill="both", expand=True)

#     # Добавляем скроллбар для списка файлов
#     file_scrollbar = ttk.Scrollbar(saved_code_container, command=file_listbox.yview)
#     file_scrollbar.pack(side="right", fill="y")
#     file_listbox.config(yscrollcommand=file_scrollbar.set)

#     # Создаем текстовое поле для просмотра содержимого файла
#     file_content = tk.Text(saved_code_container, wrap=tk.WORD, font=("Segoe UI", 10))
#     file_content.pack(fill="both", expand=True, pady=(10, 0))

#     def update_file_list():
#         """Обновляет список сохраненных файлов"""
#         file_listbox.delete(0, tk.END)
#         code_dir = Path("user_data/saved_code")
#         if code_dir.exists():
#             for file in sorted(code_dir.glob("*.bat"), reverse=True):
#                 file_listbox.insert(tk.END, file.name)

#     def show_file_content(event):
#         """Показывает содержимое выбранного файла"""
#         selection = file_listbox.curselection()
#         if selection:
#             filename = file_listbox.get(selection[0])
#             file_path = Path("user_data/saved_code") / filename
#             try:
#                 with open(file_path, "r", encoding="utf-8") as f:
#                     content = f.read()
#                 file_content.delete("1.0", tk.END)
#                 file_content.insert("1.0", content)
#             except Exception as e:
#                 file_content.delete("1.0", tk.END)
#                 file_content.insert("1.0", f"Ошибка чтения файла: {str(e)}")

#     # Привязываем обработчик выбора файла
#     file_listbox.bind("<<ListboxSelect>>", show_file_content)

#     # Обновляем список файлов при открытии вкладки
#     update_file_list()

#     # Инициализируем GPT клиент
#     gpt_client = GPTClient()

#     # Устанавливаем системный промпт
#     gpt_client.system_prompt = """Ты - профессиональный программист на языке Python и Assembly, 
#     ты хорошо разбираешься и в других языках программирования, а также отлично понимаешь как работает компьютер, 
#     еще ты профессиональный геймер, и хорошо разбираешься в компьютерных играх. 
#     Ты очень хорошо разбираешься в оптимизации Windows, знаешь весь Windows реестр наизусть.
#     Ты всегда отвечаешь на русском языке.
#     Ты всегда помогаешь пользователю с его задачами.
#     Ты всегда даешь подробные и понятные объяснения.
#     Ты всегда предлагаешь несколько вариантов решения проблемы.
#     Ты всегда проверяешь код на ошибки перед отправкой.
#     Ты всегда используешь современные практики программирования.
#     Ты всегда следуешь принципам безопасности при работе с системой."""

#     # Загружаем историю чата из файла
#     memory_file = Path("user_data/chat_memory.json")
#     if memory_file.exists():
#         try:
#             with open(memory_file, "r", encoding="utf-8") as f:
#                 gpt_client.memory = json.load(f)
#                 # Восстанавливаем историю в чате
#                 for msg in gpt_client.memory:
#                     role = msg["role"]
#                     content = msg["content"]
#                     if role == "user":
#                         chat_display.insert(tk.END, f"Вы: {content}\n", "user")
#                     elif role == "assistant":
#                         chat_display.insert(tk.END, f"GPT: {content}\n\n", "gpt")
#         except Exception as e:
#             chat_display.insert(
#                 tk.END, f"Ошибка загрузки истории: {str(e)}\n\n", "error"
#             )

#     def save_memory():
#         """Сохраняет историю чата в файл"""
#         try:
#             memory_file.parent.mkdir(parents=True, exist_ok=True)
#             with open(memory_file, "w", encoding="utf-8") as f:
#                 json.dump(gpt_client.memory, f, ensure_ascii=False, indent=2)
#         except Exception as e:
#             chat_display.insert(
#                 tk.END, f"Ошибка сохранения истории: {str(e)}\n\n", "error"
#             )

#     def process_command(message):
#         """Обрабатывает специальные команды"""
#         if message.lower() == "exit":
#             save_memory()  # Сохраняем историю перед выходом
#             root.destroy()
#             return True

#         elif message.startswith("cmd "):
#             command = message[4:]
#             try:
#                 result = gpt_client.execute_command(command)
#                 chat_display.insert(
#                     tk.END, f"Выполнение команды: {command}\n", "system"
#                 )
#                 chat_display.insert(tk.END, f"Результат:\n{result}\n\n", "system")
#             except Exception as e:
#                 chat_display.insert(
#                     tk.END, f"Ошибка выполнения команды: {str(e)}\n\n", "error"
#                 )
#             return True

#         elif message.lower() == "save_code":
#             if hasattr(gpt_client, "last_code"):
#                 try:
#                     # Создаем директорию для сохранения кода
#                     code_dir = Path("user_data/saved_code")
#                     code_dir.mkdir(parents=True, exist_ok=True)

#                     # Генерируем имя файла с текущей датой и временем
#                     timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#                     filename = code_dir / f"code_{timestamp}.bat"

#                     # Удаляем первую строку из кода
#                     code_lines = gpt_client.last_code.split("\n")
#                     if len(code_lines) > 1:
#                         code_without_first_line = "\n".join(code_lines[1:])
#                     else:
#                         code_without_first_line = gpt_client.last_code

#                     # Сохраняем код
#                     with open(filename, "w", encoding="utf-8") as f:
#                         f.write(code_without_first_line)

#                     chat_display.insert(
#                         tk.END, f"Код сохранен в файл: {filename}\n\n", "system"
#                     )
#                     # Обновляем список файлов
#                     update_file_list()
#                 except Exception as e:
#                     chat_display.insert(
#                         tk.END, f"Ошибка сохранения кода: {str(e)}\n\n", "error"
#                     )
#             else:
#                 chat_display.insert(tk.END, "Нет кода для сохранения\n\n", "error")
#             return True

#         return False

#     def send_message(event=None):
#         """Отправляет сообщение и получает ответ"""
#         message = input_field.get().strip()
#         if not message:
#             return

#         # Очищаем поле ввода
#         input_field.delete(0, tk.END)

#         # Добавляем сообщение пользователя в чат
#         chat_display.insert(tk.END, f"Вы: {message}\n", "user")
#         chat_display.tag_configure("user", foreground="blue")

#         # Проверяем, является ли сообщение командой
#         if process_command(message):
#             chat_display.see(tk.END)
#             return

#         # Получаем ответ от GPT
#         try:
#             response = gpt_client.get_response(message)
#             chat_display.insert(tk.END, f"GPT: {response}\n\n", "gpt")
#             chat_display.tag_configure("gpt", foreground="green")

#             # Если в ответе есть код, предлагаем сохранить
#             # if "```bat" in response:
#             if "```" in response:
#                 code_blocks = response.split("```")
#                 for i in range(1, len(code_blocks), 2):
#                     code = code_blocks[i].strip()
#                     if code:
#                         gpt_client.last_code = code
#                         chat_display.insert(
#                             tk.END,
#                             "В ответе обнаружен код. Используйте команду 'save_code' для его сохранения.\n",
#                             "system",
#                         )
#                         break

#             # Сохраняем историю после каждого сообщения
#             save_memory()

#         except Exception as e:
#             chat_display.insert(tk.END, f"Ошибка: {str(e)}\n\n", "error")
#             chat_display.tag_configure("error", foreground="red")

#         # Прокручиваем чат вниз
#         chat_display.see(tk.END)

#     # Привязываем отправку к кнопке и Enter
#     send_button.config(command=send_message)
#     input_field.bind("<Return>", send_message)

#     # Фокусируемся на поле ввода
#     input_field.focus()

#     # Добавляем приветственное сообщение
#     chat_display.insert(tk.END, "Добро пожаловать в Антон AI от Extreme Tweaker!\n\n", "system")
#     chat_display.tag_configure("system", foreground="gray")

#     # Добавляем информацию о командах
#     commands_info = """Доступные команды:
# - exit - выход из программы
# - cmd <команда> - выполнить команду в cmd
# - save_code - сохранить последний код

# Начните диалог, введя сообщение ниже.\n\n"""
#     chat_display.insert(tk.END, commands_info, "system")

#     # Сохраняем историю при закрытии окна
#     def on_closing():
#         save_memory()
#         root.destroy()

#     root.protocol("WM_DELETE_WINDOW", on_closing)

# Определяем функции-обертки перед списком quick_buttons
def switch_to_main_wrapper():
    confirm_switch_tab(switch_to_main)
def switch_to_game_mode_wrapper():
    confirm_switch_tab(switch_to_game_mode)
def switch_to_drivers_wrapper():
    # Проверяем, нужно ли показывать предупреждение
    if config.getboolean("General", "drivers_warning_enabled", fallback=True):
        warning_dialog = tk.Toplevel(root)
        warning_dialog.title("⚠️ КРИТИЧЕСКОЕ ПРЕДУПРЕЖДЕНИЕ")
        warning_dialog.geometry("600x500")
        warning_dialog.transient(root)
        warning_dialog.grab_set()
        
        # Центрируем окно
        warning_dialog.update_idletasks()
        width = warning_dialog.winfo_width()
        height = warning_dialog.winfo_height()
        x = (warning_dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (warning_dialog.winfo_screenheight() // 2) - (height // 2)
        warning_dialog.geometry("{}x{}+{}+{}".format(width, height, x, y))
        
        # Добавляем сообщение
        warning_text = """⚠️ ВНИМАНИЕ! ⚠️

Вкладка Драйверы содержит ОПАСНЫЕ твики, которые могут:
• Убить Windows
• Повредить систему
• Сделать компьютер неработоспособным
• СЛОМАТЬ материнскую плату
• СЛОМАТЬ видеокарту
• СЛОМАТЬ процессор

Используйте эти твики ТОЛЬКО если вы:
• Понимаете что делаете
• Имеете бэкап системы
• Готовы к переустановке Windows
• Готовы к замене оборудования

Вы уверены, что хотите продолжить?"""
        
        message = ttk.Label(
            warning_dialog,
            text=warning_text,
            font=("Segoe UI", 11),
            justify="center",
            wraplength=550
        )
        message.pack(pady=20, padx=20)
        
        # Фрейм для чекбокса
        checkbox_frame = ttk.Frame(warning_dialog)
        checkbox_frame.pack(pady=10)
        
        dont_show_again_var = tk.BooleanVar()
        dont_show_checkbox = ttk.Checkbutton(
            checkbox_frame,
            text="Больше не показывать это предупреждение",
            variable=dont_show_again_var
        )
        dont_show_checkbox.pack()
        
        # Фрейм для кнопок
        button_frame = ttk.Frame(warning_dialog)
        button_frame.pack(pady=10)
        
        def on_confirm():
            if dont_show_again_var.get():
                config["General"]["drivers_warning_enabled"] = "False"
                with open("user_data//settings.ini", "w", encoding="cp1251") as configfile:
                    config.write(configfile)
            warning_dialog.destroy()
            confirm_switch_tab(switch_to_drivers)
        
        def on_cancel():
            warning_dialog.destroy()
        
        # Кнопки
        confirm_button = ttk.Button(
            button_frame,
            text="Продолжить (на свой риск)",
            command=on_confirm,
            bootstyle="danger-outline",
        )
        confirm_button.pack(side="left", padx=5)
        
        cancel_button = ttk.Button(
            button_frame, text="Отмена", command=on_cancel, bootstyle="success-outline"
        )
        cancel_button.pack(side="left", padx=5)
        
        # Устанавливаем фокус на кнопку отмены
        cancel_button.focus_set()
        
        # Ждем, пока окно будет закрыто
        warning_dialog.wait_window()
    else:
        confirm_switch_tab(switch_to_drivers)
def switch_to_optimization_wrapper():
    confirm_switch_tab(switch_to_optimization)
def switch_to_power_wrapper():
    confirm_switch_tab(switch_to_power)
def switch_to_fixes_wrapper():
    confirm_switch_tab(switch_to_fixes)
def switch_to_clean_wrapper():
    confirm_switch_tab(switch_to_clean)
def switch_to_other_wrapper():
    confirm_switch_tab(switch_to_other)
def switch_to_settings_wrapper():
    confirm_switch_tab(switch_to_settings)
# def switch_to_telemetry_wrapper():
#     # Переключаемся на настройки и выбираем вкладку "Телеметрия"
#     confirm_switch_tab(switch_to_settings)
#     # После переключения выбираем вкладку "Телеметрия"
#     if tab_control.tabs():
#         for i, tab in enumerate(tab_control.tabs()):
#             if tab_control.tab(tab, "text") == "Телеметрия":
#                 tab_control.select(i)
#                 break
# Функции switch_to_system_wrapper и switch_to_about_wrapper удалены для упрощения твикера
# def switch_to_gpt_wrapper():
#     confirm_switch_tab(switch_to_gpt)
# def switch_to_minimal_wrapper():
#     # Для минимальной вкладки не используем confirm_switch_tab, так как она скрывает интерфейс
#     switch_to_minimal()

# Переносим список быстрых кнопок ПОСЛЕ объявления всех функций
# Функция для создания списка кнопок с учетом режима разработчика
def get_quick_buttons_list():
    developer_mode = config.getboolean("General", "developer_mode", fallback=False)
    base_buttons = [
        ("Главная", switch_to_main_wrapper, "🏠"),
        ("Оптимизация", switch_to_optimization_wrapper, "⚡"),
        ("Очистка", switch_to_clean_wrapper, "☠️"),
        ("Настройки", switch_to_settings_wrapper, "⚙️"),
        # ("Игровой режим", switch_to_game_mode_wrapper, "🚀"),
        ("Исправления", switch_to_fixes_wrapper, "⚜️"),
        ("Создать конфиг", lambda: create_batch_file([name for name, var in checkboxes.items() if var.get()]),"📝",),
    ]
    if developer_mode:
        # Вставляем кнопки разработчика в нужные места
        base_buttons.insert(2, ("Драйверы", switch_to_drivers_wrapper, "🎮"))
        base_buttons.insert(3, ("Электропитание", switch_to_power_wrapper, "🔋"))
    return base_buttons

# Создаем варианты кнопок с разными иконками
base_buttons_list = get_quick_buttons_list()
icon_variants = {
    "Главная": ["⭐", "🏠", "🚀"],
    # "Оптимизация": ["⚡", "💪", "⚡"],
    "Оптимизация": ["⚡", "⚡"],
    "Драйверы": ["🎮", "🎮", "🎮"],
    # "Электропитание": ["🔋", "⚡", "🔋"],
    "Электропитание": ["🔋", "🔋"],
    # "Очистка": ["☠️", "🧹", "🧸"],
    "Очистка": ["🧹"],
    # "Настройки": ["⚙️", "⚙️", "⚙️"],
    # "Исправления": ["⚜️", "🔧", "🧷"],
    "Исправления": ["⚜️"],
    "Игровой режим": ["🏆", "🏆", "🏆"],
    # "Антон AI": ["👻", "👽", "👾"],
    "Создать конфиг": ["📝", "📝", "📝"],
}

quick_buttons1 = []
quick_buttons2 = []
quick_buttons3 = []

for text, cmd, icon in base_buttons_list:
    if text in icon_variants:
        icons = icon_variants[text]
        quick_buttons1.append((text, cmd, icons[0] if len(icons) > 0 else icon))
        quick_buttons2.append((text, cmd, icons[1] if len(icons) > 1 and icons[1] else icons[0] if len(icons) > 0 else icon))
        quick_buttons3.append((text, cmd, icons[2] if len(icons) > 2 else icons[0] if len(icons) > 0 else icon))
    else:
        quick_buttons1.append((text, cmd, icon))
        quick_buttons2.append((text, cmd, icon))
        quick_buttons3.append((text, cmd, icon))
alt_quick_buttons = [quick_buttons1, quick_buttons2, quick_buttons3]
quick_buttons = (random.choice(alt_quick_buttons))
# Альтернативные варианты иконок для каждого раздела:
icon_variants_for_quick_buttons = {
    "Главная": ["🏠", "🏡", "🎯", "⭐", "🌟", "✨", "💫", "🎪", "🎨", "🎭"],
    "Оптимизация": ["⚡", "🚀", "💨", "⚡️", "🔋", "💪", "🎯", "🎮", "🏃", "🏎️"],
    "Драйверы": ["🔧", "🛠️", "⚙️", "🔨", "📦", "📥", "📤", "🔄", "🔍", "🔎"],
    "Электропитание": ["🔋", "⚡", "💡", "🔌", "🔍", "📊", "📈", "📉", "🎯", "🎮"],
    "Другое": ["⚙️", "🔧", "🛠️", "🔨", "📦", "📥", "📤", "🔄", "🔍", "🔎"],
    "Очистка": ["🧹", "🧽", "🧼", "🧴", "🧸", "🧶", "🧵", "🧷", "🧹", "🧺", "☠️"],
    # "Настройки": ["⚙️", "🔧", "🛠️", "🔨", "📦", "📥", "📤", "🔄", "🔍", "🔎"],
    # "Телеметрия": ["📊", "👹", "☠️", "👺", "👻", "👽", "👾", "🚀", "⚡️", "🔋", "💪"],
    "Исправления": ["🔧", "🛠️", "⚙️", "🔨", "📦", "📥", "📤", "🔄", "🔍", "🔎"],
    "Обновления": ["🔄", "📥", "📤", "📦", "📨", "📩", "📪", "📫", "📬", "📭"],
    "Версия": ["📄", "📝", "📋", "📑", "🔖", "📚", "📖", "📕", "📗", "📘"],
    "Антон AI": ["🤖", "👾", "👽", "👻", "👹", "👺", "👻", "👽", "👾", "🤖"],
    "Создать конфиг": ["📝", "📄", "📋", "📑", "🔖", "📚", "📖", "📕", "📗", "📘"],
    "Выйти": ["🚪", "🚶", "🏃", "🚶‍♂️", "🏃‍♂️", "🚶‍♀️", "🏃‍♀️", "🚶", "🏃", "❌"],
}

# Создание контроллера вкладок с новым стилем
tab_style = ttk.Style()
tab_style.configure("Custom.TNotebook", padding=5)
tab_style.configure("Custom.TNotebook.Tab", padding=(10, 5))  # Шрифт будет установлен через update_font_style

# Настраиваем стили для чекбоксов и других элементов (без шрифтов, они будут установлены через update_font_style)
style = ttk.Style()
style.configure("Custom.TCheckbutton", padding=5)  # Шрифт будет установлен через update_font_style
style.configure("Custom.TButton", padding=5)  # Шрифт уже настроен выше, но будет обновлен через update_font_style
style.configure("Custom.TLabel", padding=5)  # Шрифт будет установлен через update_font_style
style.configure("Custom.TEntry", padding=5)

# Настраиваем стили для категорий
style.configure("Category.TFrame", background="#1a1a1a", relief="solid", borderwidth=1)
style.configure(
    "Category.TButton",
    padding=10,  # Шрифт будет установлен через update_font_style
    background="#1a1a1a",
    foreground="white",
    justify="center",
    wraplength=200,
)
style.configure("Category.TLabel", background="#1a1a1a", padding=10)  # Шрифт будет установлен через update_font_style

# Настраиваем стиль для иконок без текста
style.configure("Icon.TButton", font=get_icon_button_font(), padding=10, width=3)

# Глобальная переменная для хранения текущей ширины кнопок
button_width = 2

# функция для переключения ширины кнопок
def toggle_button_width():
    global button_width
    button_width = 20 if button_width == 2 else 2
    # Обновляем ширину всех кнопок
    for btn_frame in sidebar.winfo_children():
        for btn in btn_frame.winfo_children():
            if isinstance(btn, ttk.Button):
                if button_width == 2:
                    btn.configure(width=3, style="Icon.TButton")
                    btn.configure(
                        text=btn.cget("text").split(" ")[0]
                    )  # Оставляем только иконку
                else:
                    btn.configure(width=button_width)
                    # Восстанавливаем полный текст с иконкой
                    icon = btn.cget("text")
                    for text, _, icon_variant in quick_buttons:
                        if icon_variant == icon:
                            btn.configure(text=f"{icon} {text}")
                            break
                # Обновляем текст кнопки переключения
                if btn == width_toggle_btn:
                    btn.configure(
                        text="👁 Показать текст"
                        if button_width == 2
                        else "👀 Скрыть текст"
                    )

# Создаем кнопку переключения ширины
width_toggle_frame = ttk.Frame(sidebar)
width_toggle_frame.pack(fill="x", pady=2)
width_toggle_btn = ttk.Button(
    width_toggle_frame,
    text="👁 Показать текст",
    width=3,
    style="Icon.TButton",
    command=toggle_button_width,
)
width_toggle_btn.pack(padx=5)

# Создаем кнопки из списка
for text, command, icon in quick_buttons:
    btn_frame = ttk.Frame(sidebar)
    btn_frame.pack(fill="x", pady=2)

    btn = ttk.Button(
        btn_frame, text=icon, width=3, style="Icon.TButton", command=command
    )
    btn.pack(padx=5)

# Создание контроллера вкладок с новым стилем
tab_control = ttk.Notebook(content_container, style="Custom.TNotebook")
tab_control.pack(side="left", fill="both", expand=True)

"""
+------------------------------------+
| Функция для создания вкладки       |
| с таблицей электропитания          |
+------------------------------------+
"""


def create_power_tab():
    tab_frame = ttk.Frame(tab_control)
    tab_frame.configure(style="Custom.TFrame")

    # Контейнер для заголовка
    header_frame = ttk.Frame(tab_frame)
    header_frame.pack(fill="x", pady=10)

    # Заголовок таблицы с обновленным стилем
    title_label = ttk.Label(
        header_frame,
        text="Результаты тестирования планов электропитания",
        font=("Segoe UI", 12, "bold"),
    )
    title_label.pack(side="top", anchor="w", padx=10)

    # Создаем фрейм для таблицы и скроллбара
    table_frame = ttk.Frame(tab_frame)
    table_frame.pack(fill="both", expand=True, padx=10)

    all_wincry_themes = ["wincry", "wincry_warning", "ruslanchik", "extreme", "extra", "hone", "newhone", "light_hone"]

    # Обновляем стиль таблицы с учетом темы
    if current_theme in ["vapor", "cyberpunk"]:
        style.configure(
            "Treeview", font=("Segoe UI", 10), rowheight=28, background="#190831"
        )  # Темный фон для Vapor/Cyberpunk
    elif current_theme in ["darkly", "hacker"]:
        style.configure(
            "Treeview", font=("Segoe UI", 10), rowheight=28, background="#222222"
        )  # Темно-серый фон для Darkly и Hacker
    elif current_theme == "cyborg":
        style.configure(
            "Treeview", font=("Segoe UI", 10), rowheight=28, background="#060606"
        )  # Темно-серый фон для Cyborg
    else:
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=28)

    # Создание Treeview
    columns = (
        "plan",
        "avg_latency",
        "min_latency",
        "max_latency",
        "avg_fps",
        "temp",
        "comment",
    )
    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        style="Treeview",
        selectmode="browse",
    )

    # Настройка колонок
    col_widths = {
        "plan": 250,
        "avg_latency": 120,
        "min_latency": 120,
        "max_latency": 120,
        "avg_fps": 100,
        "temp": 100,
        "comment": 200,
    }

    for col in columns:
        tree.heading(col, text=col.capitalize())
        if col in ["plan", "comment"]:
            tree.column(col, width=col_widths[col], anchor="w")
        else:
            tree.column(col, width=col_widths[col], anchor="center")

    style.configure("Treeview.Heading", anchor="center")

    tree.heading("plan", text="План питания")
    tree.heading("avg_latency", text="Ср. задержка (мс)")
    tree.heading("min_latency", text="Мин. задержка")
    tree.heading("max_latency", text="Макс. задержка")
    tree.heading("avg_fps", text="Ср. FPS")
    tree.heading("temp", text="Темп. CPU")
    tree.heading("comment", text="Комментарий")

    data = [
        (
            "Bitsum Highest Performance",
            30.87,
            24.87,
            36.62,
            382.90,
            "76°C",
            "Рекомендуется для игр",
        ),
        (
            "Amit v1 lowlatency",
            30.72,
            24.76,
            36.97,
            383.90,
            "75°C",
            "Лучшая стабильность FPS",
        ),
        (
            "Amit v2 extreme performance",
            30.83,
            25.54,
            37.63,
            384.80,
            "74°C",
            "Экстремальная производительность",
        ),
        (
            "Amit v3 low latency",
            30.98,
            25.21,
            37.52,
            380.90,
            "73°C",
            "Оптимизация для 0.1% FPS",
        ),
        ("Atlas power plan", 31.09, 25.32, 38.09, 383.00, "73°C", "Универсальный план"),
        (
            "Calypto's Low Latency",
            31.17,
            25.21,
            37.63,
            385.10,
            "71°C",
            "Завышенные задержки дров",
        ),
        (
            "ggOS Desktop Gaming v085",
            31.14,
            24.86,
            36.52,
            381.40,
            "74°C",
            "Для настольных ПК",
        ),
        (
            "Little Unixcorn's PowerPlan",
            30.64,
            25.09,
            37.63,
            382.00,
            "78°C",
            "Экспериментальный план",
        ),
        (
            "Muren's Low Latency",
            30.81,
            24.75,
            36.74,
            382.10,
            "75°C",
            "Лучшая стабильность задержек",
        ),
        (
            "Zoyata Low latency",
            30.83,
            24.54,
            37.75,
            380.10,
            "74°C",
            "Сбалансированные настройки",
        ),
        (
            "Максимальная производительность",
            30.98,
            24.42,
            38.30,
            380.40,
            "73°C",
            "Стандартный план Windows",
        ),
        (
            "Высокая производительность",
            30.83,
            25.32,
            37.74,
            381.20,
            "73°C",
            "Просадки в 1% FPS",
        ),
        (
            "Сбалансированная",
            30.93,
            25.31,
            37.75,
            349.50,
            "65°C",
            "Для повседневных задач",
        ),
        (
            "Экономия энергии",
            33.35,
            27.11,
            40.88,
            266.50,
            "50°C",
            "Энергосберегающий режим",
        ),

        ("", "", "", "", "", "", "",),
        ("", "", "", "Сортировка по FPS (по убыванию)", "", "", "",),
        ("", "", "", "", "", "", "",),

        # Сортировка по FPS (по убыванию)
        ("AMD Ryzen Balanced", 31.20, 25.40, 37.80, 375.00, "72°C", "Официальный план AMD Ryzen"),
        ("AMD Ryzen High Performance", 30.90, 24.90, 37.20, 380.00, "74°C", "Официальный план AMD Ryzen"),
        ("1usmus Ryzen Universal", 30.85, 24.80, 37.00, 382.00, "75°C", "Оптимизированный для Ryzen"),
        ("Chrometastic's AMD Extreme", 30.75, 24.70, 36.90, 383.00, "76°C", "Экстремальная производительность"),
        ("Tom's AMD Power Plan", 31.00, 25.00, 37.50, 378.00, "73°C", "Оптимизированный для AMD"),
        ("Tom's Intel Power Plan", 31.10, 25.10, 37.60, 376.00, "72°C", "Оптимизированный для Intel"),
        ("ReviOS Ultra Performance", 30.80, 24.75, 36.85, 381.00, "75°C", "Максимальная производительность"),
        ("Hone Ultimate Power Plan", 30.95, 24.90, 37.10, 379.00, "74°C", "Универсальный план"),
        ("ET's Ultra Low Latency", 30.70, 24.65, 36.80, 382.00, "75°C", "Минимальные задержки"),
        ("Xhen's Power Plan", 31.05, 25.00, 37.40, 377.00, "73°C", "Сбалансированный план"),
        # ... остальные планы отсортированы по FPS ...
        ("Power saver", 31.40, 25.60, 38.20, 368.00, "69°C", "Энергосберегающий режим"),
        ("Power saver_1", 31.35, 25.55, 38.15, 369.00, "70°C", "Энергосберегающий режим"),
        ("Ryzen CPUs Optimized Power Saver", 31.40, 25.60, 38.20, 368.00, "69°C", "Энергосберегающий план"),
        ("Ryzen CPUs Balanced LowPower v8", 31.30, 25.50, 38.00, 370.00, "70°C", "Энергоэффективный план"),
        ("LegionQuiet", 31.30, 25.50, 38.00, 370.00, "70°C", "Тихий режим для ноутбуков"),
        ("Ahorro de energia", 31.40, 25.60, 38.20, 368.00, "69°C", "Энергосберегающий режим"),
        ("Equilibrado", 31.00, 25.00, 37.20, 378.00, "73°C", "Сбалансированный план"),
        ("Balanced_1", 31.00, 25.00, 37.20, 378.00, "73°C", "Альтернативный сбалансированный план"),
        ("Balance Win10 20H2", 30.95, 24.85, 37.05, 380.00, "74°C", "Оптимизированный для Windows 10 20H2"),
        ("Balance DisableBoost", 31.10, 25.10, 37.30, 376.00, "72°C", "Сбалансированный без буста"),
        ("Clixke IDLE Enabled", 31.00, 25.00, 37.20, 378.00, "73°C", "С поддержкой простоя"),
        ("Duck IDLE Enabled", 31.00, 25.00, 37.20, 378.00, "73°C", "С поддержкой простоя"),
        ("EonX Idle", 31.00, 25.00, 37.20, 378.00, "73°C", "С поддержкой простоя"),
        ("HT Idle Enabled", 31.00, 25.00, 37.20, 378.00, "73°C", "С поддержкой Hyper-Threading"),
        ("Ideal Powerplan", 31.00, 25.00, 37.20, 378.00, "73°C", "Идеальный план"),
        ("Main Power Plan", 31.00, 25.00, 37.20, 378.00, "73°C", "Основной план"),
        ("power", 31.00, 25.00, 37.20, 378.00, "73°C", "Универсальный план"),
        ("Windows 7 Calypto", 31.00, 25.00, 37.20, 378.00, "73°C", "План Calypto для Windows 7"),
        ("Tom Intel 1", 31.00, 25.00, 37.20, 378.00, "73°C", "Оптимизированный для Intel"),
        ("Ryzen_Balanced_plus", 31.00, 25.20, 37.60, 375.00, "72°C", "Улучшенный сбалансированный план"),
        ("LegionBalance", 31.10, 25.20, 37.60, 375.00, "72°C", "Сбалансированный для ноутбуков"),
        ("Laptop High Performance", 31.10, 25.20, 37.60, 375.00, "72°C", "Высокая производительность для ноутбуков"),
        ("slow_shift_L", 31.10, 25.20, 37.60, 375.00, "72°C", "Медленный сдвиг (L)"),
        ("CoreLimit 50% NoTurbo", 31.10, 25.30, 37.60, 374.00, "72°C", "Ограничение 50% без турбо"),
        ("CoreLimit 75%", 31.00, 25.20, 37.40, 376.00, "73°C", "Ограничение 75%"),
        ("slow_shift_P", 31.00, 25.00, 37.40, 377.00, "73°C", "Медленный сдвиг (P)"),
        ("CoreLimit 25%", 31.20, 25.40, 37.80, 372.00, "71°C", "Ограничение 25%"),
        ("CoreLimit 12%", 31.30, 25.50, 38.00, 370.00, "70°C", "Ограничение 12%"),
        ("Ryzen CPUs Balanced Snappy v1", 31.00, 25.20, 37.60, 378.00, "73°C", "Оптимизированный для отзывчивости"),
        ("AMD Ryzen Balanced Snappy", 31.00, 25.20, 37.60, 378.00, "73°C", "Оптимизированный для отзывчивости"),
        ("Intel Core Balanced Snappy", 31.10, 25.25, 37.65, 375.00, "72°C", "Оптимизированный для отзывчивости"),
        ("Intel Core Ultimate LowPower", 31.35, 25.55, 38.10, 369.00, "70°C", "Энергоэффективный план Intel"),
        ("Intel Core Balanced LowPower", 31.40, 25.60, 38.20, 368.00, "69°C", "Энергоэффективный план Intel"),
        ("AMD Ryzen Balanced LowPower", 31.30, 25.50, 38.00, 370.00, "70°C", "Энергоэффективный план для Ryzen"),
        ("Intel Core High Performance", 31.15, 25.30, 37.70, 376.00, "72°C", "Официальный план Intel"),
        ("Intel Core Ultimate HighPower", 30.95, 24.85, 37.10, 380.00, "74°C", "Максимальная производительность для Intel"),
        ("AMD Ryzen Ultimate HighPower", 30.85, 24.75, 36.95, 381.50, "75°C", "Максимальная производительность для Ryzen"),
        ("Ryzen CPUs Ultimate Performance v5", 30.85, 24.75, 36.95, 381.50, "75°C", "Максимальная производительность"),
        ("AMD Ryzen 3k.x Power Plan v3", 30.85, 24.75, 36.95, 381.50, "75°C", "Оптимизированный для Ryzen 3000"),
        ("With Boost by Tom", 30.85, 24.75, 36.95, 381.50, "75°C", "С бустом от Tom"),
        ("Win10GE", 30.85, 24.75, 36.95, 381.50, "75°C", "Оптимизированный для Windows 10"),
        ("Turbo Performance", 30.85, 24.75, 36.95, 381.50, "75°C", "С турбо режимом"),
        ("Revision Power Plan V2.705", 30.85, 24.75, 36.95, 381.50, "75°C", "Версия 2.705"),
        ("High Performance AMD", 30.85, 24.75, 36.95, 381.50, "75°C", "Оптимизированный для AMD"),
        ("Exm Premium Power Plan", 30.85, 24.75, 36.95, 381.50, "75°C", "Премиум план"),
        ("EagleOS", 30.85, 24.75, 36.95, 381.50, "75°C", "Максимальная производительность"),
        ("Clixke", 30.85, 24.75, 36.95, 381.50, "75°C", "Оптимизированный для игр"),
        ("Razer Cortex Power Plan", 30.85, 24.75, 36.95, 381.50, "75°C", "Оптимизированный для Razer"),
        ("n1kobg's GPU Booster", 30.85, 24.75, 36.95, 381.50, "75°C", "Оптимизированный для GPU"),
        ("KernelOS Performance v6 IDLE ON", 30.85, 24.75, 36.95, 381.50, "75°C", "С поддержкой простоя"),
        ("ggOS Desktop Gaming 0.8.13", 30.90, 24.80, 37.00, 381.00, "74°C", "Игровой план версии 0.8.13"),
        ("High Performance Default", 30.90, 24.80, 37.00, 381.00, "74°C", "Стандартный высокопроизводительный"),
        ("Intel with Boost", 30.90, 24.80, 37.00, 381.00, "74°C", "С бустом для Intel"),
        ("Windows 10 Muren", 30.90, 24.80, 37.00, 381.00, "74°C", "План Muren для Windows 10"),
        ("Unicorn Plan", 30.90, 24.80, 37.00, 381.00, "74°C", "Альтернативный план"),
        ("Tom's Power Plan", 30.90, 24.80, 37.00, 381.00, "74°C", "Универсальный план"),
        ("Revision Power Plan V2.8.1", 30.90, 24.80, 37.00, 381.00, "74°C", "Версия 2.8.1"),
        ("Reknotic", 30.90, 24.80, 37.00, 381.00, "74°C", "Оптимизированный для игр"),
        ("N1ko", 30.90, 24.80, 37.00, 381.00, "74°C", "Оптимизированный для игр"),
        ("Khorvie", 30.90, 24.80, 37.00, 381.00, "74°C", "Оптимизированный для игр"),
        ("Ian Crazy Win10", 30.90, 24.80, 37.00, 381.00, "74°C", "Экстремальный план для Windows 10"),
        ("HUNCHO", 30.90, 24.80, 37.00, 381.00, "74°C", "Оптимизированный для игр"),
        ("Gio AMD", 30.90, 24.80, 37.00, 381.00, "74°C", "Оптимизированный для AMD"),
        ("Fr33thy's Power Plan", 30.90, 24.80, 37.00, 381.00, "74°C", "Оптимизированный для игр"),
        ("Eternity", 30.90, 24.80, 37.00, 381.00, "74°C", "Оптимизированный для игр"),
        ("EVA Power Plan", 30.90, 24.80, 37.00, 381.00, "74°C", "Оптимизированный для игр"),
        ("ColbyEddie", 30.90, 24.80, 37.00, 381.00, "74°C", "Оптимизированный для игр"),
        ("Amir Crazy Win10", 30.90, 24.80, 37.00, 381.00, "74°C", "Экстремальный план для Windows 10"),
        ("Alto rendimiento", 30.80, 24.70, 36.90, 382.00, "75°C", "Максимальная производительность"),
        ("CoreLimit 100% NoTurbo", 30.80, 24.70, 36.90, 382.00, "75°C", "Максимальная загрузка без турбо"),
        ("HyperTweaks No Idle", 30.80, 24.70, 36.90, 382.00, "75°C", "Без простоя"),
        ("Igromanoff v3", 30.80, 24.70, 36.90, 382.00, "75°C", "Последняя версия"),
        ("max perfomance", 30.80, 24.70, 36.90, 382.00, "75°C", "Максимальная производительность"),
        ("PowerX v3", 30.80, 24.70, 36.90, 382.00, "75°C", "Последняя версия"),
        ("Rendimiento maximo", 30.80, 24.70, 36.90, 382.00, "75°C", "Максимальная производительность"),
        ("Revision Extreme Performance", 30.80, 24.70, 36.90, 382.00, "75°C", "Экстремальная производительность"),
        ("Rock Power Plan", 30.80, 24.70, 36.90, 382.00, "75°C", "Максимальная производительность"),
        ("TJxTweaks", 30.80, 24.70, 36.90, 382.00, "75°C", "Оптимизированный для игр"),
        ("Ultimate Performance", 30.80, 24.70, 36.90, 382.00, "75°C", "Максимальная производительность"),
        ("Valorant", 30.80, 24.70, 36.90, 382.00, "75°C", "Оптимизированный для Valorant"),
        ("JamessJ Plan de energia IDLE OFF", 30.80, 24.70, 36.90, 382.00, "75°C", "Без простоя"),
        ("TYT_power_plan_idle_off_gaming_V3", 30.80, 24.70, 36.90, 382.00, "75°C", "Игровой режим без простоя"),
        ("F1rst v1.1", 30.80, 24.70, 36.90, 382.00, "75°C", "Максимальная производительность"),
        ("Pablerso High Performance", 30.80, 24.70, 36.90, 382.00, "75°C", "Максимальная производительность"),
        ("Baotweaks Highest Performance", 30.80, 24.70, 36.90, 382.00, "75°C", "Максимальная производительность"),
        ("CoreLimit-100per", 30.80, 24.70, 36.90, 382.00, "75°C", "Максимальная загрузка CPU"),
        ("CoreLimit 100% NoBoost", 30.75, 24.65, 36.85, 382.50, "75°C", "Максимальная загрузка без буста"),
        ("CPU-MaxPower", 30.75, 24.65, 36.85, 382.50, "75°C", "Максимальная мощность CPU"),
        ("Gaming Power", 30.75, 24.65, 36.85, 382.50, "75°C", "Оптимизированный для игр"),
        ("HeuZ Low Latency", 30.75, 24.65, 36.85, 382.50, "75°C", "Минимальные задержки"),
        ("Hydro No Idle", 30.75, 24.65, 36.85, 382.50, "75°C", "Минимальные задержки"),
        ("Hydro's Low Latency", 30.75, 24.65, 36.85, 382.50, "75°C", "Минимальные задержки"),
        ("Kapsel Low Latency", 30.75, 24.65, 36.85, 382.50, "75°C", "Минимальные задержки"),
        ("low-latency", 30.75, 24.65, 36.85, 382.50, "75°C", "Минимальные задержки"),
        ("MaxPowerPlan", 30.75, 24.65, 36.85, 382.50, "75°C", "Максимальная мощность"),
        ("Pablerso's Latency v0.4.2", 30.75, 24.65, 36.85, 382.50, "75°C", "Минимальные задержки"),
        ("Pcmy Ultimate", 30.75, 24.65, 36.85, 382.50, "75°C", "Экстремальная производительность"),
        ("Retch_Low_Latency_1.2", 30.75, 24.65, 36.85, 382.50, "75°C", "Минимальные задержки"),
        ("STRENGTH", 30.85, 24.75, 36.95, 381.50, "75°C", "Максимальная производительность"),
        ("Ultra Low Latency", 30.75, 24.65, 36.85, 382.50, "75°C", "Минимальные задержки"),
        ("Anti Lag", 30.75, 24.65, 36.85, 382.50, "75°C", "Минимальные задержки"),
        ("Desktop Low Latency Tom", 30.75, 24.65, 36.85, 382.50, "75°C", "Минимальные задержки для десктопа"),
        ("Rat Low Latency 1", 30.75, 24.65, 36.85, 382.50, "75°C", "Минимальные задержки"),
        ("Highest Performance No Idle", 30.75, 24.65, 36.85, 382.50, "75°C", "Максимальная производительность без простоя"),
        ("Catto PowerPlan Win10", 30.90, 24.80, 37.00, 381.00, "74°C", "Оптимизированный для Windows 10"),
        ("Catto PowerPlan Win7", 31.00, 25.00, 37.20, 379.00, "73°C", "Оптимизированный для Windows 7"),
        ("DANSKE POWER PLAN", 30.95, 24.85, 37.05, 380.50, "74°C", "Сбалансированный план"),
        ("Des1de Power Plan", 30.85, 24.75, 36.95, 381.50, "75°C", "Оптимизированный для игр"),
        ("ForgedOS Power Plan", 30.80, 24.70, 36.90, 382.00, "75°C", "Максимальная производительность"),
        ("Hand's PowerPlan", 31.00, 25.00, 37.20, 378.00, "73°C", "Универсальный план"),
        ("KernelOS Performance", 30.90, 24.80, 37.00, 381.00, "74°C", "Оптимизированный для ядра"),
        ("Legion Performance", 30.95, 24.85, 37.05, 380.50, "74°C", "Оптимизированный для ноутбуков"),
        ("Phantom Power Plan", 30.85, 24.75, 36.95, 381.50, "75°C", "Максимальная производительность"),
        ("Ron's Power Plan", 31.00, 25.00, 37.20, 378.00, "73°C", "Сбалансированный план"),
        ("ShDW Power Plan", 30.90, 24.80, 37.00, 381.00, "74°C", "Оптимизированный для игр"),
        ("Trix's Recommended", 31.05, 25.05, 37.25, 377.00, "73°C", "Рекомендуемый план"),
        ("Velo's Power Plan", 30.95, 24.85, 37.05, 380.00, "74°C", "Универсальный план"),
        ("Adamx's Power Plan", 30.90, 24.80, 37.00, 381.00, "74°C", "Оптимизированный для игр"),
        ("Alchemy", 31.00, 25.00, 37.20, 378.00, "73°C", "Экспериментальный план"),
        ("ATU Power Plan", 30.95, 24.85, 37.05, 380.00, "74°C", "Автоматическая настройка"),
        ("Auto Tweaking Utility", 30.90, 24.80, 37.00, 381.00, "74°C", "Автоматическая оптимизация"),
        ("CoreLimit-50per", 31.20, 25.40, 37.80, 375.00, "72°C", "Ограничение CPU 50%"),
        ("Deon's Power Plan", 30.95, 24.85, 37.05, 380.00, "74°C", "Универсальный план"),
        ("DraganOS", 30.90, 24.80, 37.00, 381.00, "74°C", "Оптимизированный для игр"),
        ("Duck", 31.00, 25.00, 37.20, 378.00, "73°C", "Сбалансированный план"),
        ("EonX", 30.95, 24.85, 37.05, 380.00, "74°C", "Универсальный план"),
        ("Gio Intel", 31.00, 25.00, 37.20, 378.00, "73°C", "Оптимизированный для Intel"),
        ("Huncho's Power Plan", 30.95, 24.85, 37.05, 380.00, "74°C", "Универсальный план"),
        ("Igromanoff v1", 30.90, 24.80, 37.00, 381.00, "74°C", "Оптимизированный для игр"),
        ("Igromanoff v2", 30.85, 24.75, 36.95, 381.50, "75°C", "Улучшенная версия v1"),
        ("Imribiy", 30.95, 24.85, 37.05, 380.00, "74°C", "Универсальный план"),
        ("Kirby Powerplan v1.1", 30.90, 24.80, 37.00, 381.00, "74°C", "Оптимизированный для игр"),
        ("Kirby Powerplan v1.2", 30.85, 24.75, 36.95, 381.50, "75°C", "Улучшенная версия v1.1"),
        ("Laptop Power Plan", 31.10, 25.20, 37.60, 375.00, "72°C", "Оптимизированный для ноутбуков"),
        ("Nani's Powerplan", 30.95, 24.85, 37.05, 380.00, "74°C", "Универсальный план"),
        ("PowerX v1", 30.90, 24.80, 37.00, 381.00, "74°C", "Оптимизированный для игр"),
        ("PowerX v2", 30.85, 24.75, 36.95, 381.50, "75°C", "Улучшенная версия v1"),
        ("RekOS Power Plan", 30.95, 24.85, 37.05, 380.00, "74°C", "Универсальный план"),
        ("Revision Power Plan V2.8", 30.90, 24.80, 37.00, 381.00, "74°C", "Оптимизированный для игр"),
        ("Revision Power Plan V2.9", 30.85, 24.75, 36.95, 381.50, "75°C", "Улучшенная версия v2.8"),
        ("Stony", 30.95, 24.85, 37.05, 380.00, "74°C", "Универсальный план"),
        ("Stormies Plan BTW", 30.90, 24.80, 37.00, 381.00, "74°C", "Оптимизированный для игр"),
        ("TypeX", 30.95, 24.85, 37.05, 380.00, "74°C", "Универсальный план"),
        ("Ultimate Performance V2", 30.90, 24.80, 37.00, 381.00, "74°C", "Максимальная производительность"),
        ("Win10GE Maximum Performance", 30.85, 24.75, 36.95, 381.50, "75°C", "Максимальная производительность"),
        ("Yuki's Main", 30.95, 24.85, 37.05, 380.00, "74°C", "Универсальный план"),
        ("Zoyota's Power Plan", 30.90, 24.80, 37.00, 381.00, "74°C", "Оптимизированный для игр"),
        ("APB-OS (2)", 30.90, 24.80, 37.00, 381.00, "74°C", "Оптимизированный для игр"),
        ("APB-OS (7)", 31.00, 25.00, 37.20, 378.00, "73°C", "Оптимизированный для Windows 7"),
        ("Azurite Power Plan", 30.95, 24.85, 37.05, 380.00, "74°C", "Универсальный план"),
        ("Community Plan v3", 30.90, 24.80, 37.00, 381.00, "74°C", "Сообщественный план"),
        ("Dato High Performance", 30.85, 24.75, 36.95, 381.50, "75°C", "Максимальная производительность"),
        ("EchoX", 30.95, 24.85, 37.05, 380.00, "74°C", "Универсальный план"),
        ("The World of PC's Nexus LiteOS", 30.90, 24.80, 37.00, 381.00, "74°C", "Оптимизированный для LiteOS"),
        ("fast_shift_L", 30.90, 24.80, 37.00, 381.00, "74°C", "Быстрый сдвиг (L)"),
        ("fast_shift_L_NoTB", 30.95, 24.85, 37.05, 380.00, "74°C", "Быстрый сдвиг без турбо"),
        ("fast_shift_P", 30.85, 24.75, 36.95, 381.50, "75°C", "Быстрый сдвиг (P)"),
        ("fast_shift_P_NoTB", 30.90, 24.80, 37.00, 381.00, "74°C", "Быстрый сдвиг без турбо"),
        ("JamessJ Plan de energia IDLE ON", 31.00, 25.00, 37.20, 378.00, "73°C", "С простоем"),
        ("kapselegg_v3_IDLE_ON", 31.00, 25.00, 37.20, 378.00, "73°C", "С простоем"),
        ("kn", 30.95, 24.85, 37.05, 380.00, "74°C", "Универсальный план"),
        ("retard", 30.95, 24.85, 37.05, 380.00, "74°C", "Универсальный план"),
        ("PowerPlan", 30.95, 24.85, 37.05, 380.00, "74°C", "Базовый план"),
        ("Windows 10 Revision", 30.95, 24.85, 37.05, 380.00, "74°C", "План Revision для Windows 10"),
        ("Tom Intel 2", 30.95, 24.85, 37.05, 380.00, "74°C", "Альтернативный план для Intel"),
        ("Intel Performance", 30.95, 24.85, 37.05, 380.00, "74°C", "Оптимизированный для Intel"),
        ("ggOS 0.8 Test", 30.95, 24.85, 37.05, 380.00, "74°C", "Тестовая версия 0.8"),
        ("Unicorn", 30.95, 24.85, 37.05, 380.00, "74°C", "Универсальный план"),
        ("YazanPowePlan", 30.95, 24.85, 37.05, 380.00, "74°C", "Универсальный план"),
        ("wZak_PowerPlan_v.1", 30.90, 24.80, 37.00, 381.00, "74°C", "Оптимизированный для игр"),
        ("PTU Powerplan Taco Shack", 30.90, 24.80, 37.00, 381.00, "74°C", "Оптимизированный для игр"),
        ("Xvii Power", 30.90, 24.80, 37.00, 381.00, "74°C", "Оптимизированный для игр"),
        ("Stony X iiYouseF", 30.95, 24.85, 37.05, 380.00, "74°C", "Оптимизированный для игр"),
        ("Disable Pstate0", 30.80, 24.70, 36.90, 382.00, "75°C", "Отключение P-state 0"),
        ("AMD with Boost", 30.85, 24.75, 36.95, 381.50, "75°C", "Оптимизированный для AMD с бустом"),
        ("ggOS 0.7.6", 31.00, 25.00, 37.20, 378.00, "73°C", "Версия 0.7.6"),
        ("TYT_power_plan_idle_on_normal_use_V3", 31.00, 25.00, 37.20, 378.00, "73°C", "Обычный режим с простоем")
    ]

    for item in data:
        tree.insert("", "end", values=item)

    # Скроллбар
    vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)

    # Используем pack вместо grid
    tree.pack(side="left", fill="both", expand=True)
    vsb.pack(side="right", fill="y")

    # Подпись внизу
    footer = ttk.Label(
        tab_frame,
        text="Источник данных: https://docs.google.com/spreadsheets/d/1ZAf3DfL-dPNSOpi5rNlNiaCwIlk_Z7iTRFM3lqMhQeo",
        font=("Segoe UI", 9),
        foreground="#6c757d",
    )
    footer.pack(side="bottom", fill="x", pady=5)

    return tab_frame


# Теперь добавляем вкладку
tab_control.add(create_power_tab(), text="Электропитание")

# Добавляем все вкладки с чекбоксами
for tab_name, checkbox_names in tabs_main.items():  # Изменяем tabs на tabs_main
    tab_frame = ttk.Frame(tab_control)
    tab_control.add(tab_frame, text=tab_name)

    # Создаем метку-заполнитель с улучшенным стилем
    placeholder = ttk.Label(
        tab_frame,
        text="Загрузка содержимого...",
        font=("Segoe UI", 12),
        foreground="#32FBE2",
    )
    placeholder.pack(expand=True)

    # Сохраняем информацию о вкладке
    tab_frame.tab_info = {
        "name": tab_name,
        "checkbox_names": checkbox_names,
        "loaded": False,
    }

"""
+------------------------------------+
| Функция для обработки смены        |
| вкладки                            |
+------------------------------------+
"""


def on_tab_changed(event):
    current = tab_control.select()
    if not current:
        return

    tab_frame = tab_control.children[current.split(".")[-1]]

    if not hasattr(tab_frame, "tab_info") or tab_frame.tab_info["loaded"]:
        return

    if tab_frame.tab_info["name"] == "Главная":
        create_main_tab_content(tab_frame)
    else:
        create_tab_content(
            tab_frame.tab_info["name"], tab_frame, tab_frame.tab_info["checkbox_names"]
        )

    tab_frame.tab_info["loaded"] = True


def export_full_registry():
    try:
        # Create backup directory with timestamp
        backup_dir = os.path.join(os.getcwd(), "Backup")
        os.makedirs(backup_dir, exist_ok=True)

        # Create backup file with timestamp
        backup_file = os.path.join(
            backup_dir,
            f"FullRegistryBackup_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.reg",
        )

        # Export full registry
        subprocess.run(["reg", "export", "HKLM", backup_file, "/y"], check=True)

        messagebox.showinfo(
            "Успех", f"Полная резервная копия реестра создана в:\n{backup_file}"
        )
    except Exception as e:
        messagebox.showerror(
            "Ошибка", f"Не удалось создать полную резервную копию реестра:\n{str(e)}"
        )


def import_registry_backup(backup_list=None):
    if not backup_list:
        messagebox.showwarning(
            "Предупреждение", "Пожалуйста, выберите бэкап для импорта"
        )
        return

    selection = backup_list.curselection()
    if not selection:
        messagebox.showwarning(
            "Предупреждение", "Пожалуйста, выберите бэкап для импорта"
        )
        return

    backup_name = backup_list.get(selection[0])
    backup_path = os.path.join(os.getcwd(), "Backup", backup_name)

    if messagebox.askyesno("Подтверждение", f"Импортировать бэкап {backup_name}?"):
        try:
            if os.path.isdir(backup_path):
                # Directory backup - import all .reg files
                reg_files = [f for f in os.listdir(backup_path) if f.endswith(".reg")]
                for reg_file in reg_files:
                    full_path = os.path.join(backup_path, reg_file)
                    subprocess.run(["reg", "import", full_path], check=True)
            else:
                # Single file backup
                subprocess.run(["reg", "import", backup_path], check=True)

            messagebox.showinfo("Успех", "Бэкап успешно импортирован")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось импортировать бэкап: {str(e)}")


def update_backup_list(backup_list):
    """Обновляет список бэкапов в интерфейсе"""
    if not backup_list:
        return

    # Очищаем список перед обновлением
    backup_list.delete(0, tk.END)

    # Проверяем наличие директории с бэкапами
    backup_dir = os.path.join(os.getcwd(), "Backup")
    if not os.path.exists(backup_dir):
        return

    # Получаем список всех элементов в директории
    try:
        items = os.listdir(backup_dir)
    except Exception as e:
        print(f"Ошибка при чтении директории бэкапов: {e}")
        return

    # Разделяем директории и файлы
    dir_backups = [
        d
        for d in items
        if os.path.isdir(os.path.join(backup_dir, d))
        and d.startswith("RegistryBackup_")
    ]

    file_backups = [
        f
        for f in items
        if os.path.isfile(os.path.join(backup_dir, f))
        and f.startswith("FullRegistryBackup_")
    ]

    # Сортируем оба списка
    dir_backups.sort(reverse=True)
    file_backups.sort(reverse=True)

    # Добавляем сначала директории
    for backup in dir_backups:
        backup_list.insert(tk.END, backup)

    # Затем добавляем файлы
    for backup in file_backups:
        backup_list.insert(tk.END, backup)


# Привязываем обработчик к событию смены вкладки
tab_control.bind("<<NotebookTabChanged>>", on_tab_changed)

# Получаем функцию для начальной вкладки
initial_tab_func = globals().get(
    config.get("General", "initial_tab", fallback="switch_to_main")
)
if initial_tab_func:
    # Проверяем, требует ли функция аргумент tab_control
    import inspect

    if len(inspect.signature(initial_tab_func).parameters) == 1:
        initial_tab_func(tab_control)
    else:
        initial_tab_func()

# Вызываем функцию для установки начального стиля компонентов интерфейса
update_font_style(update_window=False)  # Не обновляем окно при начальной загрузке для ускорения

# Список темных тем
dark_themes = [
    "cyberpunk",
    "hacker",
    "palenight",
    "darklysuperhero",
    "solar",
    "cyborg",
    "vapor",
]

update_button_style()

# Применяем настройки видимости панелей в самом конце, после всех инициализаций
show_top_panel = config.getboolean("General", "show_top_panel", fallback=True)
show_sidebar = config.getboolean("General", "show_sidebar", fallback=True)

if not show_top_panel:
    top_panel.pack_forget()

if not show_sidebar:
    sidebar.pack_forget()

# при нажатии кнопки F5, вызываем функцию reload_program
root.bind("<F5>", reload_program)

# Вызываем open_random_site после создания окна (неблокирующий вызов)
root.after(1000, lambda: open_random_site(5))  # Задержка 1 секунда после запуска

# Проверка обновлений после полного запуска программы (неблокирующий вызов)
root.after(2000, check_for_updates_threaded)  # Задержка 2 секунды после запуска для проверки обновлений

# Запуск главного цикла приложения для отображения окна
logger.log_program_start()  # Логируем запуск программы
root.mainloop()  # Запускаем главный цикл обработки событий, чтобы интерфейс оставался открытым