from TCP_server import Server
from json_file import write_json

def main():
    TCP_server = Server()    #소켓 객체 생성
    write_data=write_json()       #json 파일 작성 객체 생성

    write_data.open_file()    #json 파일 오픈
    TCP_server.start_server()
    TCP_server.accept_socket()
    
    try:
        while True:        
            data = TCP_server.client_socket.recv(1024)
            decoded_data = data.decode('utf-8')
            print(decoded_data)
            if decoded_data=="CLOSE":
                break
            else:
                write_data.save_data(decoded_data)
        
    finally: 
        write_data.close_file()
        TCP_server.client_socket.close()

if __name__ == "__main__":
    main()