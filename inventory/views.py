from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q, Count, Sum

from .models import Product, Order, Category, Supplier, StockHistory
from .forms import ProductForm, OrderForm, CategoryForm, SupplierForm


def is_admin(user):
    return user.is_authenticated and user.is_staff


def home(request):
    q = request.GET.get("q", "")
    products = Product.objects.filter(status="active")

    if q:
        products = products.filter(
            Q(name__icontains=q) |
            Q(sku__icontains=q) |
            Q(category__name__icontains=q)
        )

    return render(request, "inventory/home.html", {
        "products": products,
        "q": q,
    })


@login_required
@user_passes_test(is_admin)
def dashboard(request):
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status="pending").count()
    approved_orders = Order.objects.filter(status="approved").count()

    low_stock_products = Product.objects.filter(quantity__lte=5)
    recent_orders = Order.objects.select_related("user", "product").order_by("-created_at")[:10]

    order_stats = Order.objects.values("status").annotate(total=Count("id"))
    category_stats = Category.objects.annotate(total_products=Count("products"))

    return render(request, "inventory/dashboard.html", {
        "total_products": total_products,
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "approved_orders": approved_orders,
        "low_stock_products": low_stock_products,
        "recent_orders": recent_orders,
        "order_stats": order_stats,
        "category_stats": category_stats,
    })


@login_required
@user_passes_test(is_admin)
def product_list(request):
    q = request.GET.get("q", "")
    products = Product.objects.select_related("category", "supplier").all()

    if q:
        products = products.filter(
            Q(name__icontains=q) |
            Q(sku__icontains=q) |
            Q(category__name__icontains=q)
        )

    return render(request, "inventory/product_list.html", {
        "products": products,
        "q": q,
    })


@login_required
@user_passes_test(is_admin)
def product_create(request):
    form = ProductForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        product = form.save()
        StockHistory.objects.create(
            product=product,
            action="import",
            quantity=product.quantity,
            note="Tạo sản phẩm mới"
        )
        messages.success(request, "Thêm sản phẩm thành công.")
        return redirect("product_list")

    return render(request, "inventory/form.html", {
        "form": form,
        "title": "Thêm sản phẩm"
    })


@login_required
@user_passes_test(is_admin)
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    old_quantity = product.quantity

    form = ProductForm(request.POST or None, request.FILES or None, instance=product)

    if form.is_valid():
        product = form.save()

        if product.quantity != old_quantity:
            StockHistory.objects.create(
                product=product,
                action="import" if product.quantity > old_quantity else "export",
                quantity=abs(product.quantity - old_quantity),
                note="Cập nhật số lượng tồn kho"
            )

        messages.success(request, "Cập nhật sản phẩm thành công.")
        return redirect("product_list")

    return render(request, "inventory/form.html", {
        "form": form,
        "title": "Cập nhật sản phẩm"
    })


@login_required
@user_passes_test(is_admin)
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        product.delete()
        messages.success(request, "Xóa sản phẩm thành công.")
        return redirect("product_list")

    return render(request, "inventory/confirm_delete.html", {
        "object": product,
        "title": "Xóa sản phẩm"
    })


@login_required
def order_create(request):
    product_id = request.GET.get("product")
    initial = {}

    if product_id:
        initial["product"] = get_object_or_404(Product, pk=product_id, status="active")

    form = OrderForm(request.POST or None, initial=initial)

    if form.is_valid():
        order = form.save(commit=False)
        order.user = request.user

        if order.quantity <= 0:
            messages.error(request, "Số lượng phải lớn hơn 0.")
            return redirect("order_create")

        if order.product.quantity < order.quantity:
            messages.error(request, "Sản phẩm không đủ tồn kho.")
            return redirect("home")

        order.save()
        messages.success(request, "Đặt hàng thành công. Đơn hàng đang chờ duyệt.")
        return redirect("my_orders")

    return render(request, "inventory/form.html", {
        "form": form,
        "title": "Tạo đơn hàng"
    })


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).select_related("product").order_by("-created_at")
    return render(request, "inventory/my_orders.html", {
        "orders": orders
    })


@login_required
@user_passes_test(is_admin)
def order_list(request):
    orders = Order.objects.select_related("user", "product").order_by("-created_at")
    return render(request, "inventory/order_list.html", {
        "orders": orders
    })


@login_required
@user_passes_test(is_admin)
def order_approve(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if order.status != "pending":
        messages.warning(request, "Đơn hàng này đã được xử lý.")
        return redirect("order_list")

    if order.product.quantity < order.quantity:
        messages.error(request, "Không đủ hàng để duyệt đơn.")
        return redirect("order_list")

    product = order.product
    product.quantity -= order.quantity
    product.save()

    order.status = "approved"
    order.save()

    StockHistory.objects.create(
        product=product,
        action="order",
        quantity=order.quantity,
        note=f"Duyệt đơn hàng #{order.id}"
    )

    messages.success(request, "Duyệt đơn hàng thành công.")
    return redirect("order_list")


@login_required
@user_passes_test(is_admin)
def order_reject(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = "rejected"
    order.save()

    messages.success(request, "Đã từ chối đơn hàng.")
    return redirect("order_list")
