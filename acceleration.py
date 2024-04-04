import smbus
import time
import matplotlib.pyplot as plt

# MPU6050 레지스터 주소
class Acceleration():
    def __init__(self):
        self.power_mgmt_1=0x6b
        self.accel_x_out = 0x3b
        self.accel_y_out = 0x3d
        self.x_data=[]
        self.y_data=[]
        # I2C 버스 생성
        self.bus = smbus.SMBus(1)
    
    # 센서 초기화
    def init_sensor(self):
        self.bus.write_byte_data(0x68, self.power_mgmt_1, 0)
    
    # 가속도 값 읽기
    def read_accel(self):
        def read_word(reg):
            high = self.bus.read_byte_data(0x68, reg)
            low = self.bus.read_byte_data(0x68, reg+1)
            val = (high << 8) + low
            return val if val < 0x8000 else val - 65536

        accel_x = read_word(self.accel_x_out)
        accel_y = read_word(self.accel_y_out)

        return accel_x, accel_y

    # 데이터 저장
    def save_data(self):
        start_time=time.time()

        try:
            while time.time()-start_time<10:
                self.accel_x_out,self.accel_y_out=self.read_accel()
                print(f"Accelerometer: X={self.accel_x}, Y={self.accel_y}")

                # 데이터 저장
                self.x_data.append(self.accel_x)
                self.y_data.append(self.accel_y)

                time.sleep(0.1)  # 0.1초마다 데이터 샘플링

        except KeyboardInterrupt:
            pass  # Ctrl+C 입력시 종료

    # 그래프를 이미지 파일로 저장
    def show_data(self):
        plt.plot(self.x_data, label='X-Axis')
        plt.plot(self.y_data, label='Y-Axis')
        plt.xlabel('Time')
        plt.ylabel('Acceleration')
        plt.legend()
        plt.savefig('acceleration_graph.png')  


    #가속도 값을 이용한 충격 감지(수정 필요)
    def detect_collision(self,threshold=5000, duration=5):
        self.init_sensor()
        start_time = time.time()

        accel_x_prev, accel_y_prev = self.read_accel()
        while time.time() - start_time < duration:
            accel_x, accel_y = self.read_accel()
            
            # 가속도 변화량 계산
            delta_x = abs(accel_x - accel_x_prev)
            delta_y = abs(accel_y - accel_y_prev)

            # 가속도 변화량이 임계값을 초과하는지 확인
            if delta_x > threshold or delta_y > threshold:
                print("Collision detected!")
                return True

            accel_x_prev, accel_y_prev = accel_x, accel_y

        print("No collision detected.")
        return False
