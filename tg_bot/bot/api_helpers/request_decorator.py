import aiohttp


def request_decorator(func):
    async def wrapper(*args, **kwargs):
        url, method, data = await func(*args, **kwargs)
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, json=data) as response:
                return await response.json()
    return wrapper
