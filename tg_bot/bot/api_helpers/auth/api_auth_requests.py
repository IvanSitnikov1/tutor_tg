from config import API_URL
from bot.api_helpers.request_decorator import request_decorator


@request_decorator
async def create_user_request(user_type: str, username: str, tg_id: int, teacher_id: int = None):
    url = f'{API_URL}/users/add_user_{user_type}'
    data = {
        'username': username,
        'tg_id': tg_id,
    }
    if teacher_id:
        data['teacher_id'] = teacher_id
    return url, 'POST', data, 201
