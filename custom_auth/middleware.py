from django.contrib.auth.models import AnonymousUser

from .utils import get_user_from_token


class JWTAuthenticationMiddleware:
    """
    Middleware для извлечения пользователя из JWT-токена.

    Сохраняет пользователя в request._jwt_user.
    DRF authentication class использует это значение.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.headers.get("Authorization", "")

        if auth_header.startswith("Bearer "):
            token = auth_header.split(" ", 1)[1]
            user = get_user_from_token(token)
            request._jwt_user = user if user else AnonymousUser()
        else:
            request._jwt_user = AnonymousUser()

        return self.get_response(request)
