from django.shortcuts import render
from .models import CarNumber
from django.http import HttpResponse, HttpRequest
from django.utils import timezone

def the_database_of_cars(request: HttpRequest) -> HttpResponse:
    return HttpResponse("The database of cars")

def process_video(request):
    if request.method == 'POST' and request.FILES.get('video'):
        video = request.FILES['video']

        # Обработка видеофайла и распознавание номеров автомобилей
        # Здесь должен быть ваш код для обработки видеофайла и распознавания номеров автомобилей

        # Пример сохранения номера автомобиля в базе данных с датой и временем
        recognized_number = "ABC123"  # Полученный распознанный номер автомобиля
        car = CarNumber(number=recognized_number, time=timezone.now())
        car.save()

        return HttpResponse("Видеофайл обработан и номера сохранены.")

    return render(request, 'upload.html')
