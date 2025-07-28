from django.db import models
from django.core.validators import MinValueValidator

class Product(models.Model):
    name        = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    quantity    = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Quantity must be at least 1"
    )
    price       = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Price must be at least ₹0.01"
    )
    date_added  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    ACTIONS = [
        ('A', 'Added'),
        ('U', 'Updated'),
        ('D', 'Deleted'),
    ]

    product      = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    product_name = models.CharField(
        max_length=100,
        default="",   # ← backfills existing rows so migrations won’t prompt you
        help_text="Snapshot of the product name at time of transaction"
    )
    action       = models.CharField(max_length=1, choices=ACTIONS)
    quantity     = models.IntegerField()
    timestamp    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_action_display()} {self.quantity} of {self.product_name}"
