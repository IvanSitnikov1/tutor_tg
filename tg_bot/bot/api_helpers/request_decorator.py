"""
Модуль содержит декоратор для обертки запросов к API бота. Забирает из переданной функции url, метод и
данные, если требуется и вызывает нужный запрос к API. Возвращает JSON с ответом
"""
import aiohttp


def request_decorator(func):
    async def wrapper(*args, **kwargs):
        url, method, data = await func(*args, **kwargs)
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, json=data) as response:
                return await response.json()
    return wrapper
