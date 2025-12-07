import sys
import os
import traceback
from datetime import datetime
import telebot
import configparser
import glob
import uuid
import sys

# print("Checking for updates...")
# try:
#     import updater
#     updater.check_and_update(auto_update=True)  # Автоматическое обновление без запроса
# except Exception as e:
#     print(f"Ошибка при проверке обновлений: {e}")

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    print("Running in a PyInstaller bundle")
    if os.path.exists('config.py'):
        from telemetry.config import verify_and_get_credentials
    else:
        from telemetry.config_for_github import verify_and_get_credentials
else:
    print("Running in a normal Python environment")
    from telemetry.config_for_github import verify_and_get_credentials    

# Запуск программы
print("\nStarting Extreme...")

telemetry_override = None  # None = по настройкам, True = включить, False = отключить

# Обработка аргументов командной строки для управления телеметрией
TELEMETRY_OFF_FLAGS = {'-nt', '-n', '--no-telemetry'}
TELEMETRY_ON_FLAGS = {'-t', '-d', '--debugging', '--telemetry'}
for arg in sys.argv[1:]:
    if arg.lower() in TELEMETRY_OFF_FLAGS:
        telemetry_override = False
        print("[CLI] Telemetry will be DISABLED by command-line flag.")
        break
    elif arg.lower() in TELEMETRY_ON_FLAGS:
        telemetry_override = True
        print("[CLI] Telemetry will be ENABLED by command-line flag.")
        break

def is_telemetry_enabled():
    """Проверяет, включена ли отправка телеметрии в настройках или переопределена через аргумент"""
    global telemetry_override
    if telemetry_override is not None:
        return telemetry_override
    try:
        config = configparser.ConfigParser()
        config.read('user_data//settings.ini', encoding='cp1251')
        return config.getboolean('Telemetry', 'send_on_close', fallback=True)
    except Exception as e:
        print(f"Error checking telemetry settings: {e}")
        return True  # По умолчанию включено, если не удалось прочитать настройки

def send_telegram_message(message):
    """Отправляет сообщение в Telegram"""
    try:
        # Проверяем настройки
        if not is_telemetry_enabled():
            return
            
        token, chat_id = verify_and_get_credentials()
        
        # Отправляем сообщение
        bot = telebot.TeleBot(token)
        bot.send_message(chat_id, message)
    except Exception as e:
        print(f"Ошибка при отправке сообщения в Telegram: {str(e)}")

def send_error_to_telegram(exc_type=None, exc_value=None, exc_traceback=None):
    """Отправляет информацию об ошибке в Telegram"""
    try:
        # Проверяем настройки
        if not is_telemetry_enabled():
            return
            
        # Если аргументы не переданы, пробуем получить информацию об ошибке
        if exc_type is None:
            exc_type, exc_value, exc_traceback = sys.exc_info()
        
        # Проверяем, есть ли реальная ошибка
        if exc_type is None:
            return  # Нет ошибки, выходим из функции
        
        # Формируем сообщение об ошибке
        error_message = f"⚠️ Критическая ошибка в Extreme!\n\n"
        
        # Безопасно получаем имя типа ошибки
        try:
            error_type = exc_type.__name__ if exc_type and hasattr(exc_type, '__name__') else str(exc_type)
        except:
            error_type = "Unknown Error"
        
        error_message += f"Тип ошибки: {error_type}\n"
        error_message += f"📝 Сообщение: {str(exc_value) if exc_value is not None else 'Нет сообщения об ошибке'}\n"
        error_message += f"⏰ Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        error_message += f"👤 Пользователь: #{os.getenv('USERNAME', 'unknown')}\n\n"
        error_message += f"🐍 Python версия: {sys.version}\n"
        
        # Добавляем стек вызовов, если он есть
        if exc_traceback is not None:
            try:
                error_message += "Стек вызовов:\n"
                error_message += "".join(traceback.format_tb(exc_traceback))
            except:
                error_message += "Не удалось получить стек вызовов\n"
        
        # Отправляем сообщение
        send_telegram_message(error_message)
        
    except Exception as e:
        print(f"Ошибка при отправке уведомления: {str(e)}")
        # Пробуем отправить хотя бы базовое сообщение об ошибке
        try:
            send_telegram_message(f"⚠️ Произошла ошибка в Extreme, но не удалось получить детали: {str(e)}")
        except:
            pass

def send_log_file():
    """Отправляет последний созданный лог-файл"""
    try:
        print("Attempting to send log file...")
        # Ищем все лог-файлы в директории user_data//logs
        log_files = glob.glob('user_data//logs/*.log')
        if not log_files:
            print("No log files found")
            return
            
        # Сортируем по времени создания (самый новый последний)
        latest_log = max(log_files, key=os.path.getctime)
        print(f"Found latest log file: {latest_log}")
        
        # Отправляем файл
        from telemetry.telemetry_manager import TelemetryManager
        manager = TelemetryManager()
        
        # Читаем содержимое лог-файла
        try:
            with open(latest_log, 'r', encoding='utf-8') as f:
                log_content = f.read()
                
            # Формируем сообщение с содержимым лог-файла
            log_message = f"📝 Содержимое лог-файла {os.path.basename(latest_log)}:\n\n{log_content}"
            manager.send_message(log_message)
            print("Log file content sent successfully")
        except Exception as e:
            print(f"Ошибка при чтении лог-файла: {str(e)}")
            
    except Exception as e:
        print(f"Ошибка при отправке лог-файла: {str(e)}")

def custom_exception_handler(exc_type, exc_value, exc_traceback):
    """Пользовательский обработчик исключений"""
    print("Exception caught by custom handler:")
    print(f"Type: {exc_type}")
    print(f"Value: {exc_value}")
    print("Traceback:")
    traceback.print_tb(exc_traceback)
    
    # Отправляем информацию об ошибке
    send_error_to_telegram(exc_type, exc_value, exc_traceback)
    # Вызываем стандартный обработчик для вывода в консоль
    sys.__excepthook__(exc_type, exc_value, exc_traceback)

print("Setting up exception handler...")
# Устанавливаем обработчик необработанных исключений
sys.excepthook = custom_exception_handler

print("Starting main program...")
try:
    # Запускаем основную программу
    print("Importing main module...")
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        import main
    else:
        import main
    print("Main module imported successfully")
    
    # Если программа успешно импортирована, устанавливаем функцию для отправки телеметрии при закрытии
    if is_telemetry_enabled():
        print("Telemetry is enabled")
        # Отправляем лог-файл
        send_log_file()
        print("Collecting and sending telemetry...")
        main.collect_and_send()
    else:
        print("Telemetry is disabled")
    
except Exception as e:
    print(f"Error in main program: {e}")
    print("Traceback:")
    traceback.print_exc()
    # Если произошла ошибка при импорте или запуске
    send_error_to_telegram()
    raise  # Повторно вызываем исключение для отображения в консоли 