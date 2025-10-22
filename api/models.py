from django.db import models
from django.utils import timezone



# Create your models here.

class String(models.Model):
    id = models.TextField(max_length=64, primary_key=True, editable=False, unique=True)
    value = models.TextField()
    length = models.IntegerField()
    is_palindrome = models.BooleanField()
    unique_characters = models.IntegerField()
    word_count = models.IntegerField()
    sha256_hash = models.CharField(max_length=1000)
    character_frequency_map = models.JSONField()
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    
    
    
    def __str__(self):
        return self.value
    