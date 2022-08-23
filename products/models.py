from django.db import models
from django import forms
import datetime
import calculation

# Create your models here.

class Supplier(models.Model):
    name = models.CharField(max_length=20, unique = True)
    company_name = models.CharField(max_length=20, null=True, blank=True)
    category = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(
        null=True, blank=True, default="default.jpg")
    mobile_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return str(self.name)


class Sku(models.Model):
    code = models.CharField(max_length=10, unique = True)
    main_image = models.ImageField(
        null=True, blank=True, default="default.jpg")
    link = models.URLField(max_length=500, null=True, blank=True,)

    def __str__(self):
        return str(self.code)

now = datetime.datetime.now()
class Entry(models.Model):
    code = models.ForeignKey(Sku, null=True, blank=True, on_delete=models.CASCADE)
    price = models.IntegerField(null=True, blank=True, default=0)
    qty = models.IntegerField(null=True, blank=True, default=0)
    total_price = models.IntegerField( null=True, blank=True,)
    order_date = models.DateField(null=True, blank=True,)
    delivery_date = models.DateField(null=True, blank=True,)

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True)
    Initial = 'Initial'
    Assigned = 'Assigned'
    Pending = 'Pending'
    Complete = 'Complete'

    STATUS = [
        (Initial, 'Initial'),
        (Assigned, 'Assigned'),
        (Pending, 'Pending'),
        (Complete, 'Complete'),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS,
        default=Initial,
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True,)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True,)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.code)

    def save(self, *args, **kwargs):
        self.total_price = self.qty * self.price
        super(Entry, self).save(*args, **kwargs)


