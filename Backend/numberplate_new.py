import cv2
import numpy as np
import pytesseract
from datetime import datetime
import time

detected_cars = set()  # Store detected car numbers to avoid duplicates

def perform_anpr(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    gray = cv2.bilateralFilter(gray, 13, 15, 15)
    edges = cv2.Canny(gray, 30, 200)
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    screenCnt = None
    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)
        if len(approx) == 4:
            screenCnt = approx
            break

    if screenCnt is None:
        print("No contour detected")
        return None

    cv2.drawContours(frame, [screenCnt], -1, (0, 255, 0), 3)

    mask = np.zeros(gray.shape, np.uint8)
    new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1)
    new_image = cv2.bitwise_and(frame, frame, mask=mask)

    (x, y) = np.where(mask == 255)
    (topx, topy) = (np.min(x), np.min(y))
    (bottomx, bottomy) = (np.max(x), np.max(y))
    Cropped = gray[topx:bottomx + 1, topy:bottomy + 1]

    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    text = pytesseract.image_to_string(Cropped, config='--psm 11')
    print("Detected Number is:", text)

    return text

def save_to_file(text):
    if text not in detected_cars:
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        with open('detected_cars.txt', 'a') as file:
            file.write(f"Car Number:{text}Entry date & Time: {current_time}\n")
        detected_cars.add(text)

def real_time_anpr():
    cap = cv2.VideoCapture(0)

    delay_time = 3  # Set the delay time in seconds

    while True:
        plate_detected = False

        while not plate_detected:
            ret, frame = cap.read()
            if not ret:
                print("Error reading frame")
                break

            plate_number = perform_anpr(frame)
            if plate_number:
                save_to_file(plate_number)
                plate_detected = True

            cv2.imshow('ANPR', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(delay_time)  # Add delay before processing the next frame

    cap.release()
    cv2.destroyAllWindows()

real_time_anpr()
