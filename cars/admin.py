from django.contrib import admin
from .models import CarNumber

class CarNumberAdmin(admin.ModelAdmin):
    list_display = ('number', 'time')  # Определение отображаемых полей в списке объектов модели

# Зарегистрируйте модель CarNumber с использованием настроенного класса CarNumberAdmin
admin.site.register(CarNumber, CarNumberAdmin)
