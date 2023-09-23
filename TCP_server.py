import socket

class Server:
    def __init__(self):
        self.host='0.0.0.0'   #모든 클라이언트 접속 허용
        self.port=12345 #port No.
        self.server_socket=None #서버 소켓 변수
        self.client_socket=None #클라이언트와 통신하는 소켓 변수
        
    def start_server(self): # 서버 소켓 생성 함수
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #서버 소켓 생성
        self.server_socket.bind((self.host, self.port)) #소켓 바인딩
        self.server_socket.listen()  # 클라이언트 요청 대기

        print("서버가 시작되었습니다. 대기 중...")

    def accept_socket(self):    #클라이언트 연결 수립 함수
        self.client_socket, client_address = self.server_socket.accept()    #클라이언트와 통신 소켓 생성
        print(f"클라이언트가 연결되었습니다. 주소: {client_address}")

            
