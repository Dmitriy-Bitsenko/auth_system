from rest_framework import permissions

from .models import AccessRoleRule, UserRole


class HasAccess(permissions.BasePermission):
    """
    Проверка прав доступа для бизнес-эндпоинтов.

    Использование:
        permission_classes = [HasAccess]
        required_permission = 'read'  # или 'create', 'update', 'delete'
        business_element = 'users'   # имя элемента из БД
    """

    required_permission = None
    business_element = None

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        # Получаем роли пользователя
        user_roles = UserRole.objects.filter(user=request.user).values_list(
            "role_id", flat=True
        )

        if not user_roles:
            return False

        # Проверяем есть ли у хотя бы одной роли нужное право
        return AccessRoleRule.objects.filter(
            role_id__in=user_roles,
            element__name=self.business_element,
            **{f"{self.required_permission}_perm": True},
        ).exists()


class CanRead(HasAccess):
    required_permission = "read"


class CanCreate(HasAccess):
    required_permission = "create"


class CanUpdate(HasAccess):
    required_permission = "update"


class CanDelete(HasAccess):
    required_permission = "delete"
