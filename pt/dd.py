from picamera2 import Picamera2
import cv2
import numpy as np
import RPi.GPIO as GPIO
import time

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

L_Motor = GPIO.PWM(PWMA, 150)
L_Motor.start(0)
R_Motor = GPIO.PWM(PWMB, 150)
R_Motor.start(0)

speedset = 14 # 직진
speedSet = 17  # left and right

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

def main():
    picam2 = Picamera2()
    video_config = picam2.create_video_configuration(main={"format": 'XRGB8888', "size": (640, 480)})
    picam2.configure(video_config)
    picam2.start()

    filepath = "/home/user/AI_CAR/video/test4/test"
    i = 0
    carState = "stop"

    try:
        while True:
            keyValue = cv2.waitKey(10)

            if keyValue == ord('q'):
                break
            elif keyValue == 82:
                carState = "go"
                motor_go(speedset)
            elif keyValue == 84:
                carState = "stop"
                motor_stop()
            elif keyValue == 81:
                carState = "left"
                motor_left(speedSet)
            elif keyValue == 83:
                carState = "right"
                motor_right(speedSet)

            frame = picam2.capture_array()
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
            cv2.imshow('Original', frame_bgr)

            height = frame_bgr.shape[0]
            save_image = frame_bgr[int(height/2):,:,:]
            save_image = cv2.cvtColor(save_image, cv2.COLOR_BGR2YUV)
            save_image = cv2.resize(save_image, (200,66))
            save_image = cv2.GaussianBlur(save_image, (3,3), 0)
            #_, save_image = cv2.threshold(save_image, 160,255,cv2.THRESH_BINARY_INV)
            cv2.imshow('Save', save_image)

            if carState in ["left", "right", "go"]:
            
                angle = 90 if carState == "go" else 45 if carState == "left" else 135
                cv2.imwrite(f"{filepath}_{i:05d}_{angle:03d}.png", save_image)
                i += 1

    finally:
        cv2.destroyAllWindows()
        picam2.stop()
        GPIO.cleanup()

if __name__ == '__main__':
    main()

