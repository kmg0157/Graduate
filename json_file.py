import json

class write_json:
    def __init__(self):
        self.file_path='gps.json'   #json 파일 저장할 경로

    def save_data(self,decoded_data):   #json 파일 저장 함수
        
        gps_data = json.loads(decoded_data) # 수신한 데이터 파싱 (JSON 디코딩)
            
        # 수신한 GPS 데이터를 파일에 추가 저장
        with open(self.file_path, 'a+') as json_file:
            if json_file.tell() != 1:  # 파일이 비어있지 않으면 쉼표와 줄 바꿈 추가
                json_file.write(',\n')
            json.dump(gps_data, json_file, indent=4)    #데이터 작성
            
    def open_file(self):    #json 파일 열기 함수
        with open(self.file_path,'w') as json_file:
            json_file.write('[')

    def close_file(self):   #json 파일 닫기 함수
        with open(self.file_path,'a+') as json_file:
            json_file.write(']\n')