from django.db import models
from django.urls import reverse
from django.forms import model_to_dict
from django_extensions.db.fields import AutoSlugField
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
"""
Module: models.py

Contains Django models for handling categories, items, and deliveries.

This module defines the following classes:
- Category: Represents a category for items.
- Product: Represents an product in the inventory.
- Order: Represents a order of an item to a customer.

Each class provides specific fields and methods for handling related data.
"""
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order #{self.pk} - {self.product.name}"