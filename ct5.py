import cv2
import serial
import time

def preprocess_image(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    return gray

def facetracking():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    ArduinoSerial = serial.Serial('COM7', 9600, timeout=0.1)
    time.sleep(1)

    screen_center_x = 640 // 2
    screen_width = 640
    screen_height = 480
    center_tolerance = 200
    intermediate_space = screen_width * 0.40

    fps = 23
    delay = 1 / fps
    wait_time = 0.2 # Tiempo entre señales
    last_sent_time = time.time()
    
    last_detected_position = None

    while cap.isOpened():
        start_time = time.time()
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)

        gray = preprocess_image(frame)
        faces = face_cascade.detectMultiScale(gray, 1.1, 6)

        command = '0'
        if len(faces) > 0:
            biggest_face = max(faces, key=lambda rect: rect[2] * rect[3])
            x, y, w, h = biggest_face
            face_center_x = x + w // 2
            face_center_y = y + h // 2
            cv2.circle(frame, (face_center_x, face_center_y), 2, (0, 255, 0), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)

            offset = face_center_x - screen_center_x
            last_detected_position = face_center_x

            if abs(offset) > intermediate_space:
                if offset > 0:
                    command = 'XFR'
                else:
                    command = 'XFL'
            elif abs(offset) > center_tolerance // 2:
                if offset > 0:
                    command = 'XR'
                else:
                    command = 'XL'
            else:
                command = 'C'

            rep_count = 0

            current_time = time.time()
            if current_time - last_sent_time > wait_time:
                ArduinoSerial.write((command + '\n').encode('utf-8'))
                last_sent_time = current_time
                print("comandito: " + command)
        else:
            if last_detected_position is not None and rep_count < 5:
                if last_detected_position < screen_center_x:
                    command = 'XL'
                else:
                    command = 'XR'
                current_time = time.time()
                if current_time - last_sent_time > wait_time:
                    ArduinoSerial.write((command + '\n').encode('utf-8'))
                    last_sent_time = current_time
                    rep_count += 1
                    print("rep: " + command)

        cv2.rectangle(frame, (0, 0), (screen_center_x - center_tolerance // 2, screen_height), (255, 0, 0), 2)
        cv2.rectangle(frame, (screen_center_x - center_tolerance // 2, 0), (screen_center_x + center_tolerance // 2, screen_height), (0, 255, 0), 2)
        cv2.rectangle(frame, (screen_center_x + center_tolerance // 2, 0), (screen_width, screen_height), (0, 0, 255), 2)

        cv2.imshow('img', frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

        time_to_wait = delay - (time.time() - start_time)
        if time_to_wait > 0:
            time.sleep(time_to_wait)

    cap.release()
    cv2.destroyAllWindows()
    ArduinoSerial.close()

facetracking()
