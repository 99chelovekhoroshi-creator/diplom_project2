    from PIL import Image, ImageEnhance, ImageFilter, ExifTags
    import pytesseract

    # Открытие изображения и поворот
    img = Image.open('1-small 2.png')
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(img._getexif().items())

        if exif[orientation] == 3:
            img = img.rotate(180, expand=True)
        elif exif[orientation] == 6:
            img = img.rotate(270, expand=True)
        elif exif[orientation] == 8:
            img = img.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        # Обработка ошибки, если exif информация отсутствует
        pass

    # Улучшение качества изображения
    img = img.convert('L')  # Конвертирование изображения в черно-белый формат
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2)  # Увеличение контраста в 2 раза
    img = img.filter(ImageFilter.MedianFilter())  # Применение медианного фильтра
    img = img.filter(ImageFilter.SHARPEN)  # Увеличение резкости изображения

    # Распознавание текста на изображении
    text = pytesseract.image_to_string(img)

    # Вывод распознанного текста
    print(text,img)



# import cv2
#
# cap = cv2.VideoCapture('new.mp4')
# if not cap.isOpened():
#     print("Cannot open video file")
# else:
#     while True:
#         ret, frame = cap.read()
#         if ret:
#             frame = cv2.resize(frame, (800, int(frame.shape[0]/frame.shape[1]*800)))
#             h, w = frame.shape[:2]
#             frame = frame[int(h*0.2):h, :]
#             frame = cv2.copyMakeBorder(frame, 50, 50, 50, 50, cv2.BORDER_CONSTANT)
#             cv2.imshow("Video", frame)
#             if cv2.waitKey(25) & 0xFF == ord('q'):
#                 break
#         else:
#             print("Cannot read the frame")
#             break
#
#     cap.release()
#     cv2.destroyAllWindows()
