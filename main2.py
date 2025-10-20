# HERE WE WORK WITH OBJECT TRAINING . BUT WE HAVE SOME PROBLEMS 667
import cv2
import pytesseract

# Установка конфигурации для PyTesseractq
config = r'--oem 3 --psm 6'

# Загрузка видеофайла
cap = cv2.VideoCapture('new777.mp4')

# Инициализация трекера
tracker = cv2.TrackerCSRT_create()

while True:
    ret, frame = cap.read()
    if ret:
        frame = cv2.resize(frame, (800, 600), interpolation = cv2.INTER_LINEAR)

        h, w = frame.shape[:2]
        frame = frame[int(h*0.2):h, :]
        frame = cv2.copyMakeBorder(frame, 50, 50, 50, 50, cv2.BORDER_CONSTANT)
        cv2.imshow("Video", frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        print("Cannot read the frame")
        break

    # Конвертация текущего кадра в черно-белый
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Загрузка каскадного классификатора для распознавания автомобильных номеров
    plates = cv2.CascadeClassifier('haarcascade_plates.xml')


    # Обнаружение прямоугольных областей, соответствующих автомобильным номерам
    plates_rect = plates.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
    if not frame.any():
        break

    # Обработка каждого обнаруженного автомобильного номера
    for (x, y, w, h) in plates_rect:
        # Отрисовка прямоугольника вокруг автомобильного номера
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Проверка, был ли уже начат tracking для этого номера
        if "tracker" not in locals():
            # Если нет, то инициализация трекера на основе текущего кадра и координат рамки вокруг номера
            tracker.init(frame, (x, y, w, h))
        else:
            # Если трекер уже был инициализирован, то обновление его позиции на основе текущего кадра
            success, box = tracker.update(frame)
            if success:
                (x, y, w, h) = [int(i) for i in box]
                # Отрисовка новой рамки вокруг номера
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Выделение изображения автомобильного номера из текущего кадра
        plate_img = gray[y:y+h, x:x+w]

        # Применение расп
        # Выделение изображения автомобильного номера из текущего кадра
        plate_img = gray[y:y + h, x:x + w]

        # Применение распознавания текста к выделенному изображению автомобильного номера
        plate_text = pytesseract.image_to_string(plate_img, lang='eng', config=config)

        # Очистка распознанного текста от лишних символов и пробелов
        plate_text = ''.join(filter(str.isalnum, plate_text)).upper()

        # Проверка соответствия формату номера
        if len(plate_text) != 8 or not plate_text[:3].isdigit() or not (
                plate_text[3:5].isalpha() and len(plate_text[3:5]) in [2, 3]) or not plate_text[5:].isdigit():
            plate_text = "nomer zhok"

        # Вывод распознанного номера на кадре
        cv2.putText(frame, plate_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # Отображение текущего кадра
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Освобождение ресурсов и закрытие окна
cap.release()
cv2.destroyAllWindows()