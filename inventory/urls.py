from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("dashboard/", views.dashboard, name="dashboard"),

    path("products/", views.product_list, name="product_list"),
    path("products/add/", views.product_create, name="product_add"),
    path("products/<int:pk>/edit/", views.product_update, name="product_edit"),
    path("products/<int:pk>/delete/", views.product_delete, name="product_delete"),

    path("orders/", views.order_list, name="order_list"),
    path("orders/add/", views.order_create, name="order_create"),
    path("orders/my/", views.my_orders, name="my_orders"),
    path("orders/<int:pk>/approve/", views.order_approve, name="order_approve"),
    path("orders/<int:pk>/reject/", views.order_reject, name="order_reject"),
]
