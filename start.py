import sys
import os

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    print("Running in a PyInstaller bundle")
else:
    print("Running in a normal Python environment")

print("\nStarting Extreme...")

print("Setting up exception handler...")

print("Starting main program...")
try:
    print("Importing main module...")
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        import main
    else:
        import main
    print("Main module imported successfully")

except Exception as e:
    print(f"Error in main program: {e}")
    import traceback
    traceback.print_exc()
    raise
