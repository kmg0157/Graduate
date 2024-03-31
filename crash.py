#충돌 감지 모듈 사용(충돌 유무만 판단)
import RPi.GPIO as GPIO 

#충돌 감지 부분 객체 생성
class crash_detect:
    def __init__(self):
        # GPIO 핀 번호 설정
        self.sensor_pin=17

        # GPIO 설정 
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.sensor_pin, GPIO.IN)
    
    #충돌 감지 함수
    def crash_detection(self):
        while True:
            if GPIO.input(self.sensor_pin) == GPIO.HIGH:
                return 1
            else:
                return 0
                
    #GPIO 정리 함수            
    def crash_cleanup(self):
        GPIO.cleanup()
