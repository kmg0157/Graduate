import pymysql
import json

class Database:
    def __init__(self):
        self.conn=None
        self.cur=None
        self.sequence=0

    # 생성해둔 DB 접속
    def connect_db(self):
        self.conn=pymysql.connect(host="localhost",port=3306,user="root",password="0157",db="gpsdb",charset="utf8")   #DB 연결
        self.cur=self.conn.cursor() #커서 생성

    # 데이터 삽입 쿼리 실행
    def save_data(self,data):
        parshed_data=json.loads(data)  #데이터 파싱
        #데이터 저장
        insert_query = "INSERT INTO data (Sequence, Timestamp, Latitude, Longitude) VALUES (%s, %s, %s, %s)"
        self.cur.execute(insert_query, (parshed_data["Sequence"], parshed_data["Timestamp"], parshed_data["Latitude"], parshed_data["Longitude"]))
        

    # DB 연결 종료
    def close_db(self):
        self.conn.commit()  #테이블 변경사항 저장
        self.cur.close()    #커서 종료
        self.conn.close()   #DB 접속 종료