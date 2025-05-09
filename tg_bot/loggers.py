import logging
import sys
from logging.handlers import RotatingFileHandler

# ANSI-коды цветов
LOG_COLORS = {
    'DEBUG': '\033[36m',    # Cyan
    'INFO': '\033[32m',     # Green
    'WARNING': '\033[33m',  # Yellow
    'ERROR': '\033[31m',    # Red
    'CRITICAL': '\033[1;31m',  # Bold Red
}
RESET_COLOR = '\033[0m'


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        log_color = LOG_COLORS.get(record.levelname, '')
        message = super().format(record)
        return f"{log_color}{message}{RESET_COLOR}"


# === Создание логгера ===
logger = logging.getLogger("bot_logger")
logger.setLevel(logging.DEBUG)

# --- Консольный хендлер с цветами ---
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)

console_format = ColoredFormatter(
    '[%(asctime)s] [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
console_handler.setFormatter(console_format)

# --- Файловый хендлер с ротацией ---
file_handler = RotatingFileHandler(
    filename='bot.log',
    maxBytes=10 * 1024 * 1024,  # 10 МБ
    backupCount=3,
    encoding='utf-8'
)
file_handler.setLevel(logging.INFO)

file_format = logging.Formatter(
    '[%(asctime)s] [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
file_handler.setFormatter(file_format)

# --- Добавление хендлеров ---
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# === Подключаем хендлеры к логгерам Aiogram ===
lib_logger = logging.getLogger("aiogram")
lib_logger.setLevel(logging.INFO)
lib_logger.addHandler(console_handler)
lib_logger.addHandler(file_handler)
