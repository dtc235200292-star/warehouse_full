from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("products/", views.product_list, name="product_list"),
    path("products/add/", views.product_create, name="product_add"),
    path("products/edit/<int:pk>/", views.product_update, name="product_edit"),
    path("products/delete/<int:pk>/", views.product_delete, name="product_delete"),

    path("orders/", views.order_list, name="order_list"),
    path("orders/add/", views.order_create, name="order_add"),
    path("orders/<int:pk>/", views.order_detail, name="order_detail"),
    path("orders/delete/<int:pk>/", views.order_delete, name="order_delete"),
    path("orders/approve/<int:pk>/", views.order_approve, name="order_approve"),
    path("orders/reject/<int:pk>/", views.order_reject, name="order_reject"),

    path("dashboard/", views.dashboard, name="dashboard"),
]
