import cv2
import serial
import time

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
ArduinoSerial = serial.Serial('com4', 9600, timeout=0.1)
time.sleep(1)

screen_center_x = 640 // 2
screen_center_y = 480 // 2
center_tolerance = 200 // 2
desired_fps = 20
speed = 0.5

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

        if abs(face_center_x - screen_center_x) > center_tolerance or abs(face_center_y - screen_center_y) > center_tolerance:
            offset_x = (face_center_x - screen_center_x) * speed
            offset_y = (face_center_y - screen_center_y) * speed
            string = 'X{0:+d}Y{1:+d}'.format(int(-offset_x), int(-offset_y))
            print(string)
            ArduinoSerial.write(string.encode('utf-8'))
        else:
            ArduinoSerial.write('X0Y0'.encode('utf-8'))

        cv2.circle(frame, (face_center_x, face_center_y), 2, (0, 255, 0), 2)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)

    cv2.rectangle(frame, (screen_center_x - center_tolerance, screen_center_y - center_tolerance),
                  (screen_center_x + center_tolerance, screen_center_y + center_tolerance), (255, 255, 255), 3)

    cv2.imshow('img', frame)

    elapsed_time = time.time() - start_time
    if elapsed_time < 1 / desired_fps:
        time.sleep(1 / desired_fps - elapsed_time)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
