from TCP_server import Server
from json_file import write_json

def main():
    TCP_server = Server()   #서버 소켓 객체 생성
    write_data=write_json() #json 파일 객체 생성

    write_data.open_file()    #json 파일 열기
    TCP_server.start_server()   #서버 소켓 생성
    TCP_server.accept_socket()  #클라이언트와 연결 수립
    
    try:
        while True:        
            data = TCP_server.client_socket.recv(1024)  #클라이언트로부터 최대 1024bytes 데이터 받기
            decoded_data = data.decode('utf-8') #데이터 디코딩
            print(decoded_data)
            if decoded_data=="CLOSE":   #클라이언트 종료 문자열 수신 시
                break
            else:
                write_data.save_data(decoded_data)  #전달받은 데이터 json 파일에 작성
        
    finally: 
        write_data.close_file() #json 파일 닫기
        TCP_server.client_socket.close()    #클라이언트 소켓 종료
        TCP_server.server_socket.close()    #서버 소켓 종료

if __name__ == "__main__":
    main()