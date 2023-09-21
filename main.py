from TCP_server import start_server, accept_client
from json_file_make import write_json
import socket

# 서버 설정
host = '0.0.0.0'  # 모든 네트워크 인터페이스에서 접속 허용
port = 12345

def main():
    server_socket = start_server(host, port)    #소켓 객체 생성
    data=write_json()       #json 파일 작성 객체 생성

    data.open_file()    #json 파일 오픈

    try:
        while True:
            comm_socket = accept_client(server_socket)

            try:
                data.save_data(comm_socket)
            except socket.error as e:
                comm_socket.close()
                break
        
    except KeyboardInterrupt:
        pass    

    data.close_file()
    server_socket.close()

if __name__ == "__main__":
    main()