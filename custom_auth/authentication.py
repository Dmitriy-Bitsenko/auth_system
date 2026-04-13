from rest_framework.authentication import BaseAuthentication


class JWTAuthentication(BaseAuthentication):
    """
    DRF authentication class — берёт пользователя из request._jwt_user.

    Middleware уже декодировал токен и сохранил пользователя.
    """

    def authenticate(self, request):
        user = getattr(request, "_jwt_user", None)
        if user and not user.is_anonymous:
            return (user, None)
        return None
