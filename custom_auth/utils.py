import datetime

import jwt
from django.conf import settings
from django.utils import timezone

from .models import BlacklistedToken, User


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
        "exp": timezone.now() + datetime.timedelta(hours=settings.JWT_EXPIRE_HOURS),
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


def is_token_blacklisted(token):
    """
    Проверяем, находится ли токен в блэклисте.
    """
    return BlacklistedToken.objects.filter(token=token).exists()


def blacklist_token(token, user):
    """
    Добавляем токен в блэклист.
    """
    payload = decode_token(token)
    expires_at = timezone.make_aware(datetime.datetime.fromtimestamp(payload["exp"]))
    BlacklistedToken.objects.create(
        token=token,
        user=user,
        expires_at=expires_at,
    )


def get_user_from_token(token):
    """
    Извлекаем пользователя из токена.

    1. Проверяем, не в блэклисте ли токен
    2. Декодируем токен → получаем user_id
    3. Ищем пользователя в БД
    4. Проверяем, что он активен (is_active=True)

    Возвращает User или None.
    """
    try:
        if is_token_blacklisted(token):
            return None

        payload = decode_token(token)
        user = User.objects.get(id=payload["user_id"], is_active=True)
        return user
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
        return None
