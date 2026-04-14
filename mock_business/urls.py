from django.urls import path

from .views import MockOrdersListView, MockReportsView, MockUsersListView

urlpatterns = [
    path("users/", MockUsersListView.as_view(), name="mock-users"),
    path("orders/", MockOrdersListView.as_view(), name="mock-orders"),
    path("reports/", MockReportsView.as_view(), name="mock-reports"),
]
