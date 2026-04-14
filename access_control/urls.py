from django.urls import path

from .views import (
    AccessRuleDetailView,
    AccessRuleListCreateView,
    BusinessElementDetailView,
    BusinessElementListCreateView,
    RoleDetailView,
    RoleListCreateView,
    UserRoleDetailView,
    UserRoleListCreateView,
)

urlpatterns = [
    # Роли
    path("roles/", RoleListCreateView.as_view(), name="roles-list"),
    path("roles/<int:pk>/", RoleDetailView.as_view(), name="role-detail"),
    # Бизнес-элементы
    path(
        "elements/",
        BusinessElementListCreateView.as_view(),
        name="elements-list",
    ),
    path(
        "elements/<int:pk>/",
        BusinessElementDetailView.as_view(),
        name="element-detail",
    ),
    # Правила доступа
    path(
        "rules/",
        AccessRuleListCreateView.as_view(),
        name="rules-list",
    ),
    path(
        "rules/<int:pk>/",
        AccessRuleDetailView.as_view(),
        name="rule-detail",
    ),
    # Роли пользователей
    path(
        "user-roles/",
        UserRoleListCreateView.as_view(),
        name="user-roles-list",
    ),
    path(
        "user-roles/<int:pk>/",
        UserRoleDetailView.as_view(),
        name="user-role-detail",
    ),
]
