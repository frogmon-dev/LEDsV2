#-*- coding:utf-8 -*-

# 중복 실행 방지
from tendo import singleton
try:
    me = singleton.SingleInstance()
except:
    print("another process running!")
    exit()
    
import paho.mqtt.client as mqtt
import json
from frogmon.uCommon import COM
from frogmon.uGlobal import GLOB

configFileNM = COM.gHomeDir + COM.gSetupFile
controlFileNM = COM.gHomeDir + COM.gControlFile

mSvr_addr = GLOB.readConfig(configFileNM, 'MQTT', 'host_addr', 'frogmon.synology.me')
mSvr_port = GLOB.readConfig(configFileNM, 'MQTT', 'host_port', '8359')

user_id = GLOB.readConfig(configFileNM, 'SETUP', 'user_id', 'frogmon')
dev_id = GLOB.readConfig(configFileNM, 'AGENT', 'id', '0')

mSub_nm = "FARMs/Status/%s/#" % (user_id)
mPub_nm = "FARMs/Control/%s/%s" % (user_id, dev_id)

# MQTT 서버 정보
MQTT_BROKER = mSvr_addr
MQTT_PORT = int(mSvr_port)
MQTT_TOPIC = mSub_nm  # 하위 토픽을 모두 구독하기 위해 '#'을 사용

# 메시지를 수신했을 때 호출되는 콜백 함수
def on_message(client, userdata, message):
    message_payload = message.payload.decode()
    print(f"Received message '{message.payload.decode()}' on topic '{message.topic}'")
    # 토픽을 '/'로 분류
    topic_parts = message.topic.split('/')    
    # 센서 ID 값 추출 (4번째 값)
    if len(topic_parts) > 3:
        sensor_id = topic_parts[3]
        print(f"Sensor ID: {sensor_id}")
        # JSON 파일로 메시지 저장
        json_data = json.loads(message_payload)
        with open(f"{COM.gJsonDir}/{sensor_id}.json", "w") as json_file:
            json.dump(json_data, json_file, indent=4)
        print(f"Message saved to {sensor_id}.json")
    

# MQTT 클라이언트 생성
client = mqtt.Client()

# 메시지 수신 시 콜백 함수 설정
client.on_message = on_message

# MQTT 브로커에 연결
client.connect(MQTT_BROKER, MQTT_PORT)

# 토픽 구독
client.subscribe(MQTT_TOPIC)

# 메시지 루프 시작
client.loop_forever()
