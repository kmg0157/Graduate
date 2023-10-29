import json

class write_json:
    def __init__(self, file_path):
        self.file_path = file_path  #파일 경로
        self.data=''    #데이터

    def save_data_to_json(self, data):  #데이터 저장 함수
        with open(self.file_path, "a+") as file_object: 
            if data["Sequence"] > 1:
                file_object.write(",\n")    
            json.dump(data, file_object, indent=4)  #json 파일에 데이터 작성

    def initialize_json_file(self): #json 파일 생성 및 초기화 함수
        with open(self.file_path, 'w') as file_object:
            file_object.write("[")

    def close_json_file(self):  #json 파일 닫기 함수
        with open(self.file_path, "a+") as file_object:
            file_object.write("]\n")