from django.db import models

class CarNumber(models.Model):
    number = models.CharField(max_length=20)
    date_added = models.DateTimeField(auto_now_add=True)
# Create your models here.
