import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = "user_data//logs"

class Logger:
    def __init__(self, name="Extreme"):
        self.enabled = True
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        os.makedirs(LOG_DIR, exist_ok=True)
        log_file = os.path.join(LOG_DIR, f"{name}.log")
        handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3, encoding="utf-8")
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def set_enabled(self, enabled):
        self.enabled = enabled

    def log_info(self, message):
        if self.enabled:
            self.logger.info(message)

    def log_error(self, message, exc_info=False):
        if self.enabled:
            self.logger.error(message, exc_info=exc_info)

    def log_warning(self, message):
        if self.enabled:
            self.logger.warning(message)

    def log_settings_change(self, setting, value=None):
        if self.enabled:
            if value is not None:
                self.logger.info(f"Settings changed: {setting} = {value}")
            else:
                self.logger.info(f"Settings changed: {setting}")

    def log_tweak_execution(self, tweak_name, status=None):
        if self.enabled:
            if status:
                self.logger.info(f"Tweak executed: {tweak_name} - {status}")
            else:
                self.logger.info(f"Tweak executed: {tweak_name}")

    def log_program_start(self):
        if self.enabled:
            self.logger.info("Program started")
