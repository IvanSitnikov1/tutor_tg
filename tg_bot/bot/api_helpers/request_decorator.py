import aiohttp


def request_decorator(func):
    async def wrapper(*args, **kwargs):
        url, method, data, expected_status = await func(*args, **kwargs)
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, json=data) as response:
                if response.status == expected_status:
                    response_json = await response.json()
                    return response_json['data']
                return None
    return wrapper
