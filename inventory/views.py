from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.shortcuts import render, redirect
from django.db.models import Q

from .models import Product, Order
from .forms import OrderForm


def home(request):
    products = Product.objects.all().order_by("-id")

    # ✅ Orders: khách chỉ thấy đơn của mình, staff thấy tất cả
    if request.user.is_authenticated:
        if request.user.is_staff:
            orders = Order.objects.all().order_by("-id")[:50]
        else:
            orders = Order.objects.filter(customer_name=request.user.username).order_by("-id")[:50]
    else:
        orders = Order.objects.none()

    return render(request, "inventory/home.html", {"products": products, "orders": orders})


def _is_staff(user):
    return user.is_authenticated and user.is_staff


@login_required
@user_passes_test(_is_staff)
def dashboard(request):
    """
    ✅ Dashboard quản trị (Staff/Admin)
    Có search q (tìm product name/sku, order customer/product)
    """
    q = request.GET.get("q", "").strip()

    products_qs = Product.objects.all().order_by("-id")
    orders_qs = Order.objects.select_related("product").all().order_by("-id")

    if q:
        products_qs = products_qs.filter(Q(name__icontains=q) | Q(sku__icontains=q))
        orders_qs = orders_qs.filter(
            Q(customer_name__icontains=q) |
            Q(product__name__icontains=q) |
            Q(product__sku__icontains=q)
        )

    context = {
        "products": products_qs[:200],
        "orders": orders_qs[:200],
        "q": q,
    }
    return render(request, "inventory/dashboard.html", context)


@login_required
@transaction.atomic
def order_create(request):
    """
    ✅ Khách hàng được đặt
    ✅ Trừ kho theo số lượng đặt (select_for_update để tránh trùng đơn)
    ✅ Staff có thể đặt hộ (nếu bạn muốn cho nhập customer_name)
    """
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)

            # user thường: ép customer_name = username
            if not request.user.is_staff:
                order.customer_name = request.user.username

            # ✅ khóa dòng sản phẩm để trừ kho an toàn
            product = Product.objects.select_for_update().get(pk=order.product_id)

            if order.quantity <= 0:
                form.add_error("quantity", "Số lượng phải lớn hơn 0.")
                return render(request, "inventory/form.html", {"form": form, "title": "Đặt hàng"})

            if product.quantity < order.quantity:
                form.add_error(None, f"Kho không đủ hàng. Tồn hiện tại: {product.quantity}")
                return render(request, "inventory/form.html", {"form": form, "title": "Đặt hàng"})

            # ✅ trừ kho
            product.quantity -= order.quantity
            product.save()

            # ✅ trạng thái
            order.status = "pending"
            order.save()

            messages.success(request, "Đặt hàng thành công! Đơn đang chờ duyệt.")
            return redirect("home")

        messages.error(request, "Dữ liệu chưa hợp lệ. Kiểm tra lại form.")
    else:
        # ✅ Prefill khi bấm "Đặt" ở home: /orders/add/?product=ID
        initial = {}
        product_id = request.GET.get("product")

        if product_id:
            initial["product"] = product_id

        if request.user.is_authenticated and not request.user.is_staff:
            initial["customer_name"] = request.user.username

        form = OrderForm(initial=initial)

    return render(request, "inventory/form.html", {"form": form, "title": "Đặt hàng"})
