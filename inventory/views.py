from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q

from .models import Product, Order
from .forms import ProductForm, OrderForm


def is_admin(user):
    return user.is_authenticated and user.is_staff


def home(request):
    q = request.GET.get("q", "").strip()

    products = Product.objects.filter(status="active").order_by("-id")

    if q:
        products = products.filter(
            Q(name__icontains=q) |
            Q(sku__icontains=q)
        )

    orders = Order.objects.none()

    if request.user.is_authenticated:
        if request.user.is_staff:
            orders = Order.objects.all().select_related("product").order_by("-id")
        else:
            orders = Order.objects.filter(
                customer_name=request.user.username
            ).select_related("product").order_by("-id")

    context = {
        "products": products,
        "orders": orders,
        "q": q,
    }

    return render(request, "inventory/home.html", context)


# CRUD PRODUCT

@login_required
@user_passes_test(is_admin)
def product_list(request):
    q = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", "-id")

    products = Product.objects.all()

    if q:
        products = products.filter(
            Q(name__icontains=q) |
            Q(sku__icontains=q)
        )

    allowed_sorts = ["id", "-id", "name", "-name", "quantity", "-quantity", "price", "-price"]
    if sort not in allowed_sorts:
        sort = "-id"

    products = products.order_by(sort)

    return render(
        request,
        "inventory/product_list.html",
        {
            "products": products,
            "q": q,
            "sort": sort,
        }
    )


@login_required
@user_passes_test(is_admin)
def product_create(request):
    form = ProductForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        messages.success(request, "Thêm sản phẩm thành công")
        return redirect("product_list")

    return render(request, "inventory/form.html", {"form": form, "title": "Thêm sản phẩm"})


@login_required
@user_passes_test(is_admin)
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)

    if form.is_valid():
        form.save()
        messages.success(request, "Cập nhật sản phẩm thành công")
        return redirect("product_list")

    return render(request, "inventory/form.html", {"form": form, "title": "Cập nhật sản phẩm"})


@login_required
@user_passes_test(is_admin)
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        product.delete()
        messages.success(request, "Xóa sản phẩm thành công")
        return redirect("product_list")

    return render(
        request,
        "inventory/confirm_delete.html",
        {
            "object": product,
            "type": "sản phẩm",
        }
    )


# CREATE ORDER

@login_required
def order_create(request):
    initial_data = {}

    product_id = request.GET.get("product")
    if product_id:
        try:
            product_obj = Product.objects.get(pk=product_id, status="active")
            initial_data["product"] = product_obj
        except Product.DoesNotExist:
            messages.error(request, "Sản phẩm không tồn tại hoặc đang ngừng bán.")
            return redirect("home")

    form = OrderForm(request.POST or None, initial=initial_data)

    if form.is_valid():
        order = form.save(commit=False)
        product = order.product

        if product.status != "active":
            messages.error(request, "Sản phẩm này hiện không thể đặt.")
            return redirect("home")

        if order.quantity <= 0:
            messages.error(request, "Số lượng phải lớn hơn 0.")
            return redirect("home")

        if product.quantity < order.quantity:
            messages.error(request, f"Không đủ hàng. Tồn kho hiện tại: {product.quantity}")
            return redirect("home")

        if request.user.is_staff:
            if not order.customer_name:
                order.customer_name = request.user.username
        else:
            order.customer_name = request.user.username

        product.quantity -= order.quantity
        product.save()

        order.status = "pending"
        order.save()

        messages.success(request, "Đặt hàng thành công. Đơn hàng đang chờ duyệt.")
        return redirect("home")

    return render(
        request,
        "inventory/form.html",
        {
            "form": form,
            "title": "Đặt hàng",
        }
    )


@login_required
def order_list(request):
    if request.user.is_staff:
        orders = Order.objects.all().select_related("product").order_by("-id")
    else:
        orders = Order.objects.filter(
            customer_name=request.user.username
        ).select_related("product").order_by("-id")

    return render(request, "inventory/order_list.html", {"orders": orders})


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order.objects.select_related("product"), pk=pk)

    if not request.user.is_staff and order.customer_name != request.user.username:
        messages.error(request, "Bạn không có quyền xem đơn hàng này.")
        return redirect("home")

    return render(request, "inventory/order_detail.html", {"order": order})


@login_required
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if not request.user.is_staff and order.customer_name != request.user.username:
        messages.error(request, "Bạn không có quyền xóa đơn hàng này.")
        return redirect("home")

    if request.method == "POST":
        if order.status == "approved":
            order.product.quantity += order.quantity
            order.product.save()

        order.delete()
        messages.success(request, "Xóa đơn hàng thành công.")
        return redirect("home")

    return render(
        request,
        "inventory/confirm_delete.html",
        {
            "object": order,
            "type": "đơn hàng",
        }
    )


# APPROVE / REJECT ORDER

@login_required
@user_passes_test(is_admin)
def order_approve(request, pk):
    order = get_object_or_404(Order, pk=pk)

    order.status = "approved"
    order.save()

    messages.success(request, "Đã duyệt đơn hàng.")
    return redirect("dashboard")


@login_required
@user_passes_test(is_admin)
def order_reject(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if order.status == "pending":
        order.product.quantity += order.quantity
        order.product.save()

    order.status = "rejected"
    order.save()

    messages.error(request, "Đã từ chối đơn hàng.")
    return redirect("dashboard")


@login_required
@user_passes_test(is_admin)
def dashboard(request):
    q = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()
    sort = request.GET.get("sort", "-id")

    products = Product.objects.all()
    orders = Order.objects.all().select_related("product")

    if q:
        products = products.filter(
            Q(name__icontains=q) |
            Q(sku__icontains=q)
        )

        orders = orders.filter(
            Q(customer_name__icontains=q) |
            Q(product__name__icontains=q)
        )

    if status:
        orders = orders.filter(status=status)

    allowed_sorts = ["id", "-id", "quantity", "-quantity", "status", "-status"]
    if sort not in allowed_sorts:
        sort = "-id"

    orders = orders.order_by(sort)
    products = products.order_by("-id")

    context = {
        "products": products,
        "orders": orders,
        "q": q,
        "status": status,
        "sort": sort,
        "total_products": Product.objects.count(),
        "total_orders": Order.objects.count(),
        "pending_orders": Order.objects.filter(status="pending").count(),
        "approved_orders": Order.objects.filter(status="approved").count(),
        "rejected_orders": Order.objects.filter(status="rejected").count(),
    }

    return render(request, "inventory/dashboard.html", context)
