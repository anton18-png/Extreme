#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Конвертер PowerShell скриптов в Batch файлы
Поддерживает два типа конвертации:
1. Простые команды -> прямые PowerShell команды в bat
2. Сложные скрипты с функциями -> bat файл, запускающий ps1
"""

import os
import re
import sys
from pathlib import Path

class PS2BatchConverter:
    def __init__(self):
        self.stats = {
            'simple': 0,
            'complex': 0,
            'failed': 0
        }
    
    def is_simple_script(self, content):
        """
        Определяет, является ли скрипт простым (однострочные команды)
        или сложным (с функциями, параметрами и т.д.)
        """
        lines = content.split('\n')
        
        # Признаки сложного скрипта
        complex_patterns = [
            r'function\s+',           # Объявление функций
            r'param\s*\(',             # Параметры
            r'\[CmdletBinding\(',      # CmdletBinding
            r'^\s*if\s*\(',            # Условные операторы
            r'^\s*foreach\s*\(',       # Циклы
            r'^\s*while\s*\(',
            r'^\s*switch\s*\(',
            r'^\s*try\s*{',
            r'^\s*catch\s*{',
            r'^\s*class\s+',           # Классы
            r'^\s*enum\s+',            # Перечисления
        ]
        
        # Проверяем наличие признаков сложного скрипта
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            for pattern in complex_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    return False
        
        # Проверяем количество строк (если больше 20 - считаем сложным)
        non_comment_lines = [l for l in lines if l.strip() and not l.strip().startswith('#')]
        if len(non_comment_lines) > 20:
            return False
        
        return True
    
    def extract_powershell_commands(self, content):
        """
        Извлекает PowerShell команды из скрипта
        """
        commands = []
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Пропускаем комментарии и пустые строки
            if not line or line.startswith('#'):
                continue
            
            # Пропускаем объявления функций и параметров
            if re.match(r'^(function|param|\[CmdletBinding)', line, re.IGNORECASE):
                continue
            
            commands.append(line)
        
        return commands
    
    def create_simple_bat(self, ps_commands, output_path):
        """
        Создает bat файл с прямыми PowerShell командами
        """
        bat_content = [
            '@echo off',
            'chcp 65001 > nul',  # Поддержка UTF-8
            'set "PS=powershell.exe -ExecutionPolicy Bypass -NoProfile -Command"',
            ''
        ]
        
        for cmd in ps_commands:
            # Экранируем специальные символы для bat
            escaped_cmd = cmd.replace('"', '\\"')
            bat_content.append(f'%PS% "{escaped_cmd}"')
            bat_content.append('if %errorlevel% neq 0 (')
            bat_content.append(f'    echo [ERROR] Команда не выполнена: {cmd[:50]}...')
            bat_content.append('    pause')
            bat_content.append('    exit /b %errorlevel%')
            bat_content.append(')')
            bat_content.append('')
        
        bat_content.extend([
            'echo.',
            'echo ✅ Все команды выполнены',
            'pause'
        ])
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(bat_content))
    
    def create_complex_bat(self, ps_path, output_path):
        """
        Создает bat файл, который запускает PowerShell скрипт
        """
        ps_filename = os.path.basename(ps_path)
        bat_content = [
            '@echo off',
            'chcp 65001 > nul',
            '',
            f'echo 🔧 Запуск PowerShell скрипта: {ps_filename}',
            'echo.',
            '',
            ':: Проверка наличия PowerShell',
            'where powershell.exe > nul 2>&1',
            'if %errorlevel% neq 0 (',
            '    echo [ERROR] PowerShell не найден!',
            '    pause',
            '    exit /b 1',
            ')',
            '',
            ':: Запуск PowerShell скрипта',
            f'powershell.exe -ExecutionPolicy Bypass -NoProfile -File "%~dp0{ps_filename}" %*',
            '',
            'if %errorlevel% equ 0 (',
            f'    echo ✅ Скрипт {ps_filename} выполнен успешно',
            ') else (',
            f'    echo [ERROR] Ошибка при выполнении {ps_filename}',
            '    echo Код ошибки: %errorlevel%',
            ')',
            '',
            'echo.',
            'pause'
        ]
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(bat_content))
    
    def convert_file(self, ps_path, output_dir=None):
        """
        Конвертирует один PS файл в BAT
        """
        try:
            print(f"\n📄 Обработка: {ps_path}")
            
            # Читаем PS файл
            with open(ps_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Определяем имя выходного файла
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
                bat_path = os.path.join(output_dir, Path(ps_path).stem + '.bat')
            else:
                bat_path = Path(ps_path).with_suffix('.bat')
            
            # Проверяем тип скрипта
            if self.is_simple_script(content):
                print("   Тип: Простой скрипт (конвертация команд)")
                commands = self.extract_powershell_commands(content)
                self.create_simple_bat(commands, bat_path)
                self.stats['simple'] += 1
            else:
                print("   Тип: Сложный скрипт (создание запускателя)")
                self.create_complex_bat(ps_path, bat_path)
                self.stats['complex'] += 1
            
            print(f"   ✅ Создан: {bat_path}")
            return True
            
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
            self.stats['failed'] += 1
            return False
    
    def convert_directory(self, dir_path, output_dir=None, recursive=False):
        """
        Конвертирует все PS файлы в директории
        """
        dir_path = Path(dir_path)
        
        if not dir_path.exists():
            print(f"❌ Директория не найдена: {dir_path}")
            return
        
        # Поиск PS файлов
        pattern = '**/*.ps1' if recursive else '*.ps1'
        ps_files = list(dir_path.glob(pattern))
        
        if not ps_files:
            print(f"❌ PowerShell файлы не найдены в {dir_path}")
            return
        
        print(f"🔍 Найдено {len(ps_files)} PowerShell файлов")
        
        for ps_file in ps_files:
            self.convert_file(str(ps_file), output_dir)
        
        # Выводим статистику
        self.print_stats()
    
    def print_stats(self):
        """Вывод статистики конвертации"""
        print("\n" + "="*50)
        print("📊 СТАТИСТИКА КОНВЕРТАЦИИ:")
        print("="*50)
        print(f"✅ Простых скриптов: {self.stats['simple']}")
        print(f"🔧 Сложных скриптов: {self.stats['complex']}")
        print(f"❌ Ошибок: {self.stats['failed']}")
        print(f"📦 Всего обработано: {sum(self.stats.values())}")
        print("="*50)

def main():
    """Основная функция"""
    
    print("="*60)
    print("🔄 PowerShell to Batch Converter v1.0")
    print("="*60)
    
    converter = PS2BatchConverter()
    
    # Проверяем аргументы командной строки
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
        output_dir = sys.argv[2] if len(sys.argv) > 2 else None
        
        if os.path.isdir(input_path):
            recursive = '--recursive' in sys.argv or '-r' in sys.argv
            converter.convert_directory(input_path, output_dir, recursive)
        else:
            converter.convert_file(input_path, output_dir)
            converter.print_stats()
        return
    
    # Интерактивный режим
    while True:
        print("\n📋 Выберите действие:")
        print("1. Конвертировать один файл")
        print("2. Конвертировать все .ps1 файлы в папке")
        print("3. Выход")
        
        choice = input("👉 Ваш выбор (1-3): ").strip()
        
        if choice == '1':
            ps_path = input("📂 Путь к PS файлу: ").strip()
            if ps_path:
                output_dir = input("📁 Папка для сохранения (Enter - та же папка): ").strip()
                if not output_dir:
                    output_dir = None
                converter.convert_file(ps_path, output_dir)
                converter.print_stats()
        
        elif choice == '2':
            dir_path = input("📂 Путь к папке: ").strip()
            if dir_path:
                recursive = input("📁 Обрабатывать подпапки? (y/n): ").strip().lower() == 'y'
                output_dir = input("📁 Папка для сохранения (Enter - та же папка): ").strip()
                if not output_dir:
                    output_dir = None
                converter.convert_directory(dir_path, output_dir, recursive)
        
        elif choice == '3':
            print("👋 До свидания!")
            break
        
        else:
            print("❌ Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()