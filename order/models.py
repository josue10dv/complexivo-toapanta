from django.db import models

class AvailableState:
    PENDING = "pending"
    IN_PROGRESS = "in_process"
    SERVED = "served"
    PAID = "paid"

    CHOICES = [
        (PENDING, "pendiente"),
        (IN_PROGRESS, "en proceso"),
        (SERVED, "servido"),
        (PAID, "pagado"),
    ]

class Tables(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    capacity = models.IntegerField(null=False)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Orders(models.Model):
    table_id = models.ForeignKey(Tables, on_delete=models.PROTECT, related_name="fk_order_table")
    # Nueva columna para el número de orden
    number = models.IntegerField(null=True, blank=True, unique=True)
    items_summary = models.TextField(null=False)
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    state = models.CharField(
        max_length=20,
        choices=AvailableState.CHOICES,
        default=AvailableState.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Orden #{self.number} - Mesa {self.table_id.name}"
