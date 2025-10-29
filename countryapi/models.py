from django.db import models
from django.utils import timezone
import random
import uuid
from decimal import Decimal



# Create your models here.



class Country(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=255, unique=True, blank=False, null=False)
    capital = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=255,  blank=True, null=True)
    population = models.BigIntegerField(null=False, blank=False)
    currency_code = models.CharField(null=True, blank=False, max_length=10)
    exchange_rate = models.DecimalField(null=True, blank=False, max_digits=20, decimal_places=10)
    estimated_gdp = models.BigIntegerField(null=True, blank=False)
    flag_url = models.URLField(null=True, blank=True)
    last_refreshed_at = models.DateTimeField(auto_now=True)
    
    
    
    def __str__(self):
        return self.name
    
   