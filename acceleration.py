import smbus
import time
import matplotlib.pyplot as plt

# MPU6050 레지스터 주소
power_mgmt_1 = 0x6b
accel_x_out = 0x3b
accel_y_out = 0x3d
# accel_z_out = 0x3f  # Z 축 제거

# I2C 버스 생성
bus = smbus.SMBus(1)  # Raspberry Pi에서는 1번을 사용합니다. 만약 0번을 사용하는 경우, 0으로 변경합니다.

# 센서 초기화
def init_sensor():
    bus.write_byte_data(0x68, power_mgmt_1, 0)

# 가속도 값 읽기
def read_accel():
    def read_word(reg):
        high = bus.read_byte_data(0x68, reg)
        low = bus.read_byte_data(0x68, reg+1)
        val = (high << 8) + low
        return val if val < 0x8000 else val - 65536

    accel_x = read_word(accel_x_out)
    accel_y = read_word(accel_y_out)
    # accel_z = read_word(accel_z_out)  # Z 축 제거

    return accel_x, accel_y  # Z 축 제거

# 메인 함수
def main():
    init_sensor()

    # 데이터 저장 리스트
    x_data = []
    y_data = []

    start_time = time.time()  # 시작 시간

    try:
        while time.time() - start_time < 10:  # 10초 동안 데이터 읽기
            accel_x, accel_y = read_accel()
            print(f"Accelerometer: X={accel_x}, Y={accel_y}")

            # 데이터 저장
            x_data.append(accel_x)
            y_data.append(accel_y)

            time.sleep(0.1)  # 0.1초마다 데이터 샘플링

    except KeyboardInterrupt:
        pass  # Ctrl+C 입력시 종료

    # 그래프 그리기
    plt.plot(x_data, label='X-Axis')
    plt.plot(y_data, label='Y-Axis')
    plt.xlabel('Time')
    plt.ylabel('Acceleration')
    plt.legend()
    plt.savefig('acceleration_graph.png')  # 그래프를 이미지 파일로 저장

if __name__ == "__main__":
    main()
