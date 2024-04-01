import RPi.GPIO as GPIO  # Raspberry Pi GPIO 라이브러리 사용
import time

# GPIO 핀 번호 설정
sensor_pin = 17

count=1
# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor_pin, GPIO.IN)

try:
    while True:
        # 센서 감지 확인
        time.sleep(0.05)
        if GPIO.input(sensor_pin) == GPIO.HIGH:
            print("진동이 감지되었습니다!")
            break
        else:
            print(count)
            count=count+1

except KeyboardInterrupt:
    # 프로그램 종료 시 GPIO 정리
    GPIO.cleanup()
