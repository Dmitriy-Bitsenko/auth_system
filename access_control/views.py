from rest_framework import generics, permissions

from .models import AccessRoleRule, BusinessElement, Role, UserRole
from .serializers import (
    AccessRoleRuleSerializer,
    BusinessElementSerializer,
    RoleSerializer,
    UserRoleSerializer,
)


class IsAdmin(permissions.BasePermission):
    """Разрешение только для пользователей с ролью admin."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return UserRole.objects.filter(
            user=request.user, role__name="admin"
        ).exists()


class RoleListCreateView(generics.ListCreateAPIView):
    """GET/POST — список ролей и создание новых (admin)."""

    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdmin]


class RoleDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET/PUT/DELETE — одна роль (admin)."""

    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdmin]


class BusinessElementListCreateView(generics.ListCreateAPIView):
    """GET/POST — список бизнес-объектов (admin)."""

    queryset = BusinessElement.objects.all()
    serializer_class = BusinessElementSerializer
    permission_classes = [IsAdmin]


class BusinessElementDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET/PUT/DELETE — один бизнес-объект (admin)."""

    queryset = BusinessElement.objects.all()
    serializer_class = BusinessElementSerializer
    permission_classes = [IsAdmin]



class AccessRuleListCreateView(generics.ListCreateAPIView):
    """GET/POST — список правил доступа (admin)."""

    queryset = AccessRoleRule.objects.all()
    serializer_class = AccessRoleRuleSerializer
    permission_classes = [IsAdmin]


class AccessRuleDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET/PUT/DELETE — одно правило (admin)."""

    queryset = AccessRoleRule.objects.all()
    serializer_class = AccessRoleRuleSerializer
    permission_classes = [IsAdmin]


class UserRoleListCreateView(generics.ListCreateAPIView):
    """GET/POST — роли пользователей (admin)."""

    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [IsAdmin]


class UserRoleDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET/PUT/DELETE — роль пользователя (admin)."""

    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [IsAdmin]
