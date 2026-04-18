from rest_framework import serializers

from .models import User
from .utils import generate_token


class ProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор профиля пользователя.
    Позволяет просматривать и обновлять: first_name, last_name, middle_name, email.
    Для смены пароля есть отдельное поле new_password.
    """

    new_password = serializers.CharField(
        write_only=True, required=False, min_length=8
    )
    new_password_confirm = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "middle_name",
            "email",
            "new_password",
            "new_password_confirm",
        ]
        read_only_fields = ["id", "email"]

    def validate(self, data):
        """
        Проверяем, что новые пароли совпадают (если указаны).
        """
        new_password = data.get("new_password")
        new_password_confirm = data.get("new_password_confirm")

        if new_password or new_password_confirm:
            if not new_password or not new_password_confirm:
                raise serializers.ValidationError(
                    {"new_password": "Укажите оба поля: new_password и new_password_confirm"}
                )
            if new_password != new_password_confirm:
                raise serializers.ValidationError(
                    {"new_password_confirm": "Новые пароли не совпадают"}
                )

        if "email" in data and data["email"] != self.instance.email:
            if User.objects.filter(email=data["email"]).exists():
                raise serializers.ValidationError(
                    {"email": "Этот email уже занят"}
                )

        return data

    def update(self, instance, validated_data):
        """
        Обновляем профиль. Если указан new_password — хешируем и сохраняем.
        """
        new_password = validated_data.pop("new_password", None)
        validated_data.pop("new_password_confirm", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)


        if new_password:
            instance.set_password(new_password)

        instance.save()
        return instance


class DeleteAccountSerializer(serializers.Serializer):
    """
    Сериализатор удаления аккаунта.
    Требует подтверждения пароля для безопасности.
    """

    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        user = self.context["request"].user
        password = data["password"]


        if not user.check_password(password):
            raise serializers.ValidationError({"password": "Неверный пароль"})

        return data

    def save(self):
        """
        Мягкое удаление: ставим is_active=False.
        """
        user = self.context["request"].user
        user.is_active = False
        user.save()
        return user


class RegisterSerializer(serializers.Serializer):
    """
    Сериализатор регистрации.
    Здесь мы описываем какие данные принимаем и как валидируем.
    """


    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    middle_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)  # write_only = не показываем в ответе
    password_confirm = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Проверяем, что пароли совпадают.
        data — это dict с полями из запроса:
            {"first_name": "...", "email": "...", "password": "...", ...}
        """
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError({"password_confirm": "Пароли не совпадают"})


        if User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError({"email": "Этот email уже занят"})

        return data

    def create(self, validated_data):
        """
        Создаём пользователя в БД.
        validated_data — данные, прошедшие validate() (без password_confirm).
        """
        validated_data.pop("password_confirm")  

        user = User(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            middle_name=validated_data.get("middle_name", ""),
            email=validated_data["email"],
        )
        user.set_password(validated_data["password"])
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    """
    Сериализатор логина.
    Проверяем email + пароль, возвращаем JWT токен.
    """

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data["email"]
        password = data["password"]


        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "Неверный email или пароль"})


        if not user.is_active:
            raise serializers.ValidationError({"email": "Аккаунт заблокирован"})


        if not user.check_password(password):
            raise serializers.ValidationError({"email": "Неверный email или пароль"})


        token = generate_token(user)

        return {
            "token": token,
            "user": {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
            },
        }
