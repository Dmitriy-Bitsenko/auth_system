from django.contrib.auth.models import AbstractUser
from django.db import models

import bcrypt


class User(AbstractUser):
    """Кастомная модель пользователя."""

    middle_name = models.CharField("Отчество", max_length=150, blank=True)
    email = models.EmailField("Email", unique=True)
    is_active = models.BooleanField("Активен", default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    username = None

    def check_password(self, raw_password):
        """
        Проверяем пароль с помощью bcrypt.
        """
        password_bytes = raw_password.encode("utf-8")
        hash_str = self.password
        if not hash_str.startswith("bcrypt$"):
            return False
        parts = hash_str.split("$")
        stored_hash = f"${parts[1]}${parts[2]}${parts[3]}".encode("utf-8")
        return bcrypt.checkpw(password_bytes, stored_hash)

    def set_password(self, raw_password):
        """
        Хешируем пароль с помощью bcrypt.
        """
        password_bytes = raw_password.encode("utf-8")
        password_hash = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        hash_str = password_hash.decode("utf-8")
        parts = hash_str.split("$")
        self.password = f"bcrypt${parts[1]}${parts[2]}${parts[3]}"

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class BlacklistedToken(models.Model):
    """
    Модель для хранения заблокированных (logout) токенов.
    После logout токен попадает сюда и больше не принимается.
    """

    token = models.TextField("Токен", unique=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="blacklisted_tokens",
        verbose_name="Пользователь",
    )
    expires_at = models.DateTimeField("Истекает", help_text="Когда токен истечёт")
    created_at = models.DateTimeField("Создан", auto_now_add=True)

    class Meta:
        verbose_name = "Заблокированный токен"
        verbose_name_plural = "Заблокированные токены"

    def __str__(self):
        return f"Token для {self.user.email} (истекает: {self.expires_at})"
