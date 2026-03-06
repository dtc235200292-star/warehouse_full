from django import forms
from .models import Product, Order


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = "__all__"

    def clean_image(self):
        image = self.cleaned_data.get("image")

        if image:

            if image.size > 2 * 1024 * 1024:
                raise forms.ValidationError("Ảnh phải < 2MB")

            if not image.name.endswith((".jpg", ".png", ".jpeg")):
                raise forms.ValidationError("Chỉ cho phép jpg/png")

        return image


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ["product", "customer_name", "quantity"]
