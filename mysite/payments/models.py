from django.db import models

# Create your models here.
from django.db import models
from django.utils.timezone import now
import uuid

class MpesaTransaction(models.Model):
    transaction_id = models.CharField(max_length=100, unique=True)
    receiver = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=20)
    time = models.DateTimeField(default=now)
    reference_code = models.CharField(max_length=100)
    is_valid = models.BooleanField(default=False)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"Transaction {self.transaction_id} by {self.sender}"
