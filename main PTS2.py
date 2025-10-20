import cv2
import pytesseract
import re
import requests
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'databaseproject.settings')

import django
django.setup()

import sys
from django.utils import timezone
from cars.models import CarNumber

# Добавьте путь к вашему проекту Django
sys.path.append('C://Users//rasul//OneDrive//Рабочий стол//sec//databaseproject')

# Задайте переменную окружения DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

import django
django.setup()

config = r'--oem 3 --psm 6'

cap = cv2.VideoCapture('007.mp4')

recognized_number = None

while True:
    ret, frame = cap.read()
    if ret:
        frame = cv2.resize(frame, (800, int(frame.shape[0]/frame.shape[1]*800)))
        h, w = frame.shape[:2]
        frame = frame[int(h*0.2):h, :]
        frame = cv2.copyMakeBorder(frame, 50, 50, 50, 50, cv2.BORDER_CONSTANT)
    else:
        print("Cannot read the frame")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    plates = cv2.CascadeClassifier('haarcascade_plates.xml')

    plates_rect = plates.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

    for (x, y, w, h) in plates_rect:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        plate_img = gray[y:y+h, x:x+w]

        plate_text = pytesseract.image_to_string(plate_img, lang='eng', config=config)

        plate_text = ''.join(filter(str.isalnum, plate_text)).upper()

        if re.match(r"[A-Z]{2}\d{3}[A-Z]{3}\d{2}", plate_text) and recognized_number is None:
            recognized_number = plate_text
            # Создание объекта CarNumber и сохранение его в базе данных Django
            car = CarNumber(number=recognized_number, time=timezone.now())
            car.save()

        cv2.putText(frame, plate_text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

if recognized_number is not None:
    print(recognized_number)






# import cv2
# import pytesseract
# import re
# import requests
# import os
# import sys
#
# # Добавьте путь к вашему проекту Django
# sys.path.append('C://Users//rasul//OneDrive//Рабочий стол//sec//databaseproject')
#
# # Задайте переменную окружения DJANGO_SETTINGS_MODULE
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
#
# import django
# django.setup()
#
# config = r'--oem 3 --psm 6'
#
# cap = cv2.VideoCapture('007.mp4')
#
# recognized_number = None
#
# while True:
#     ret, frame = cap.read()
#     if ret:
#         frame = cv2.resize(frame, (800, int(frame.shape[0]/frame.shape[1]*800)))
#         h, w = frame.shape[:2]
#         frame = frame[int(h*0.2):h, :]
#         frame = cv2.copyMakeBorder(frame, 50, 50, 50, 50, cv2.BORDER_CONSTANT)
#     else:
#         print("Cannot read the frame")
#         break
#
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#
#     plates = cv2.CascadeClassifier('haarcascade_plates.xml')
#
#     plates_rect = plates.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
#
#     for (x, y, w, h) in plates_rect:
#         cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
#
#         plate_img = gray[y:y+h, x:x+w]
#
#         plate_text = pytesseract.image_to_string(plate_img, lang='eng', config=config)
#
#         plate_text = ''.join(filter(str.isalnum, plate_text)).upper()
#
#         if re.match(r"[A-Z]{2}\d{3}[A-Z]{3}\d{2}", plate_text) and recognized_number is None:
#             recognized_number = plate_text
#             # Создание объекта CarNumber и сохранение его в базе данных Django
#             from cars.models import CarNumber
#             car = CarNumber(number=recognized_number)
#             car.save()
#
#         cv2.putText(frame, plate_text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
#
#     cv2.imshow('frame', frame)
#
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# cap.release()
# cv2.destroyAllWindows()
#
# if recognized_number is not None:
#     print(recognized_number)

