from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import json

# AWS IoT Core에 등록된 Thing의 엔드포인트와 인증 정보 설정
host = "your-aws-iot-endpoint.iot.region.amazonaws.com"
rootCAPath = "root-CA.crt"
certificatePath = "your-certificate.pem.crt"
privateKeyPath = "your-private.pem.key"
clientId = "your-client-id"
topic = "your-topic"

# AWS IoT MQTT 클라이언트 생성
mqttClient = AWSIoTMQTTClient(clientId)
mqttClient.configureEndpoint(host, 8883)
mqttClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# 연결 시도
mqttClient.connect()

# 데이터 생성 및 전송
while True:
    data = {
        "temperature": 25.5,
        "humidity": 60
    }
    payload = json.dumps(data)
    mqttClient.publish(topic, payload, 1)
    print("Published: " + payload)
    time.sleep(5)  # 5초마다 데이터 전송

# 연결 종료
mqttClient.disconnect()
