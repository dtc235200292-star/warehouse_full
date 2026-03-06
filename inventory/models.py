from django.db import models

class Product(models.Model):

    STATUS = [
        ("active", "Active"),
        ("inactive", "Inactive"),
    ]

    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=50, unique=True)

    quantity = models.IntegerField(default=0)

    price = models.FloatField(default=0)

    image = models.ImageField(upload_to="products/", null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="active"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Order(models.Model):

    STATUS = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    customer_name = models.CharField(max_length=100)

    quantity = models.IntegerField(default=1)

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.product.name}"
