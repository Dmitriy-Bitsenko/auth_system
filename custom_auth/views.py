from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import LoginSerializer, RegisterSerializer


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
    Требует авторизации (токен).
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return Response(
            {"message": "Успешный выход"},
            status=status.HTTP_200_OK,
        )
