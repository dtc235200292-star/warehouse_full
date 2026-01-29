from django import forms
from .models import Product, Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["product", "customer_name", "quantity"]

    def clean_quantity(self):
        qty = self.cleaned_data.get("quantity")
        if qty is None or qty <= 0:
            raise forms.ValidationError("Số lượng phải > 0.")
        return qty

    def clean(self):
        cleaned = super().clean()
        product = cleaned.get("product")
        qty = cleaned.get("quantity")

        if product and qty:
            if product.quantity < qty:
                raise forms.ValidationError(
                    f"Kho không đủ hàng. Tồn hiện tại: {product.quantity}"
                )
        return cleaned
