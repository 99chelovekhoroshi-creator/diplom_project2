from django.urls import path
from cars.views import the_database_of_cars, process_video

urlpatterns = [
    path('', the_database_of_cars, name='index'),
    path('process-video/', process_video, name='process_video'),
]
