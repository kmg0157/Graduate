import socket

def start_server(host, port):
    # 서버 소켓 생성
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)  # 최대 1개의 연결까지 대기

    print("서버가 시작되었습니다. 대기 중...")

    return server_socket

def accept_client(server_socket):
    # 클라이언트 연결 대기
    client_socket, client_address = server_socket.accept()
    print(f"클라이언트가 연결되었습니다. 주소: {client_address}")

    return client_socket
