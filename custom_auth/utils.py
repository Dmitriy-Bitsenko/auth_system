import datetime

import jwt
from django.conf import settings

from .models import User


def generate_token(user):
    """
    Создаём JWT-токен для пользователя.

    payload — словарь с данными:
        user_id — ID пользователя
        exp — когда токен истечёт (UTC)

    jwt.encode() превращает payload в строку и подписывает секретом.
    """
    payload = {
        "user_id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=settings.JWT_EXPIRE_HOURS),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_token(token):
    """
    Декодируем JWT-токен.

    jwt.decode() проверяет:
        - подпись (секрет совпадает?)
        - срок действия (exp не истёк?)

    Если всё ок — возвращает payload dict.
    Если нет — выбрасывает исключение.
    """
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])


def get_user_from_token(token):
    """
    Извлекаем пользователя из токена.

    1. Декодируем токен → получаем user_id
    2. Ищем пользователя в БД
    3. Проверяем, что он активен (is_active=True)

    Возвращает User или None.
    """
    try:
        payload = decode_token(token)
        user = User.objects.get(id=payload["user_id"], is_active=True)
        return user
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
        return None
