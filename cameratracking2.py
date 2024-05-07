import cv2
import serial
import time

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
ArduinoSerial = serial.Serial('com3', 9600, timeout=0.1)
time.sleep(1)

screen_center_x = 640 // 2
screen_center_y = 480 // 2
desired_fps = 20
speed = 0.4

while cap.isOpened():
    start_time = time.time()
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame = cv2.flip(frame, 0)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 6)

    if len(faces) > 0:
        biggest_face = max(faces, key=lambda rect: rect[2] * rect[3])
        x, y, w, h = biggest_face
        face_center_x = x + w // 2
        face_center_y = y + h // 2

        offset_x = (face_center_x - screen_center_x) * speed
        offset_y = (face_center_y - screen_center_y) * speed

        string = 'X{0:+d}Y{1:+d}'.format(int(-offset_x), int(-offset_y))
        print(string)
        ArduinoSerial.write(string.encode('utf-8'))

        cv2.circle(frame, (face_center_x, face_center_y), 2, (0, 255, 0), 2)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)

    cv2.rectangle(frame, (screen_center_x - 30, screen_center_y - 30),
                  (screen_center_x + 30, screen_center_y + 30), (255, 255, 255), 3)

    cv2.imshow('img', frame)

    elapsed_time = time.time() - start_time
    fps = 1 / elapsed_time if elapsed_time > 0 else 0

    if elapsed_time < 1 / desired_fps:
        time.sleep(1 / desired_fps - elapsed_time)


    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()