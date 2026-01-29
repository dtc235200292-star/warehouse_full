from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    # ✅ customer đặt hàng
    path("orders/add/", views.order_create, name="order_add"),

    # ✅ staff dashboard
    path("dashboard/", views.dashboard, name="dashboard"),
]
