import logging


logger = logging.getLogger("Системный")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    fmt="[{asctime}] [{levelname:^8}] [{name}] {message}",
    datefmt="%Y-%m-%d %H:%M:%S",
    style="{",
)

# Настройка для файла
file_handler = logging.FileHandler("api/log/api.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Настройка для консоли
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

# добавление обработчика к логгеру
logger.addHandler(file_handler)
logger.addHandler(console_handler)
