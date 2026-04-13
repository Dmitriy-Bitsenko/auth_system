from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import LoginSerializer, RegisterSerializer


class RegisterView(generics.CreateAPIView):
    """
    Эндпоинт регистрации.

    POST /api/auth/register/
    """

    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Пользователь создан"},
            status=status.HTTP_201_CREATED
        )


class LoginView(generics.GenericAPIView):
    """
    Эндпоинт логина.

    POST /api/auth/login/
    {
        "email": "ivan@mail.ru",
        "password": "secret123"
    }

    Возвращаем:
        200 — {"token": "...", "user": {...}}
        400 — {"email": "Неверный email или пароль"}
    """

    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # serializer.validate() уже вернул token и user
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
