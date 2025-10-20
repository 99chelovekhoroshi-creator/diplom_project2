from django.db import models
from django.utils import timezone

from django.db import models
from django.utils import timezone

class CarNumber(models.Model):
    number = models.CharField(max_length=10)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.number


# from django.utils import timezone
#
# class CarNumber(models.Model):
#     number = models.CharField(max_length=20)
#
#
#
#     def __str__(self):
#         return self.number





