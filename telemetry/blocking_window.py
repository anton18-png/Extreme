import tkinter as tk
from tkinter import messagebox

def show_blocking_message():
    """Показывает сообщение о блокировке в графическом окне"""
    root = tk.Tk()
    root.withdraw()  # Скрываем основное окно
    
    message = f"ВНИМАНИЕ: Вы заблокированы!!!\n\n"
    message += f"Возможные причины:\n"
    message += f"- Попытка взлома программы\n"
    message += f"- Попытка использования нелегальных ключей\n"
    message += f"- Попытка использования нелегальных модификаций\n"
    message += f"- Попытка использования нелегальных обновлений\n"
    message += f"- Попытка использования нелегальных расширений\n"
    message += f"- Попытка использования нелегальных плагинов\n\n"
    message += f"Если вы не виноваты, пожалуйста, обратитесь в тех. поддержку.\n"
    message += f"https://t.me/all_tweaker\n"
    
    messagebox.showerror("Extreme - Блокировка", message)
    root.destroy() 