from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.db import IntegrityError
from django.shortcuts import render, redirect

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            try:
                user = form.save()
            except IntegrityError:
                form.add_error("username", "Tên tài khoản đã tồn tại.")
                messages.error(request, "❌ Tên tài khoản đã tồn tại.")
            else:
                login(request, user)
                messages.success(request, "✅ Đăng ký thành công!")
                return redirect("home")
        else:
            messages.error(request, "❌ Dữ liệu chưa hợp lệ. Kiểm tra lại form.")

    return render(request, "accounts/register.html", {"form": form})
