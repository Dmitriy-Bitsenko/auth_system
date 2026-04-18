"""
Тестовые данные для RBAC.
Запусти: python manage.py shell
>>> exec(open('seed_test_data.py').read())
>>> run()

3 роли: admin, manager, viewer
3 бизнес-элемента: users, orders, reports
Правила доступа для каждой комбинации
"""

from access_control.models import AccessRoleRule, BusinessElement, Role, UserRole
from custom_auth.models import User
import bcrypt


def run():
    print("Создаю тестовые данные...")

    admin_role, _ = Role.objects.get_or_create(
        name="admin", defaults={"description": "Полный доступ ко всему"}
    )
    manager_role, _ = Role.objects.get_or_create(
        name="manager", defaults={"description": "Управление заказами и отчётами"}
    )
    viewer_role, _ = Role.objects.get_or_create(
        name="viewer", defaults={"description": "Только чтение"}
    )
    print(f"Роли: {admin_role}, {manager_role}, {viewer_role}")

    users_el, _ = BusinessElement.objects.get_or_create(
        name="users", defaults={"description": "Пользователи системы"}
    )
    orders_el, _ = BusinessElement.objects.get_or_create(
        name="orders", defaults={"description": "Заказы"}
    )
    reports_el, _ = BusinessElement.objects.get_or_create(
        name="reports", defaults={"description": "Отчёты и аналитика"}
    )
    print(f"Элементы: {users_el}, {orders_el}, {reports_el}")


    for element in [users_el, orders_el, reports_el]:
        AccessRoleRule.objects.get_or_create(
            role=admin_role,
            element=element,
            defaults={
                "read_perm": True,
                "read_all_perm": True,
                "create_perm": True,
                "update_perm": True,
                "update_all_perm": True,
                "delete_perm": True,
                "delete_all_perm": True,
            },
        )

    AccessRoleRule.objects.get_or_create(
        role=manager_role,
        element=users_el,
        defaults={"read_perm": True, "read_all_perm": True},
    )
    AccessRoleRule.objects.get_or_create(
        role=manager_role,
        element=orders_el,
        defaults={
            "read_perm": True,
            "read_all_perm": True,
            "create_perm": True,
            "update_perm": True,
            "update_all_perm": True,
        },
    )
    AccessRoleRule.objects.get_or_create(
        role=manager_role,
        element=reports_el,
        defaults={
            "read_perm": True,
            "read_all_perm": True,
            "create_perm": True,
        },
    )

    for element in [users_el, orders_el, reports_el]:
        AccessRoleRule.objects.get_or_create(
            role=viewer_role,
            element=element,
            defaults={"read_perm": True, "read_all_perm": True},
        )

    print("Правила доступа созданы")

    admin_user, _ = User.objects.get_or_create(
        email="admin@test.com",
        defaults={
            "first_name": "Админ",
            "last_name": "Системный",
            "is_staff": True,
            "is_superuser": True,
        },
    )
    admin_user.password = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt()).decode()
    admin_user.save()

    manager_user, _ = User.objects.get_or_create(
        email="manager@test.com",
        defaults={
            "first_name": "Менеджер",
            "last_name": "Продаж",
        },
    )
    manager_user.password = bcrypt.hashpw("manager123".encode(), bcrypt.gensalt()).decode()
    manager_user.save()

    viewer_user, _ = User.objects.get_or_create(
        email="viewer@test.com",
        defaults={
            "first_name": "Наблюдатель",
            "last_name": "Простой",
        },
    )
    viewer_user.password = bcrypt.hashpw("viewer123".encode(), bcrypt.gensalt()).decode()
    viewer_user.save()

    print("Пользователи созданы")

    UserRole.objects.get_or_create(user=admin_user, role=admin_role)
    UserRole.objects.get_or_create(user=manager_user, role=manager_role)
    UserRole.objects.get_or_create(user=viewer_user, role=viewer_role)

    print("Роли назначены")
    print("\nТестовые данные готовы!")
    print("\nЛогин:")
    print("  admin@test.com / admin123")
    print("  manager@test.com / manager123")
    print("  viewer@test.com / viewer123")
