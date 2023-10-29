from TCP_server import Server
from json_file import write_json
from gps_db import Database
from show_gps import Map

def main():
    TCP_server = Server()   #서버 소켓 객체 생성
    write_data=write_json() #json 파일 객체 생성
    save_db=Database()  #DB 저장 객체 생성
    m=Map()

    write_data.open_file()    #json 파일 열기
    TCP_server.start_server()   #서버 소켓 생성
    TCP_server.accept_socket()  #클라이언트와 연결 수립
    save_db.connect_db()    #DB 연결

    mark=0

    try:
        while True:        
            data = TCP_server.client_socket.recv(1024)  #클라이언트로부터 최대 1024bytes 데이터 받기
            decoded_data = data.decode('utf-8') #데이터 디코딩
            print(decoded_data) # 전달 받은 데이터 출력
            if decoded_data=="CLOSE":   #클라이언트 종료 문자열 수신 시
                break
            else:
                write_data.save_data(decoded_data)  #전달받은 데이터 json 파일에 작성
                save_db.save_data(decoded_data) #DB에 데이터 저장
                if mark<1:
                    m.read_data(decoded_data)
                    m.show_map()
                    mark+=1

    finally: 
        write_data.close_file() #json 파일 닫기
        save_db.close_db()  #DB 연결 종료
        TCP_server.client_socket.close()    #클라이언트 소켓 종료
        TCP_server.server_socket.close()    #서버 소켓 종료

if __name__ == "__main__":
    main()