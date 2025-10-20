# идея такая дать понять ему то что 3 цифры потом 3 букывы потом 2 цифры тем самым вместо 4 он даст А
import cv2
import easyocr
import numpy as np
import re

# Установка конфигурации для EasyOCR
reader = easyocr.Reader(['en'])

# Загрузка изображения с номером автомобиля
image = cv2.imread('mini3.png')

# Применение фильтра Гаусса для удаления шума на изображении
image = cv2.GaussianBlur(image, (3, 3), 0)

# Преобразование изображения в черно-белое
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

# Применение морфологических операций для удаления мелких объектов и заполнения пропусков в буквах и цифрах номера
kernel = np.ones((3,3),np.uint8)
closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
result = cv2.erode(closing, kernel, iterations=1)

# Применение контуров для выделения номера автомобиля на изображении
contours, hierarchy = cv2.findContours(result, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(contours, key=cv2.contourArea, reverse=True)[:1]
for c in cnts:
    x,y,w,h = cv2.boundingRect(c)
    roi = image[y:y+h, x:x+w]

# Распознавание номера
result = reader.readtext(roi)

# Определение шаблона номера и извлечение его из распознанной строки
pattern = r'\d{3}[A-Za-z]{3}\d{2}'
filtered_result = re.findall(pattern, result[0][1])

if result:
    result_str = result[0][1]
    filtered_result = re.sub(r'[^a-zA-Z0-9]', '', result_str)
    print(filtered_result)
else:
    print("Ошибка: номер не найден")
