import json

class write_json:
    def __init__(self):
        self.file_path='gps.json'

    def save_data(self,client_socket):
        try:
            data = client_socket.recv(1024)
                
            # 수신한 데이터 파싱 (JSON 디코딩)
            decoded_data = data.decode('utf-8')
            gps_data = json.loads(decoded_data)

            # 수신한 GPS 데이터를 파일에 추가 저장
            with open(self.file_path, 'a+') as json_file:
                if json_file.tell() != 1:  # 파일이 비어있지 않으면\ 쉼표와 줄 바꿈 추가
                    json_file.write(',\n')
                json.dump(gps_data, json_file, indent=4)
                json_file.flush()

        except json.decoder.JSONDecodeError as e:
            pass
            
    def open_file(self):
        with open(self.file_path,'w') as json_file:
            json_file.write('[')

    def close_file(self):
        with open(self.file_path,'a+') as json_file:
            json_file.write(']\n')