"""
Модуль с инструментами для режима разработчика
Содержит функции для очистки твиков, удаления файлов и других операций
"""
import os
import re
import subprocess
import shutil
from pathlib import Path
from contextlib import contextmanager
import sys
import io


def remove_attributes_and_delete_files(target_dir, extensions):
    """
    Удаляет файлы с указанными расширениями в целевой директории
    
    Args:
        target_dir (str): Целевая директория
        extensions (list): Список расширений файлов (например, ['.lnk', '.ico', '.txt'])
    
    Returns:
        dict: Результат операции с количеством удаленных файлов и ошибками
    """
    result = {
        'deleted_count': 0,
        'errors': []
    }
    
    if not os.path.exists(target_dir):
        result['errors'].append(f"Директория {target_dir} не существует")
        return result
    
    # Устанавливаем текущую директорию
    original_dir = os.getcwd()
    try:
        os.chdir(target_dir)
        
        # Для каждого расширения
        for ext in extensions:
            # Рекурсивно ищем все файлы с этим расширением
            for root, dirs, files in os.walk('.'):
                for file in files:
                    if file.lower().endswith(ext.lower()):
                        file_path = os.path.join(root, file)
                        try:
                            # Удаляем атрибуты (readonly, archive, system, hidden)
                            os.chmod(file_path, 0o777)
                            # Удаляем файл
                            os.remove(file_path)
                            result['deleted_count'] += 1
                        except Exception as e:
                            result['errors'].append(f"Ошибка при удалении {file_path}: {e}")
        
    finally:
        os.chdir(original_dir)
    
    return result


def remove_numbers_and_points_from_start(target_dir):
    """
    Удаляет числа и точки из начала имен файлов и папок
    
    Args:
        target_dir (str): Целевая директория
    
    Returns:
        dict: Результат операции с количеством переименованных файлов и ошибками
    """
    result = {
        'renamed_files': 0,
        'renamed_dirs': 0,
        'deleted_empty_dirs': 0,
        'errors': []
    }
    
    def remove_numbers_and_points_from_start(name):
        """Удаляет все точки и цифры в начале имени"""
        base_name, ext = os.path.splitext(name)
        new_base_name = re.sub(r'^[.\d]+', '', base_name)
        return new_base_name + ext
    
    if not os.path.exists(target_dir):
        result['errors'].append(f"Директория {target_dir} не существует")
        return result
    
    # Обрабатываем папки и файлы в обратном порядке для корректного удаления пустых папок
    for root, dirs, files in os.walk(target_dir, topdown=False):
        # Обработка файлов
        for filename in files:
            old_path = os.path.join(root, filename)
            new_filename = remove_numbers_and_points_from_start(filename)
            if new_filename != filename:
                new_path = os.path.join(root, new_filename)
                try:
                    os.rename(old_path, new_path)
                    result['renamed_files'] += 1
                except Exception as e:
                    result['errors'].append(f"Не удалось переименовать файл {old_path}: {e}")
        
        # Обработка папок
        for dirname in dirs:
            old_dir_path = os.path.join(root, dirname)
            new_dir_name = remove_numbers_and_points_from_start(dirname)
            if new_dir_name != dirname:
                new_dir_path = os.path.join(root, new_dir_name)
                try:
                    os.rename(old_dir_path, new_dir_path)
                    result['renamed_dirs'] += 1
                except Exception as e:
                    result['errors'].append(f"Не удалось переименовать папку {old_dir_path}: {e}")
        
        # После обработки всех файлов и папок, проверяем, пустая ли папка, чтобы удалить
        current_dir = root
        if current_dir != target_dir:  # чтобы не попытаться удалить корень
            try:
                if not os.listdir(current_dir):
                    os.rmdir(current_dir)
                    result['deleted_empty_dirs'] += 1
            except Exception as e:
                result['errors'].append(f"Не удалось удалить папку {current_dir}: {e}")
    
    return result


def convert_reg_to_bat(root_dir, reg_convert_exe_path):
    """
    Рекурсивно конвертирует все .reg файлы в .bat во всех папках и подпапках
    
    Args:
        root_dir (str): Корневая директория для поиска .reg файлов
        reg_convert_exe_path (str): Путь к RegConvert.exe
    
    Returns:
        dict: Результат операции с количеством сконвертированных файлов и ошибками
    """
    result = {
        'converted_count': 0,
        'error_count': 0,
        'errors': []
    }
    
    if not os.path.exists(reg_convert_exe_path):
        result['errors'].append(f"Файл {reg_convert_exe_path} не найден!")
        return result
    
    if not os.path.exists(root_dir):
        result['errors'].append(f"Директория {root_dir} не существует!")
        return result
    
    # Рекурсивно обходим все папки
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith('.reg'):
                reg_file_path = os.path.join(root, file)
                bat_file_path = os.path.splitext(reg_file_path)[0] + '.bat'
                
                try:
                    # Формируем команду для конвертации
                    cmd = [
                        reg_convert_exe_path,
                        f"/S={reg_file_path}",
                        "/O=BAT",
                        f"/T={bat_file_path}"
                    ]
                    
                    # Выполняем конвертацию
                    process_result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
                    
                    if process_result.returncode == 0:
                        result['converted_count'] += 1
                    else:
                        result['error_count'] += 1
                        result['errors'].append(
                            f"Ошибка при конвертации {reg_file_path}: {process_result.stderr}"
                        )
                        
                except Exception as e:
                    result['error_count'] += 1
                    result['errors'].append(f"Исключение при конвертации {reg_file_path}: {e}")
    
    return result


def remove_pause_and_exit_from_bat(target_dir):
    """
    Удаляет строки 'pause' и 'exit' из всех .bat и .cmd файлов в директории
    
    Args:
        target_dir (str): Целевая директория
    
    Returns:
        dict: Результат операции с количеством обработанных файлов и ошибками
    """
    result = {
        'processed_count': 0,
        'errors': []
    }
    
    if not os.path.exists(target_dir):
        result['errors'].append(f"Директория {target_dir} не существует")
        return result
    
    # Получаем список всех каталогов (без подкаталогов)
    directories = []
    for root, dirs, files in os.walk(target_dir):
        if root == target_dir:
            directories.extend(dirs)
        else:
            break
    
    # Удаляем pause и exit из bat файлов во всех каталогах
    for dir_name in directories:
        dir_path = os.path.join(target_dir, dir_name)
        if os.path.isdir(dir_path):
            for root, dirs, files in os.walk(dir_path):
                for file in files:
                    if file.endswith((".bat", ".cmd")):
                        filepath = os.path.join(root, file)
                        try:
                            with open(filepath, "rb") as f:
                                lines = f.readlines()
                            with open(filepath, "wb") as f:
                                for line in lines:
                                    if b"pause" not in line.lower() and b"exit" not in line.lower():
                                        f.write(line)
                            result['processed_count'] += 1
                        except Exception as e:
                            result['errors'].append(f"Ошибка при обработке файла {filepath}: {e}")
    
    return result


def create_tabs_file(target_dir, output_file='tabs.py'):
    """
    Создает файл tabs.py со структурой каталогов
    
    Args:
        target_dir (str): Целевая директория
        output_file (str): Имя выходного файла
    
    Returns:
        dict: Результат операции с путем к созданному файлу и ошибками
    """
    result = {
        'output_path': None,
        'errors': []
    }
    
    if not os.path.exists(target_dir):
        result['errors'].append(f"Директория {target_dir} не существует")
        return result
    
    try:
        # Получаем структуру каталогов: родительский каталог -> список подкаталогов
        parent_folders = {}
        
        for root, dirs, files in os.walk(target_dir):
            if root == target_dir:
                # Это корневые каталоги
                for dir_name in dirs:
                    dir_path = os.path.join(root, dir_name)
                    parent_folders[dir_name] = []
                    # Получаем подкаталоги для каждого родительского каталога
                    for sub_root, sub_dirs, sub_files in os.walk(dir_path):
                        if sub_root == dir_path:
                            # Это непосредственные подкаталоги родительского каталога
                            parent_folders[dir_name].extend(sub_dirs)
                        else:
                            break
        
        # Функция для получения всех путей
        def get_all_paths(directory, extensions=None, exclude_files=None, exclude_dirs=None):
            if extensions is None:
                extensions = []
            if exclude_files is None:
                exclude_files = []
            if exclude_dirs is None:
                exclude_dirs = []
            paths = []
            for root, _, files in os.walk(directory):
                if root not in exclude_dirs:
                    for file in files:
                        path = os.path.join(root, file)
                        if any(path.endswith(extension) for extension in extensions) and file not in exclude_files:
                            paths.append(path)
            return paths
        
        extensions = ['.bat', '.cmd', '.pow']
        exclude_files = ['PowerRun.exe', 'pssuspend.exe', 'TI.exe']
        exclude_dirs = ['tweaks', 'Source', 'Utils', '__pycache__', 'others']
        
        all_content = ""
        
        for i, (parent_name, sub_dirs) in enumerate(parent_folders.items()):
            tabs_name = f"tabs{i+1}" if i > 0 else "tabs"
            
            content = f"{tabs_name} = {{\n"
            
            # Для каждого подкаталога в родительском каталоге
            for sub_dir in sub_dirs:
                sub_dir_full_path = os.path.join(target_dir, parent_name, sub_dir)
                
                if sub_dir == 'Удалить приложения Microsoft':
                    exclude_subdirectories = ['Work']
                else:
                    exclude_subdirectories = []
                
                # Получаем все файлы в подкаталоге
                all_paths = get_all_paths(sub_dir_full_path, extensions, exclude_files, exclude_dirs)
                all_paths = [os.path.relpath(path, sub_dir_full_path) for path in all_paths]
                all_paths = [path for path in all_paths if not os.path.basename(path) == '.' and not any(subdirectory in path for subdirectory in exclude_subdirectories)]
                
                content += f"    '{sub_dir}': {all_paths},\n"
            content += "}\n\n"
            
            all_content += content
        
        # Записываем все в один файл
        output_path = os.path.join(target_dir, output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(all_content)
        
        result['output_path'] = output_path
        result['tabs_count'] = len(parent_folders)
        
    except Exception as e:
        result['errors'].append(f"Ошибка при создании файла tabs.py: {e}")
    
    return result


def clear_tweaks(target_dir):
    """
    Выполняет очистку твиков - удаляет все файлы с определенными расширениями
    
    Args:
        target_dir (str): Целевая директория
    
    Returns:
        dict: Результат операции
    """
    extensions = ['.lnk', '.ico', '.txt', '.png', '.jpg', '.exe', '.ini', 'reg', '.vbs', '.sys', '.dll']
    return remove_attributes_and_delete_files(target_dir, extensions)


def translate_tweaks(target_dir, dest_language='ru'):
    """
    Переводит названия файлов и папок с английского на указанный язык
    
    Args:
        target_dir (str): Целевая директория
        dest_language (str): Целевой язык перевода (по умолчанию 'ru' - русский)
    
    Returns:
        dict: Результат операции с количеством переименованных файлов/папок и ошибками
    """
    result = {
        'renamed_files': 0,
        'renamed_dirs': 0,
        'errors': []
    }
    
    if not os.path.exists(target_dir):
        result['errors'].append(f"Директория {target_dir} не существует")
        return result
    
    try:
        from googletrans import Translator
    except ImportError:
        result['errors'].append("Модуль googletrans не установлен. Установите его: pip install googletrans==4.0.0rc1")
        return result
    
    # Создаём объект для перевода
    translator = Translator()
    
    # Слова, которые не нужно переводить (регистронезависимо)
    PROTECTED_WORDS = {
        'ram', 'bios', 'nvidia', 'amd', 'hdcp', 'khz', 'cpu', 'gpu', 'ssd', 'hdd', 'reg', 'cmd',
        'usb', 'lan', 'wifi', 'bluetooth', 'dns', 'ip', 'tcp', 'udp', 'vpn', 'intel', 'bat', 'hyperv'
    }
    
    def translate_name(name):
        """Переводит название с защитой определенных слов"""
        try:
            # Разделяем имя и расширение
            name_without_ext, ext = os.path.splitext(name)
            
            # Разбиваем имя на части с сохранением разделителей
            parts = re.split(r'([_\-\s\.]+)', name_without_ext)
            
            translated_parts = []
            for part in parts:
                # Если это разделитель, оставляем как есть
                if re.match(r'[_\-\s\.]+', part):
                    translated_parts.append(part)
                # Если слово защищено, оставляем как есть
                elif part.lower() in PROTECTED_WORDS:
                    translated_parts.append(part)
                # Иначе переводим
                else:
                    try:
                        translation = translator.translate(part, dest=dest_language)
                        translated_parts.append(translation.text)
                    except Exception as e:
                        # Если не удалось перевести, оставляем как есть
                        translated_parts.append(part)
            
            # Собираем обратно имя и добавляем расширение
            translated_name = ''.join(translated_parts) + ext
            return translated_name
            
        except Exception as e:
            return name
    
    def should_translate(name):
        """Проверяет, нужно ли переводить имя"""
        # Проверяем, есть ли уже русские буквы в имени
        if re.search(r'[а-яА-Я]', name):
            return False
        
        # Проверяем, написано ли имя полностью капсом (аббревиатура)
        if name.isupper():
            return False
        
        # Разбиваем имя на части (без расширения) для проверки отдельных слов
        name_without_ext = os.path.splitext(name)[0]
        words = re.split(r'[_\-\s\.]', name_without_ext)
        
        # Если все слова капсом (кроме разделителей), не переводим
        all_caps = all(word.isupper() for word in words if word)
        if all_caps:
            return False
        
        return True
    
    # Обрабатываем все папки и файлы в каталоге
    # Сначала обрабатываем файлы, потом папки (в обратном порядке для корректного переименования)
    for root, dirs, files in os.walk(target_dir):
        # Обрабатываем файлы
        for file in files:
            # Проверяем расширение файла - если .pow, пропускаем
            if file.lower().endswith('.pow'):
                continue
            
            # Проверяем, нужно ли переводить это имя
            if not should_translate(file):
                continue
            
            # Переводим название файла
            new_file_name = translate_name(file)
            if new_file_name != file:
                try:
                    old_path = os.path.join(root, file)
                    new_path = os.path.join(root, new_file_name)
                    os.rename(old_path, new_path)
                    result['renamed_files'] += 1
                except Exception as e:
                    result['errors'].append(f"Ошибка при переименовании файла {file}: {e}")
    
    # Обрабатываем папки в обратном порядке (снизу вверх)
    for root, dirs, files in os.walk(target_dir, topdown=False):
        for dir_name in dirs:
            # Проверяем, нужно ли переводить это имя папки
            if not should_translate(dir_name):
                continue
            
            # Переводим название папки
            new_dir_name = translate_name(dir_name)
            if new_dir_name != dir_name:
                try:
                    old_path = os.path.join(root, dir_name)
                    new_path = os.path.join(root, new_dir_name)
                    os.rename(old_path, new_path)
                    result['renamed_dirs'] += 1
                except Exception as e:
                    result['errors'].append(f"Ошибка при переименовании папки {dir_name}: {e}")
    
    return result

