from django.db import models
from django.conf import settings


class Role(models.Model):
    """Роль пользователя (admin, manager, viewer и т.д.)."""

    name = models.CharField("Название роли", max_length=100, unique=True)
    description = models.TextField("Описание", blank=True)

    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"

    def __str__(self):
        return self.name


class BusinessElement(models.Model):
    """Бизнес-объект, к которому нужен доступ (users, orders, reports)."""

    name = models.SlugField("Название (slug)", max_length=100, unique=True)
    description = models.TextField("Описание", blank=True)

    class Meta:
        verbose_name = "Бизнес-объект"
        verbose_name_plural = "Бизнес-объекты"

    def __str__(self):
        return self.name


class UserRole(models.Model):
    """Связь пользователя с ролью (many-to-many через промежуточную таблицу)."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_roles",
        verbose_name="Пользователь",
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name="user_roles",
        verbose_name="Роль",
    )

    class Meta:
        verbose_name = "Роль пользователя"
        verbose_name_plural = "Роли пользователей"
        unique_together = ("user", "role")

    def __str__(self):
        return f"{self.user.email} → {self.role.name}"


class AccessRoleRule(models.Model):
    """Правила доступа: какая роль что может делать с бизнес-объектом."""

    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name="access_rules",
        verbose_name="Роль",
    )
    element = models.ForeignKey(
        BusinessElement,
        on_delete=models.CASCADE,
        related_name="access_rules",
        verbose_name="Бизнес-объект",
    )

    read_perm = models.BooleanField("Чтение", default=False)
    read_all_perm = models.BooleanField("Чтение всех", default=False)
    create_perm = models.BooleanField("Создание", default=False)
    update_perm = models.BooleanField("Редактирование", default=False)
    update_all_perm = models.BooleanField("Редактирование всех", default=False)
    delete_perm = models.BooleanField("Удаление", default=False)
    delete_all_perm = models.BooleanField("Удаление всех", default=False)

    class Meta:
        verbose_name = "Правило доступа"
        verbose_name_plural = "Правила доступа"
        unique_together = ("role", "element")

    def __str__(self):
        return f"{self.role.name} → {self.element.name}"
