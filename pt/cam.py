import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from picamera2 import Picamera2
import cv2
import time
import RPi.GPIO as GPIO
import socket
import struct
import pickle
import threading

# 모터 제어 핀 설정
PWMA = 16
AIN1 = 19
AIN2 = 26
PWMB = 13
BIN1 = 20
BIN2 = 21

# GPIO 설정 초기화
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)
GPIO.setup(PWMB, GPIO.OUT)

L_Motor = GPIO.PWM(PWMA, 200)
L_Motor.start(0)
R_Motor = GPIO.PWM(PWMB, 200)
R_Motor.start(0)

# 모터 제어 함수 정의
def motor_go(speed):
    L_Motor.ChangeDutyCycle(speed)
    GPIO.output(AIN2, False)
    GPIO.output(AIN1, True)
    R_Motor.ChangeDutyCycle(speed)
    GPIO.output(BIN2, False)
    GPIO.output(BIN1, True)

def motor_stop():
    L_Motor.ChangeDutyCycle(0)
    GPIO.output(AIN2, False)
    GPIO.output(AIN1, False)
    R_Motor.ChangeDutyCycle(0)
    GPIO.output(BIN2, False)
    GPIO.output(BIN1, False)

def motor_left(speed):
    L_Motor.ChangeDutyCycle(0)
    GPIO.output(AIN2, False)
    GPIO.output(AIN1, True)
    R_Motor.ChangeDutyCycle(speed)
    GPIO.output(BIN2, True)
    GPIO.output(BIN1, False)

def motor_right(speed):
    L_Motor.ChangeDutyCycle(speed)
    GPIO.output(AIN2, True)
    GPIO.output(AIN1, False)
    R_Motor.ChangeDutyCycle(0)
    GPIO.output(BIN2, False)
    GPIO.output(BIN1, True)

def img_preprocess(image):
    height, _, _ = image.shape
    image = image[int(height/2):,:,:]
    image = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    image = cv2.GaussianBlur(image, (3,3), 0)
    image = cv2.resize(image, (200,66))
    image = image / 255
    return image

class CarController(threading.Thread):
    def __init__(self, model_path):
        super(CarController, self).__init__()
        self.picam2 = Picamera2()
        video_config = self.picam2.create_video_configuration(main={"format": 'RGB888', "size": (640, 480)})
        self.picam2.configure(video_config)
        self.picam2.start()

        self.carState = "stop"
        self.model = load_model(model_path)
        self.steering_angle = 90

    def run(self):
        while True:
            keValue = cv2.waitKey(1)
            if keValue == ord('q'):
                break
            elif keValue == 82:
                print("go")
                self.carState = "go"
            elif keValue == 84:
                print("stop")
                self.carState = "stop"

            frame = self.picam2.capture_array()
            image = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
            cv2.imshow('Original', image)

            preprocessed = img_preprocess(image)
            cv2.imshow('pre', preprocessed)

            X = np.asarray([preprocessed])
            self.steering_angle = int(self.model.predict(X)[0])
            print("predict angle:", self.steering_angle)

            if self.carState == "go":
                if 80 <= self.steering_angle <= 97:
                    print("go")
                    motor_go(20)
                elif 97 < self.steering_angle < 121:
                    print("right")
                    motor_right(18)
                elif 65 < self.steering_angle <= 80:
                    print("left")
                    motor_left(18)
                elif self.steering_angle <= 65:
                    print("left")
                    motor_left(24)
                elif self.steering_angle >= 120:
                    print("right")
                    motor_right(24)
            elif self.carState == "stop":
                motor_stop()
        self.picam2.stop()
        cv2.destroyAllWindows()

class VideoStreamer(threading.Thread):
    def __init__(self, picam2, server_cam):
        super(VideoStreamer, self).__init__()
        self.picam2 = picam2
        self.server_cam = server_cam

    def run(self):
        try:
            while True:
                cmd_byte = self.server_cam.recv(1)
                if not cmd_byte:
                    break
                cmd = struct.unpack('!B', cmd_byte)
                if cmd[0] == 12:
                    frame_bgr = self.picam2.capture_array()
                    _, frame_encoded = cv2.imencode('.jpg', frame_bgr)
                    data = pickle.dumps(frame_encoded)
                    data_size = struct.pack("!L", len(data))
                    self.server_cam.sendall(data_size + data)
        finally:
            self.server_cam.close()

def main():
    HOST = ''  # 모든 인터페이스에서 수신
    PORT = 8096

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')

    server.bind((HOST, PORT))
    print('Socket bind complete')

    server.listen(10)
    print('Socket now listening')

    server_cam, addr = server.accept()
    print('New client connected:', addr)

    model_path = '/home/user/AI_CAR/lane_navigation_final.h5'
    car_controller = CarController(model_path)
    car_controller.start()

    video_streamer = VideoStreamer(car_controller.picam2, server_cam)
    video_streamer.start()

    car_controller.join()
    video_streamer.join()

    server.close()
    GPIO.cleanup()

if __name__ == '__main__':
    main()
