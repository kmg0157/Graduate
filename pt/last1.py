import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from picamera2 import Picamera2
import cv2
import time
import RPi.GPIO as GPIO

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

#speedset = 17 # 직진
#speedSet = 14  # left and right

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

def main():
    picam2 = Picamera2()
    video_config = picam2.create_video_configuration(main={"format": 'XRGB8888', "size": (640, 480)})
    picam2.configure(video_config)
    picam2.start()

    carState = "stop"

    model_path = '/home/user/AI_CAR/lane_navigation_reeeefinal.h5'
    model = load_model(model_path)
    
    while(1):
        
        keValue = cv2.waitKey(1)
        
        if keValue == ord('q') :
            break
        elif keValue == 82 :
            print("go")
            carState = "go"
        elif keValue == 84 :
            print("stop")
            carState = "stop"
        
        frame = picam2.capture_array()
        image = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
        cv2.imshow('Original', image)
        
        preprocessed = img_preprocess(image)
        cv2.imshow('pre', preprocessed)
        
        X = np.asarray([preprocessed])
        steering_angle = int(model.predict(X)[0])
        print("predict angle:",steering_angle)
        
        if carState == "go":
            if steering_angle >= 80 and steering_angle <= 100:
                print("go")
                motor_go(20)
            elif steering_angle > 100 and steering_angle <121:
                print("right")
                motor_right(15)
            elif steering_angle <= 80 and steering_angle >65:
                print("left")
                motor_left(15)
                
            elif steering_angle <65:
                print("left")
                motor_left(20)
            elif steering_angle >120:
                print("right")
                motor_right(20)
            
            
            
        elif carState == "stop":
            motor_stop()
        
    cv2.destroyAllWindows()
    
if __name__ == '__main__':
    main()
    GPIO.cleanup()