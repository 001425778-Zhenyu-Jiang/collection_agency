from django.db import models

class Account(models.Model):
    client_reference_no = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)
    consumer_name = models.CharField(max_length=100)
    consumer_address = models.CharField(max_length=255)
    ssn = models.CharField(max_length=11)  # Adjust the length based on your format

    def __str__(self):
        return f"{self.consumer_name} - {self.balance}"
