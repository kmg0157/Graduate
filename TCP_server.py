import socket
import json

class Server:
    def __init__(self):
        self.host='0.0.0.0'
        self.port=12345
        self.data=''

    def run_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        client_socket, addr = server_socket.accept()

        try:
            while True:
                received_data = client_socket.recv(1024)
                if not received_data:
                    break
                
                self.data=json.loads(received_data.decode())
                print("Received data:", self.data)

        except KeyboardInterrupt:
            print('서버 종료')

        finally:
            client_socket.close()


