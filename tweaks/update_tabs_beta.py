#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт обновления tabs_beta.py на основе реальной структуры папок в tweaks/.

Сканирует подпапки каждого раздела (Главная, Оптимизация, Драйверы, Электропитание,
Исправления, Очистка, Настройки) и генерирует соответствующие словари:
  tabs_main, tabs, tabs_1, tabs_2, tabs_3, tabs_4, tabs_6

Ручные словари (tabs_uninstall, tabs_5, tabs_qqnwr, tabs_mini, tabs_update, __all__)
сохраняются из существующего файла без изменений.
"""

import io
import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # tweaks/
PROJECT_DIR = os.path.dirname(BASE_DIR)                 # Extreme/
TABS_BETA_PATH = os.path.join(BASE_DIR, 'tabs_beta.py')

EXTENSIONS = ['.bat', '.cmd', '.ps1', '.exe', '.pow']
EXCLUDE_FILES = ['PowerRun.exe', 'pssuspend.exe', 'TI.exe']
EXCLUDE_DIRS = {'tweaks', 'Source', 'Utils', '__pycache__', 'others', '__pycache__'}

# Сопоставление названий папок в tweaks/ с именами переменных словарей
FOLDER_TO_DICT = {
    'Главная':       'tabs_main',
    'Оптимизация':   'tabs',
    'Драйверы':      'tabs_1',
    'Электропитание': 'tabs_2',
    'Исправления':    'tabs_3',
    'Очистка':        'tabs_4',
    'Настройки':      'tabs_6',
}

# Имена ручных словарей, которые НЕ нужно генерировать
MANUAL_DICTS = {'tabs_uninstall', 'tabs_5', 'tabs_qqnwr', 'tabs_mini', 'tabs_update', '__all__'}

# --- Сканирование файлов ---

def get_files_by_subdir(parent_dir):
    """
    Для папки parent_dir возвращает словарь:
      имя_подпапки -> [список относительных путей ко всем файлам с extensions]
    """
    result = {}
    if not os.path.isdir(parent_dir):
        return result

    # Получаем список непосредственных подпапок (исключая скрытые)
    subdirs = []
    for entry in os.scandir(parent_dir):
        if entry.is_dir() and not entry.name.startswith('.'):
            subdirs.append(entry.name)
    subdirs.sort()

    for sub in subdirs:
        sub_path = os.path.join(parent_dir, sub)
        files = []
        for root, _, fnames in os.walk(sub_path):
            # Пропускаем исключённые директории
            rel = os.path.relpath(root, parent_dir)
            parts = rel.split(os.sep)
            if any(p in EXCLUDE_DIRS for p in parts):
                continue
            for fname in fnames:
                if fname in EXCLUDE_FILES:
                    continue
                ext = os.path.splitext(fname)[1].lower()
                if ext in EXTENSIONS:
                    # Путь относительно подпапки (ключа словаря)
                    full_rel = os.path.relpath(os.path.join(root, fname), sub_path)
                    files.append(full_rel)
        files.sort()
        if files:
            result[sub] = files

    return result


# --- Генерация Python-кода словаря ---

def format_list(items):
    """Форматирует список строк как Python-литерал, разбивая на строки ~100 символов."""
    if not items:
        return '[]'
    buf = io.StringIO()
    buf.write('[')
    line_start = True
    line = ''
    for i, item in enumerate(items):
        # Экранируем кавычки и обратные слеши
        escaped = item.replace('\\', '\\\\').replace("'", "\\'")
        token = f"'{escaped}'"
        if i > 0:
            # Проверяем, поместится ли следующий элемент в строку < 120 символов
            if len(line) + len(token) + 2 > 110:
                buf.write(line + ',\n')
                line = '        ' + token
            else:
                line += ', ' + token
        else:
            line = '    ' + token
    buf.write(line + ']')
    return buf.getvalue()


def generate_dict_code(dict_name, data):
    """Генерирует полный код Python-словаря."""
    buf = io.StringIO()
    buf.write(f'{dict_name} = {{\n')
    keys = sorted(data.keys())
    for key in keys:
        items = data[key]
        items_str = format_list(items)
        # экранируем апострофы в ключе
        escaped_key = key.replace('\\', '\\\\').replace("'", "\\'")
        buf.write(f"    '{escaped_key}': {items_str},\n")
    buf.write('}\n\n')
    return buf.getvalue()


# --- Чтение и сохранение ручных словарей ---

def read_manual_sections(filepath):
    """
    Читает tabs_beta.py и находит ручные словари.
    Возвращает словарь имя_переменной -> (start_line, end_line).
    А также возвращает содержимое до первого авто-словаря.
    """
    if not os.path.exists(filepath):
        print(f"  [предупреждение] {filepath} не найден, ручные словари будут пустыми")
        return {}, '', ''
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Находим все присваивания словарей: var_name = {
    pattern = re.compile(r'^(\w+)\s*=\s*\{', re.MULTILINE)
    matches = list(pattern.finditer(content))

    sections = {}
    for i, m in enumerate(matches):
        var_name = m.group(1)
        if var_name in MANUAL_DICTS:
            # Находим закрывающую скобку на правильном уровне вложенности
            start = m.start()
            # Открывающая скобка — последний символ match
            brace_start = m.end() - 1
            depth = 1
            pos = brace_start + 1
            while pos < len(content) and depth > 0:
                if content[pos] == '{':
                    depth += 1
                elif content[pos] == '}':
                    depth -= 1
                pos += 1
            end = pos
            sections[var_name] = (start, end)

    # Содержимое до первого словаря
    preamble = ''
    if matches:
        preamble = content[:matches[0].start()]

    return sections, preamble, content


def preserve_manual_dicts(content, manual_sections):
    """
    Извлекает текст ручных словарей из содержимого.
    Возвращает список строк (кода).
    """
    parts = []
    for var_name in sorted(MANUAL_DICTS, key=lambda v: v != '__all__' if v == '__all__' else 0):
        if var_name in manual_sections:
            start, end = manual_sections[var_name]
            part = content[start:end]
            # Удаляем trailing '}' если с новой строки
            parts.append((var_name, part))
        else:
            # Если ручного словаря нет в файле, создаём пустой
            if var_name == '__all__':
                parts.append((var_name,
                    "__all__ = ['tabs_main', 'tabs', 'tabs_1', 'tabs_2', 'tabs_3', "
                    "'tabs_4', 'tabs_5', 'tabs_6', 'tabs_update']\n"))
            else:
                parts.append((var_name, f'{var_name} = {{}}\n\n'))
    return parts


# --- Основная логика ---

def main():
    # 1. Сканируем все папки
    all_data = {}
    for folder_name, dict_name in FOLDER_TO_DICT.items():
        folder_path = os.path.join(BASE_DIR, folder_name)
        data = get_files_by_subdir(folder_path)
        all_data[dict_name] = data
        print(f"  {folder_name}/ -> {dict_name}: {len(data)} групп, "
              f"{sum(len(v) for v in data.values())} файлов")

    # 2. Читаем существующий файл для сохранения ручных словарей
    manual_sections, preamble, old_content = read_manual_sections(TABS_BETA_PATH)
    if not manual_sections:
        # Fallback: читаем из корневого tabs_beta.py
        root_tabs = os.path.join(PROJECT_DIR, 'tabs_beta.py')
        manual_sections, preamble, old_content = read_manual_sections(root_tabs)

    # 3. Генерируем новый код
    new_lines = []
    # Сначала все авто-словари в правильном порядке
    auto_order = ['tabs_main', 'tabs', 'tabs_1', 'tabs_2', 'tabs_3', 'tabs_4', 'tabs_6']
    for dict_name in auto_order:
        data = all_data.get(dict_name, {})
        code = generate_dict_code(dict_name, data)
        new_lines.append(code)

    # 4. Добавляем ручные словари
    manual_parts = preserve_manual_dicts(old_content, manual_sections)
    for var_name, code in manual_parts:
        new_lines.append(code + '\n')

    # 5. Записываем
    output = ''.join(new_lines)
    with open(TABS_BETA_PATH, 'w', encoding='utf-8') as f:
        f.write(output)
    print(f"\nГотово! Обновлён {TABS_BETA_PATH}")
    print(f"Авто-словарей: {len(auto_order)}, ручных: {len(manual_parts)}")


if __name__ == '__main__':
    main()
