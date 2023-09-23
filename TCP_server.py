import socket

class Server:
    def __init__(self):
        self.host='192.168.0.151'
        self.port=12345
        self.server_socket=None
        self.client_socket=None
        
    def start_server(self):
        # 서버 소켓 생성
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()  # 최대 1개의 연결까지 대기

        print("서버가 시작되었습니다. 대기 중...")

    def accept_socket(self):
        self.client_socket, client_address = self.server_socket.accept()
        print(f"클라이언트가 연결되었습니다. 주소: {client_address}")

            
