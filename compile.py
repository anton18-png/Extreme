import PyInstaller.__main__
import os
import shutil

# Путь к основному файлу
main_script = 'start.py'

# Путь к иконке (если есть)
icon_path = 'icon.ico'  # Укажите путь к иконке, если она есть

# Формируем команду для PyInstaller
pyinstaller_args = [
    main_script,
    '--name=dist',
    '--onefile',  # Создаем один исполняемый файл
    '--noconsole',  # Скрываем консоль при запуске
    '--add-data=tweaks;tweaks',
    '--add-data=Utils;Utils',
    # '--add-data=theme.ini;.',
    # '--add-data=system_info.py;.',
    '--add-data=tabs_beta.py;.',
    '--add-data=main.py;.',
    '--clean',  # Очищаем предыдущие сборки
    '--noconfirm',  # Не спрашивать подтверждения
]

# Добавляем иконку, если она указана
if icon_path:
    pyinstaller_args.append(f'--icon={icon_path}')

# Запускаем компиляцию
PyInstaller.__main__.run(pyinstaller_args)

print("Компиляция завершена! Исполняемый файл находится в папке dist/") 