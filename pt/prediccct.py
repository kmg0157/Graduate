import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from picamera2 import Picamera2
import cv2
import time
from picamera.array import PiRGBArray


def img_preprocess(image):
    height, _, _ = image.shape
    image = image[int(height/2):,:,:]  
    image = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)  
    image = cv2.GaussianBlur(image, (3,3), 0)  
    image = cv2.resize(image, (200,66))  
    image = image / 255  
    return image

def main():
    camera = Picamera2()
    camera.resolution = (640, 480)
    camera.framerate = 32
    time.sleep(0.1)

    model_path = '/home/user/AI_CAR/lane_navigation_final1(4.28).h5'
    model = load_model(model_path)

    rawCapture = PiRGBArray(camera, size=(640, 480))

    try:
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            image = frame.array
            image = cv2.flip(image,-1)
            cv2.imshow('Original', image)
        
            preprocessed = img_preprocess(image)
            cv2.imshow('pre', preprocessed)

            X = np.asarray([preprocessed])
            steering_angle = int(model.predict(X)[0])
            print("predict angle:", steering_angle)

            rawCapture.truncate(0)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
    GPIO.cleanup()
