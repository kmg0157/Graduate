import socket

class Client:
    def __init__(self):
        self.host='192.168.0.151'   #서버 IP 주소
        self.port=12345 #서버 port No.
        self.client_socket=None #클라이언트 소켓 변수

    def accept(self):   #서버 접속 요청 함수
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #클라이언트 소켓 생성
        self.client_socket.connect((self.host, self.port))  #클라이언트 소켓을 서버에 접속 요청

    def run_client(self,data):  #클라이언트 실행 함수
        self.client_socket.sendall(data)    #데이터를 서버로 전송
    
        if data=='CLOSE':   #키보드 인터럽트 발생 시(ctrl+c)
            print('close socket')
            self.client_socket.close()  #클라이언트 소켓 종료
