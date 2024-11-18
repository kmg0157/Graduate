import threading
import cv2
import RPi.GPIO as GPIO
import numpy as np
from tensorflow.keras.models import load_model
from picamera2 import Picamera2


PWMA = 16
AIN1 = 19
AIN2 = 26
PWMB = 13
BIN1 = 20
BIN2 = 21

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


dnn_model_path = '/home/user/OpencvDnn/models/frozen_inference_graph.pb'
dnn_config_path = '/home/user/OpencvDnn/models/ssd_mobilenet_v2_coco_2018_03_29.pbtxt'
net = cv2.dnn.readNetFromTensorflow(dnn_model_path, dnn_config_path)
classNames = {0: 'background',
              1: 'person', 2: 'bicycle', 3: 'car', 4: 'motorcycle', 5: 'airplane', 6: 'bus',
              7: 'train', 8: 'truck', 9: 'boat', 10: 'traffic light', 11: 'fire hydrant',
              13: 'stop sign', 14: 'parking meter', 15: 'bench', 16: 'bird', 17: 'cat',
              18: 'dog', 19: 'horse', 20: 'sheep', 21: 'cow', 22: 'elephant', 23: 'bear',
              24: 'zebra', 25: 'giraffe', 27: 'backpack', 28: 'umbrella', 31: 'handbag',
              32: 'tie', 33: 'suitcase', 34: 'frisbee', 35: 'skis', 36: 'snowboard',
              37: 'sports ball', 38: 'kite', 39: 'baseball bat', 40: 'baseball glove',
              41: 'skateboard', 42: 'surfboard', 43: 'tennis racket', 44: 'bottle',
              46: 'wine glass', 47: 'cup', 48: 'fork', 49: 'knife', 50: 'spoon',
              51: 'bowl', 52: 'banana', 53: 'apple', 54: 'sandwich', 55: 'orange',
              56: 'broccoli', 57: 'carrot', 58: 'hot dog', 59: 'pizza', 60: 'donut',
              61: 'cake', 62: 'chair', 63: 'couch', 64: 'potted plant', 65: 'bed',
              67: 'dining table', 70: 'toilet', 72: 'tv', 73: 'laptop', 74: 'mouse',
              75: 'remote', 76: 'keyboard', 77: 'cell phone', 78: 'microwave', 79: 'oven',
              80: 'toaster', 81: 'sink', 82: 'refrigerator', 84: 'book', 85: 'clock',
              86: 'vase', 87: 'scissors', 88: 'teddy bear', 89: 'hair drier', 90: 'toothbrush'}

def img_preprocess(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    image = cv2.resize(image, (200, 66))
    image = cv2.GaussianBlur(image, (3, 3), 0)
    image = image / 255
    return image

def dnn_thread():
    global frame, carState
    while True:
        if frame is not None:
            blob = cv2.dnn.blobFromImage(frame, size=(250, 250), swapRB=True)
            net.setInput(blob)
            detections = net.forward()
            for detection in detections[0, 0, :, :]:
                confidence = detection[2]
                if confidence > .6:
                    class_id = int(detection[1])
                    class_name=id_class_name(class_id, classNames)
                    if class_name == "person":
                        carState = "stop"
                        break

def main():
    global frame, carState
    frame = None
    carState = "stop"

    picam2 = Picamera2()
    video_config = picam2.create_video_configuration(main={"format": 'XRGB8888', "size": (640, 480)})
    picam2.configure(video_config)
    picam2.start()

    model_path = '/home/user/AI_CAR/lane_navigation_final.h5'
    model = load_model(model_path)

    dnn_process = threading.Thread(target=dnn_thread)
    dnn_process.start()

    try:
        while True:
            keyValue = cv2.waitKey(1)
            if keyValue == ord('q'):
                break
            elif keyValue == 82:
                carState = "go"
            elif keyValue == 84:
                carState = "stop"
                
            frame = picam2.capture_array()
            image = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
            preprocessed = img_preprocess(image)

            X = np.asarray([preprocessed])
            predictions = model.predict(X)
            
            if predictions.size > 0:
                steering_angle = int(predictions[0][0])
            else:
                steering_angle = 0

            if carState == "go":
                if steering_angle >= 70 and steering_angle <= 110:
                    motor_go(20)
                elif steering_angle > 110:
                    motor_right(18)
                elif steering_angle < 70:
                    motor_left(18)
            elif carState == "stop":
                motor_stop()

            cv2.imshow('Camera View', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        cv2.destroyAllWindows()
        GPIO.cleanup()
        picam2.stop_preview()

if __name__ == '__main__':
    main()                