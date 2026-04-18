from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import (
    DeleteAccountSerializer,
    LoginSerializer,
    ProfileSerializer,
    RegisterSerializer,
)
from .utils import blacklist_token


class RegisterView(generics.CreateAPIView):
    """
    Эндпоинт регистрации.

    POST /api/auth/register/
    """

    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Пользователь создан"},
            status=status.HTTP_201_CREATED,
        )


class LoginView(generics.GenericAPIView):
    """
    Эндпоинт логина.

    POST /api/auth/login/
    """

    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    """
    Эндпоинт логаута.

    POST /api/auth/logout/
    Требует авторизации (токен). Добавляет токен в блэклист.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        
        auth_header = request.headers.get("Authorization", "")
        token = auth_header.replace("Bearer ", "") if auth_header.startswith("Bearer ") else None

        if token:
            
            blacklist_token(token, request.user)

        return Response(
            {"message": "Успешный выход"},
            status=status.HTTP_200_OK,
        )


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    Эндпоинт получения и обновления профиля.

    GET  /api/auth/profile/  — получить данные профиля
    PUT/PATCH /api/auth/profile/ — обновить профиль (имя, email, пароль)
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        """
        Возвращаем текущего авторизованного пользователя.
        """
        return self.request.user


class DeleteAccountView(generics.GenericAPIView):
    """
    Эндпоинт удаления аккаунта (мягкое).

    POST /api/auth/delete-account/
    Требует подтверждения пароля. Ставит is_active=False.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = DeleteAccountSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Аккаунт успешно удалён"},
            status=status.HTTP_200_OK,
        )
