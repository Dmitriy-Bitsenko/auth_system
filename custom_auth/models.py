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
