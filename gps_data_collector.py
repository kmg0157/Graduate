#gps 데이터를 읽고 처리하는 라이브러리인 gpsd 사용
#WATCH_ENABLE: gpsd 활성화하고 gps데이터 읽기 제공
#WATCH_NEWSTYLE: 최신 gps 데이터 읽기 제공

from gps import gps, WATCH_ENABLE, WATCH_NEWSTYLE   
import time
class data_collector:
    def __init__(self):
        self.gpsd = gps(mode=WATCH_ENABLE | WATCH_NEWSTYLE)    #gps 정보 읽기 위한 변수
        self.row_num = 1    #sequence 넘버 변수

    def get_position_data(self):    #gps 위치 정보 얻는 함수
        nx = self.gpsd.next()   #next()를 통해 다음 데이터 반환
        
        if nx['class'] == 'TPV':    #gps 데이터 중 TPV(Time-Position-Velocity)를 사용
            latitude = getattr(nx, 'lat', "Unknown")    #위도 정보 문자열로 저장
            longitude = getattr(nx, 'lon', "Unknown")   #경도 정보 문자열로 저장
            timestamp = int(time.time())    #unix 타임

            #데이터 형식
            data = {
                "Sequence": self.row_num,
                "Timestamp": timestamp,
                "Latitude": latitude,
                "Longitude": longitude
            }

            self.row_num += 1   #데이터가 추가될 때 마다 Sequence 넘버 1씩 증가
            return data #선언한 데이터 반환