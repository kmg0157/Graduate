import socket
import json

# 서버 설정
host = '0.0.0.0'  # 서버 IP 주소
port = 12345       # 포트 번호

# TCP 소켓 생성
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 소켓을 주소와 연결
s.bind((host, port))

# 클라이언트의 연결을 대기
s.listen(1)
print(f"서버가 {host}:{port}에서 대기 중...")

# 클라이언트 연결 수락
conn, addr = s.accept()
print(f"{addr}에서 연결됨")

# 클라이언트로부터 데이터 수신
received_data = conn.recv(1024).decode()

# 수신된 데이터를 JSON 형식으로 역직렬화
try:
    json_data = json.loads(received_data)
except json.JSONDecodeError:
    print("유효한 JSON 데이터가 아닙니다.")
else:
    # JSON 데이터를 파일로 저장
    with open('received_data.json', 'w') as file:
        json.dump(json_data, file, indent=4)
    print("JSON 파일로 저장되었습니다.")

# 연결 종료
conn.close()
