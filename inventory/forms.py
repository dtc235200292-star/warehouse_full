from django import forms
from .models import Product, Order, Category, Supplier


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["category", "supplier", "name", "sku", "quantity", "price", "image", "status"]

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image:
            if image.size > 2 * 1024 * 1024:
                raise forms.ValidationError("Ảnh không được vượt quá 2MB.")
            if not image.name.lower().endswith((".jpg", ".jpeg", ".png")):
                raise forms.ValidationError("Chỉ cho phép ảnh JPG, JPEG hoặc PNG.")
        return image


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["product", "quantity", "note"]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description"]


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ["name", "phone", "address"]
