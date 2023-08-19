from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField

class Product(models.Model):
    class availibility(models.TextChoices):
        YES = 'yes'
        NO  = 'no'

    pname       = models.CharField(max_length=255, unique=True)
    pprice      = models.IntegerField()
    available   = models.CharField(max_length=3, choices=availibility.choices, default=availibility.NO)
    ptag        = models.CharField(max_length=255)

    class Meta:
        ordering = ['-ptag']

class Order(models.Model):
    name    = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    items   = JSONField(default=dict)
    chat    = JSONField(default=dict)
    total   = models.IntegerField()
    user    = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)

    class Meta:
        ordering = ['-total']


class Customer(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    class Meta:
        ordering = ['-user']