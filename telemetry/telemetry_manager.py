import os
import zipfile
import shutil
from datetime import datetime
import telebot
import configparser

# если есть файл config.py, то используем его, иначе используем config_for_github.py
if os.path.exists('config.py'):
    from .config import verify_and_get_credentials
else:
    from .config_for_github import verify_and_get_credentials

def save_user_info(telegram_username='', telegram_nickname='', telegram_user_id='', mark_fetch_attempted=False):
    """Сохраняет информацию о пользователе в настройки
    
    Args:
        telegram_username: Username пользователя Telegram (@username без @) - только если введен вручную
        telegram_nickname: Отображаемое имя пользователя (first_name) - только если введено вручную
        telegram_user_id: Числовой ID пользователя Telegram
        mark_fetch_attempted: Если True, помечает что попытка получения user_id уже была
    """
    try:
        config = configparser.ConfigParser()
        config.read('user_data//settings.ini', encoding='cp1251')
        
        if not config.has_section('User'):
            config.add_section('User')
        
        # Сохраняем username и nickname только если они переданы (введены пользователем вручную)
        if telegram_username:
            config.set('User', 'telegram_username', telegram_username)
        if telegram_nickname:
            config.set('User', 'telegram_nickname', telegram_nickname)
        if telegram_user_id:
            config.set('User', 'telegram_user_id', str(telegram_user_id))
        if mark_fetch_attempted:
            config.set('User', 'telegram_user_id_fetch_attempted', 'True')
        
        with open('user_data//settings.ini', 'w', encoding='cp1251') as configfile:
            config.write(configfile)
    except Exception as e:
        print(f'Ошибка сохранения информации о пользователе: {e}')


def is_valid_username(username):
    """Проверяет, является ли строка валидным Telegram username (а не именем пользователя)
    
    Args:
        username: Строка для проверки
        
    Returns:
        bool: True если это валидный username, False иначе
    """
    if not username:
        return False
    
    # Убираем @ если есть
    clean_username = username.lstrip('@').strip()
    
    # Username должен:
    # - Не быть пустым
    # - Не содержать пробелов (имена могут содержать пробелы)
    # - Содержать только буквы, цифры и подчеркивания
    # - Быть не пустым
    if not clean_username or ' ' in clean_username:
        return False
    
    # Проверяем, что содержит только допустимые символы (буквы, цифры, подчеркивания)
    if not clean_username.replace('_', '').isalnum():
        return False
    
    return True

def format_telegram_link(telegram_username, telegram_user_id):
    """Формирует ссылку на Telegram аккаунт пользователя
    
    Args:
        telegram_username: Username пользователя Telegram (@username без @)
        telegram_user_id: Числовой ID пользователя Telegram
        
    Returns:
        str: Ссылка на Telegram аккаунт пользователя в формате:
            - https://t.me/username (если есть валидный username)
            - Пустая строка (если нет валидного username)
    """
    # Ссылку создаем ТОЛЬКО если есть реальный валидный username
    if telegram_username and not telegram_username.startswith('http'):
        # Если username начинается с @, убираем его
        clean_username = telegram_username.lstrip('@').strip()
        
        # Проверяем, что это валидный username
        if is_valid_username(clean_username):
            return f'https://t.me/{clean_username}'
    
    # Если username нет или он невалидный, возвращаем пустую строку
    return ''

def get_user_info():
    """Получает информацию о пользователе из настроек, пытается получить только user_id из Telegram
    
    Returns:
        tuple: (windows_username, telegram_username, telegram_nickname, telegram_user_id)
            - windows_username: Имя учетной записи Windows
            - telegram_username: Username Telegram (@username без @) - только если введен пользователем вручную
            - telegram_nickname: Отображаемое имя пользователя (first_name) - только если введено пользователем вручную
            - telegram_user_id: Числовой ID пользователя Telegram
    """
    windows_username = os.getenv('USERNAME', 'unknown')
    telegram_username = ''
    telegram_nickname = ''
    telegram_user_id = ''
    
    try:
        config = configparser.ConfigParser()
        config.read('user_data//settings.ini', encoding='cp1251')
        # Используем только ручной username из настроек (если пользователь ввел его вручную)
        telegram_username = config.get('User', 'telegram_username', fallback='')
        telegram_nickname = config.get('User', 'telegram_nickname', fallback='')
        telegram_user_id = config.get('User', 'telegram_user_id', fallback='')
        # Проверяем, была ли уже попытка получить user_id
        fetch_attempted = config.getboolean('User', 'telegram_user_id_fetch_attempted', fallback=False)
    except Exception:
        fetch_attempted = False
    
    # Если user_id нет и еще не было попытки получить его, пытаемся получить только user_id из Telegram
    if not telegram_user_id and not fetch_attempted:
        try:
            TOKEN, chat_id = verify_and_get_credentials()
            
            # Если chat_id выглядит как user_id (положительное число), используем его
            if chat_id and chat_id.lstrip('-').isdigit():
                try:
                    chat_id_int = int(chat_id)
                    # user_id обычно положительные числа (личные чаты)
                    if chat_id_int > 0:
                        telegram_user_id = str(chat_id_int)
                        save_user_info(telegram_user_id=telegram_user_id, mark_fetch_attempted=True)
                except Exception:
                    pass
            
            # Если не получили user_id из chat_id, пробуем через getChat (для личных чатов)
            if not telegram_user_id:
                try:
                    bot = telebot.TeleBot(TOKEN)
                    chat = bot.get_chat(chat_id)
                    # Получаем только user_id, не username и не nickname
                    if hasattr(chat, 'id') and chat.id:
                        telegram_user_id = str(chat.id)
                        save_user_info(telegram_user_id=telegram_user_id, mark_fetch_attempted=True)
                except Exception:
                    pass
            
            # Помечаем, что попытка была сделана, даже если ничего не получилось
            if not telegram_user_id:
                save_user_info(mark_fetch_attempted=True)
        except Exception as e:
            print(f'Ошибка получения user_id из Telegram: {e}')
            # Помечаем, что попытка была сделана, даже если произошла ошибка
            try:
                save_user_info(mark_fetch_attempted=True)
            except:
                pass
    
    return windows_username, telegram_username, telegram_nickname, telegram_user_id

class TelemetryManager:
    def __init__(self):
        pass  # Никакой инициализации не требуется

    def get_credentials(self):
        return verify_and_get_credentials()

    def send_telegram(self, file_path, share_enabled=False):
        # Получаем декодированные значения
        TOKEN, chat_id = self.get_credentials()
        bot = telebot.TeleBot(TOKEN)
        try:
            # Получаем только имя пользователя Windows
            windows_username = os.getenv('USERNAME', 'unknown')
            
            with open(file_path, 'rb') as f:
                # Определяем тип файла для сообщения
                filename = os.path.basename(file_path)
                if filename.endswith('.zip'):
                    # Проверяем, является ли это архивом телеметрии
                    if 'telemetry' in filename.lower():
                        caption = f'Телеметрия: {filename}\n'
                        caption += f'👤 Пользователь: #{windows_username}\n'
                        # Добавляем метку о разрешении обмена
                        if share_enabled:
                            caption += '[SHARED] Обмен разрешен'
                    else:
                        caption = f'Архив с лог файлами: {filename}\n'
                        caption += f'👤 Пользователь: #{windows_username}\n'
                elif filename.endswith('.log'):
                    caption = f'Лог файл: {filename}\n'
                    caption += f'👤 Пользователь: #{windows_username}\n'
                else:
                    caption = f'Файл: {filename}\n'
                    caption += f'👤 Пользователь: #{windows_username}\n'
                    
                bot.send_document(chat_id, f, caption=caption)
        except Exception as e:
            print(f'Ошибка отправки в Telegram: {e}')

    def send_message(self, message):
        """
        Отправляет текстовое сообщение через Telegram
        
        Args:
            message (str): Текст сообщения для отправки
            
        Returns:
            bool: True если сообщение успешно отправлено, False в случае ошибки
        """
        try:
            TOKEN, chat_id = self.get_credentials()
            bot = telebot.TeleBot(TOKEN)
            
            bot.send_message(chat_id, message)
            return True
        except Exception as e:
            print(f'Ошибка отправки сообщения в Telegram: {e}')
            return False

    def collect_telemetry_data(self, share_enabled=False):
        username = os.getenv('USERNAME', 'unknown')
        current_date = datetime.now().strftime('%Y-%m-%d')
        seconds = datetime.now().strftime('%H-%M-%S')
        archive_name = f'Telemetry-{username}-{current_date}-{seconds}.zip'
        temp_dir = 'user_data//temp'
        os.makedirs(temp_dir, exist_ok=True)
        try:
            # Копируем все файлы из user_data\logs, кроме temp
            for root, dirs, files in os.walk('user_data//logs'):
                if 'temp' in root:
                    continue
                rel_path = os.path.relpath(root, 'user_data')
                temp_path = os.path.join(temp_dir, rel_path)
                os.makedirs(temp_path, exist_ok=True)
                for file in files:
                    src_file = os.path.join(root, file)
                    dst_file = os.path.join(temp_path, file)
                    shutil.copy2(src_file, dst_file)
            # Создаём архив
            archive_path = f'user_data//{archive_name}'
            with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, temp_dir)
                        zipf.write(file_path, arcname)
            # Отправляем архив в Telegram с информацией о разрешении обмена
            self.send_telegram(archive_path, share_enabled=share_enabled)
            # Удаляем временные файлы
            shutil.rmtree(temp_dir)
            os.remove(archive_path)
            return True
        except Exception as e:
            print(f"Ошибка при сборе телеметрии: {str(e)}")
            return False

    def get_shared_telemetry(self, limit=50):
        """
        Получает телеметрию других пользователей через Telegram Bot API
        
        Args:
            limit (int): Максимальное количество сообщений для получения
            
        Returns:
            list: Список словарей с информацией о телеметрии других пользователей
        """
        try:
            TOKEN, chat_id = self.get_credentials()
            bot = telebot.TeleBot(TOKEN)
            
            telemetry_list = []
            
            try:
                # Пробуем получить обновления через getUpdates
                # Это работает автоматически для личных чатов - не требуется запуск бота
                # Для каналов getUpdates не работает, нужны права администратора
                # Получаем обновления без offset, чтобы получить последние сообщения
                # Используем более длительный timeout для надежности
                updates = bot.get_updates(limit=limit, timeout=10)
                
                if not updates:
                    # Если обновлений нет, это нормально - просто еще нет телеметрии от других пользователей
                    return telemetry_list
                
                for update in updates:
                    if update.message and update.message.document:
                        doc = update.message.document
                        # Проверяем, является ли это файлом телеметрии
                        if doc.file_name and ('telemetry' in doc.file_name.lower() or doc.file_name.endswith('.zip')):
                            caption = update.message.caption or ''
                            # Показываем только телеметрию от пользователей, которые включили обмен
                            if '[SHARED]' in caption or 'Обмен разрешен' in caption:
                                # Извлекаем информацию из caption
                                username_from_caption = 'Неизвестно'
                                user_id_from_caption = 0
                                
                                # Пытаемся извлечь username из caption
                                if 'Username: @' in caption:
                                    try:
                                        username_line = [line for line in caption.split('\n') if 'Username: @' in line][0]
                                        username_from_caption = username_line.split('@')[1].strip()
                                    except:
                                        pass
                                
                                # Пытаемся извлечь user_id из caption
                                if 'Telegram User ID:' in caption:
                                    try:
                                        user_id_line = [line for line in caption.split('\n') if 'Telegram User ID:' in line][0]
                                        user_id_from_caption = int(user_id_line.split(':')[1].strip())
                                    except:
                                        pass
                                
                                # Используем информацию из сообщения, если есть
                                if update.message.from_user:
                                    username = update.message.from_user.username or username_from_caption or 'Неизвестно'
                                    user_id = update.message.from_user.id if update.message.from_user.id else user_id_from_caption
                                else:
                                    username = username_from_caption
                                    user_id = user_id_from_caption
                                
                                telemetry_info = {
                                    'username': username,
                                    'user_id': user_id,
                                    'file_name': doc.file_name,
                                    'file_size': doc.file_size or 0,
                                    'date': datetime.fromtimestamp(update.message.date).strftime('%Y-%m-%d %H:%M:%S') if update.message.date else 'Неизвестно',
                                    'caption': caption,
                                    'message_id': update.message.message_id
                                }
                                telemetry_list.append(telemetry_info)
                
            except Exception as api_error:
                error_msg = str(api_error)
                # Проверяем, является ли это ошибкой из-за использования канала
                if 'chat not found' in error_msg.lower() or 'channel' in error_msg.lower():
                    print('Примечание: Функция обмена телеметрией работает только для личных чатов с ботом.')
                    print('Для работы с каналами бот должен быть администратором канала.')
                else:
                    print(f'Ошибка API при получении телеметрии через getUpdates: {api_error}')
                    print('Убедитесь, что бот настроен правильно и вы используете личный чат с ботом.')
            
            return telemetry_list
        except Exception as e:
            print(f'Ошибка получения телеметрии других пользователей: {e}')
            return [] 