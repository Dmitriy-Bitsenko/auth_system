from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомная модель пользователя."""

    middle_name = models.CharField("Отчество", max_length=150, blank=True)
    email = models.EmailField("Email", unique=True)
    is_active = models.BooleanField("Активен", default=True)

    # Переопределяем — email вместо username
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    # Убираем username из полей
    username = None

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
