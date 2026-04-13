import bcrypt
from rest_framework import serializers

from .models import User
from .utils import generate_token


class RegisterSerializer(serializers.Serializer):
    """
    Сериализатор регистрации.
    Здесь мы описываем какие данные принимаем и как валидируем.
    """

    # Поля, которые ждём от клиента в POST-запросе
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    middle_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)  # write_only = не показываем в ответе
    password_confirm = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Проверяем, что пароли совпадают.
        data — это dict с полями из запроса:
            {"first_name": "...", "email": "...", "password": "...", ...}
        """
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError({"password_confirm": "Пароли не совпадают"})

        # Проверяем, нет ли уже такого email
        if User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError({"email": "Этот email уже занят"})

        return data

    def create(self, validated_data):
        """
        Создаём пользователя в БД.
        validated_data — данные, прошедшие validate() (без password_confirm).
        """
        validated_data.pop("password_confirm")  # убираем — он не нужен для создания

        # Хешируем пароль через bcrypt
        password_bytes = validated_data["password"].encode("utf-8")
        password_hash = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

        # Создаём пользователя. set_unusable_password() отключаем стандартный
        # Django-хеш, потом сохраним свой bcrypt-хеш напрямую
        user = User(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            middle_name=validated_data.get("middle_name", ""),
            email=validated_data["email"],
        )
        user.set_unusable_password()  # отключаем стандартный Django-пароль
        user.save()

        # Сохраняем bcrypt-хеш напрямую в поле password
        # Django хранит пароли в формате: <алгоритм>$<соли>$<хеш>
        # Нам нужно разобрать bcrypt-хеш на части
        hash_str = password_hash.decode("utf-8")
        # bcrypt формат: $2b$12$salt+hash
        parts = hash_str.split("$")
        # parts = ['', '2b', '12', 'salt+hash']
        django_format = f"bcrypt${parts[1]}${parts[3]}"
        user.password = django_format
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

        # Ищем пользователя по email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "Неверный email или пароль"})

        # Проверяем пароль
        if not user.is_active:
            raise serializers.ValidationError({"email": "Аккаунт заблокирован"})

        # bcrypt.checkpw сравнивает введённый пароль с хешем из БД
        # Django хранит: bcrypt$2b$salt+hash
        stored_password = user.password  # "bcrypt$2b$xxxxx"

        # Разбираем django-формат обратно в bcrypt-строку
        parts = stored_password.split("$")
        # parts = ["bcrypt", "2b", "salt+hash"]
        bcrypt_hash = f"${parts[1]}${parts[2]}"

        if not bcrypt.checkpw(password.encode("utf-8"), bcrypt_hash.encode("utf-8")):
            raise serializers.ValidationError({"email": "Неверный email или пароль"})

        # Генерируем JWT-токен
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
