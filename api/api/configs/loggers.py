import logging


system_logger = logging.getLogger("Системный")
system_logger.setLevel(logging.DEBUG)

user_logger = logging.getLogger("Пользовательский")
user_logger.setLevel(logging.DEBUG)

# Настраиваем форматтер
formatter = logging.Formatter(
    fmt="[{asctime}] [{levelname:^8}] [{name}] {message}",
    datefmt="%Y-%m-%d %H:%M:%S",
    style="{",
)

# Настройка для файла
file_handler = logging.FileHandler("api/log/api.log")
file_handler.setLevel(logging.DEBUG)  # Уровень для файла
file_handler.setFormatter(formatter)

# Настройка для консоли
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Уровень для консоли
console_handler.setFormatter(formatter)

# добавление обработчика к логгеру
system_logger.addHandler(file_handler)
system_logger.addHandler(console_handler)

user_logger.addHandler(file_handler)
user_logger.addHandler(console_handler)
