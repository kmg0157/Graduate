import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from picamera2 import Picamera2
import cv2
import time


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
    video_config = picam2.create_video_configuration(main={"format": 'XRGB8888',"size":(640, 480)})
    picam2.configure(video_config)
    picam2.start()

    carState = "stop"

    model_path = '/home/user/AI_CAR/lane_navigation_final1(4.28).h5'
    model = load_model(model_path)

    try:
        while True:
            frame = picam2.capture_array()
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
            cv2.imshow('Original', frame_bgr)

            height = frame_bgr.shape[0]
            save_image = frame_bgr[int(height/2):,:,:]
            save_image = cv2.cvtColor(save_image, cv2.COLOR_BGR2YUV)
            save_image = cv2.GaussianBlur(save_image, (3,3), 0)
            save_image = cv2.resize(save_image, (200, 66))
            cv2.imshow('Save', save_image)

            preprocessed = img_preprocess(image)
            cv2.imshow('pre', preprocessed)

            X = np.asarray([preprocessed])
            steering_angle = int(model.predict(X)[0])
            print("predict angle:", steering_angle)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
