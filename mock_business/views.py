from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from access_control.permissions import HasAccess


class MockUsersListView(generics.GenericAPIView):
    """
    Mock-эндпоинт: список пользователей.

    Требует: read permission для элемента 'users'.
    """

    permission_classes = [HasAccess]

    def get_permissions(self):
        """
        Динамически устанавливаем атрибуты для permission.
        """
        perms = super().get_permissions()
        for permission in perms:
            if isinstance(permission, HasAccess):
                permission.business_element = "users"
                permission.required_permission = "read"
        return perms

    def get(self, request, *args, **kwargs):
        return Response(
            {
                "data": [
                    {"id": 1, "name": "Иванов Иван"},
                    {"id": 2, "name": "Петрова Анна"},
                ]
            },
            status=status.HTTP_200_OK,
        )


class MockOrdersListView(generics.GenericAPIView):
    """
    Mock-эндпоинт: список заказов.

    Требует: read permission для элемента 'orders'.
    """

    permission_classes = [HasAccess]

    def get_permissions(self):
        perms = super().get_permissions()
        for permission in perms:
            if isinstance(permission, HasAccess):
                permission.business_element = "orders"
                permission.required_permission = "read"
        return perms

    def get(self, request, *args, **kwargs):
        return Response(
            {
                "data": [
                    {"id": 1, "order": "ORD-001", "amount": 15000},
                    {"id": 2, "order": "ORD-002", "amount": 23000},
                ]
            },
            status=status.HTTP_200_OK,
        )


class MockReportsView(generics.GenericAPIView):
    """
    Mock-эндпоинт: отчёты.

    Требует: read permission для элемента 'reports'.
    """

    permission_classes = [HasAccess]

    def get_permissions(self):
        perms = super().get_permissions()
        for permission in perms:
            if isinstance(permission, HasAccess):
                permission.business_element = "reports"
                permission.required_permission = "read"
        return perms

    def get(self, request, *args, **kwargs):
        return Response(
            {
                "data": [
                    {"id": 1, "title": "Отчёт за Q1", "date": "2026-03-31"},
                    {"id": 2, "title": "Отчёт за Q2", "date": "2026-06-30"},
                ]
            },
            status=status.HTTP_200_OK,
        )
