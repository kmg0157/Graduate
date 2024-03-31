from gps_data_collector import data_collector
from json_file import write_json
from TCP_client import Client
from crash import crash_detect
import time
import json

def main():
    gps_data = data_collector() #gps 데이터 받는 객체 생성
    crash_sensor=crash_detect() #충돌 감지 객체 생성
    json_writer = write_json('/home/kang/Desktop/project/newoutput.json') #json 파일 객체 생성
    client_socket=Client()  #TCP 소켓 객체 생성
    client_socket.accept()  #TCP 서버 연결 요청

    #충돌 감지 시
    if crash_sensor.crash_detection()==1:
            print("Application started!")
            json_writer.initialize_json_file()  #json 파일 초기화 및 생성

            data = gps_data.get_position_data() #data 변수에 gps 데이터 저장
            if data:    #데이터가 존재할 경우
                json_data=json.dumps(data)      # 데이터 직렬화
                client_socket.run_client(json_data.encode('utf-8')) #데이터 인코딩
                json_writer.save_data_to_json(data) #gps 데이터를 json 파일에 저장
                #수신한 gps 정보 출력
                print("Sequence:", data["Sequence"], " Timestamp:", data["Timestamp"], " Latitude:", data["Latitude"], " Longitude:", data["Longitude"])

                #AWS 서버에 보내는 코드

                time.sleep(3)
                
                print("socket close")
                data="CLOSE"    #서버에 소켓이 닫혔다는 것을 알리는 메세지
                data=data.encode('utf-8')   #데이터 인코딩
                client_socket.run_client(data)  # "CLOSE" 데이터 서버로 전송
                crash_sensor.crash_cleanup()
            

            json_writer.close_json_file()   #json 파일 닫기


if __name__ == "__main__":
    main()
