import RPi.GPIO as GPIO

# GPIO 핀 번호 설정
GPIO.setmode(GPIO.BCM)

try:
    # 모든 GPIO 핀에 대해 반복
    for pin in range(2, 28):  # 라즈베리 파이의 GPIO 핀은 2부터 27까지 있습니다.
        # 해당 핀을 입력 모드로 설정
        GPIO.setup(pin, GPIO.IN)
        # GPIO 핀 상태 읽기
        input_state = GPIO.input(pin)
        # GPIO 핀의 상태 출력
        print("GPIO 핀 {}의 상태: {}".format(pin, input_state))

finally:
    # 프로그램 종료 시 GPIO 리소스 해제
    GPIO.cleanup()
