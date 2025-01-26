# -*- coding:utf-8 -*-

# 중복 실행 방지
from tendo import singleton
import paho.mqtt.client as mqtt
import json
from frogmon.uCommon import COM
from frogmon.uGlobal import GLOB
import os
import time
import threading

# 중복 실행 방지
try:
    me = singleton.SingleInstance()
except:
    print("another process running!")
    exit()

# 환경설정 파일 경로
configFileNM = COM.gHomeDir + COM.gSetupFile

# 환경설정 값 읽기
def read_config_or_default(section, key, default):
    try:
        return GLOB.readConfig(configFileNM, section, key, default)
    except Exception as e:
        print(f"[ERROR] Failed to read config {section}:{key}: {e}")
        return default

# MQTT 브로커 정보
MQTT_BROKER = read_config_or_default('MQTT', 'host_addr', 'frogmon.synology.me')
MQTT_PORT = int(read_config_or_default('MQTT', 'host_port', '8359'))

# 사용자 및 장치 정보
user_id = read_config_or_default('SETUP', 'user_id', 'frogmon')
dev_id = read_config_or_default('AGENT', 'id', '0')

# MQTT 토픽 설정
MQTT_TOPIC = f"FARMs/Status/{user_id}/#"
MQTT_PUB_TOPIC = f"FARMs/Control/{user_id}/{dev_id}"
MQTT_PUB_TOPIC_STATUS = f"FARMs/Status/{user_id}/{dev_id}"

# 메시지 저장 함수
def save_message_as_json(sensor_id, message_payload):
    try:
        json_data = json.loads(message_payload)
        json_file_path = os.path.join(COM.gJsonDir, f"{sensor_id}.json")
        with open(json_file_path, "w") as json_file:
            json.dump(json_data, json_file, indent=4)
        print(f"Message saved to {json_file_path}")
    except json.JSONDecodeError:
        print(f"[ERROR] Invalid JSON format: {message_payload}")
    except Exception as e:
        print(f"[ERROR] Failed to save message: {e}")

# 메시지 수신 콜백
def on_message(client, userdata, message):
    try:
        message_payload = message.payload.decode()
        print(f"Received message '{message_payload}' on topic '{message.topic}'")
        # 토픽에서 센서 ID 추출
        topic_parts = message.topic.split('/')
        if len(topic_parts) > 3:
            sensor_id = topic_parts[3]
            print(f"Sensor ID: {sensor_id}")
            # 메시지 저장
            save_message_as_json(sensor_id, message_payload)
    except Exception as e:
        print(f"[ERROR] Error in message processing: {e}")

# MQTT 연결 재시도 함수
def connect_with_retry(client, broker, port, max_retries=5):
    for attempt in range(max_retries):
        try:
            client.connect(broker, port)
            print(f"Connected to MQTT broker {broker}:{port}")
            return
        except Exception as e:
            print(f"[ERROR] Failed to connect to MQTT broker: {e}")
            time.sleep(5)
    print("[ERROR] Exceeded maximum connection attempts")
    exit()

# 1분마다 메시지 발행
def publish_every_minute(client, topic):
    payload = {"house system": "on"}
    try:
        client.publish(topic, json.dumps(payload))
        print(f"Published: {payload} to topic {topic}")
    except Exception as e:
        print(f"[ERROR] Failed to publish message: {e}")
    threading.Timer(60, publish_every_minute, args=(client, topic)).start()

# MQTT 클라이언트 설정 및 실행
def main():
    # MQTT 클라이언트 생성
    client = mqtt.Client()

    # 메시지 수신 콜백 설정
    client.on_message = on_message

    # MQTT 브로커 연결
    connect_with_retry(client, MQTT_BROKER, MQTT_PORT)

    # 토픽 구독
    client.subscribe(MQTT_TOPIC)
    print(f"Subscribed to topic: {MQTT_TOPIC}")

    # 1분마다 메시지 발행 시작
    publish_every_minute(client, MQTT_PUB_TOPIC_STATUS)

    # 메시지 루프 시작
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("Program terminated by user")
    except Exception as e:
        print(f"[ERROR] MQTT client loop error: {e}")

if __name__ == "__main__":
    main()
