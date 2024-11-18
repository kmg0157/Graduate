import socket
import struct
import pickle
from picamera2 import Picamera2
import cv2

HOST = '' 
PORT = 8096

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

server.bind((HOST, PORT))
print('Socket bind complete')

server.listen(10)
print('Socket now listening')

server_cam, addr = server.accept()
print('New client connected:', addr)


picam2 = Picamera2()
video_config = picam2.create_video_configuration(main={"format": 'RGB888', "size": (640, 480)})
picam2.configure(video_config)
picam2.start()


try:
    while True:
        cmd_byte = server_cam.recv(1)
        if not cmd_byte:
            break
        cmd = struct.unpack('!B', cmd_byte)

        if cmd[0] == 12:
            frame_bgr = picam2.capture_array()
            
             
            
        
            
            
            _, frame_encoded = cv2.imencode('.jpg', frame_bgr)
            data = pickle.dumps(frame_encoded)
            
            
            data_size = struct.pack("!L", len(data))
            server_cam.sendall(data_size + data)
finally:
    server_cam.close()
    server.close()
    picam2.stop()
    cv2.destroyAllWindows()
    print('Connection closed')

