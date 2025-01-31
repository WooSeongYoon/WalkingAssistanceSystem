import os
import subprocess
import time
import cv2
import serial
from ultralytics import YOLO
import DistanceDetection
import DB
import gps_test05 as GPS

# Initialize
ser = serial.Serial("/dev/ttyAMA0", 115200)
model = YOLO('./best.pt')

with open('./classes.txt', 'r') as classTxt:
    class_list = classTxt.read().splitlines()

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)

MAX_DISTANCE = 1.0  # 최대 감지 거리(미터)
MIN_ACC = 0.7       # 최소 정확도
DELAY_SECONDS = 2   #

def text_to_speech(message):
    """
    텍스트 음성 변환 함수 (음성이 출력될 때까지 대기)
    subprocess를 사용하여 동기식으로 음성 출력이 완료될 때까지 대기
    """
    try:
        # espeak로 음성을 출력하고, 완료될 때까지 기다림
        subprocess.run(['espeak', message], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while speaking: {e}")

def save_image_and_location(frame, label):
    """
    이미지 저장 및 GPS 정보 추가.
    """
    img_path = './saved_image.jpg'
    cv2.imwrite(img_path, frame)
    lat, lng = GPS.get_GPS()
    print(lat, lng)
    road_address, jibun_address = GPS.get_address_from_GPS(lat, lng)
    address = jibun_address + " " + road_address
    DB.DB_Update(lat, lng, label, img_path, address, label == "Broken Braille Sidewalk Blocks")
    
def videoDetection():
    while True:
        ret, frame = cap.read()
        if not ret:
            print('Camera Error')
            break

        detection = model(frame)[0]
        distance = DistanceDetection.readLidarData(ser, MAX_DISTANCE)
        print(f"Distance: {distance}")

        for data in detection.boxes.data.tolist():
            confidence = float(data[4])
            if confidence < MIN_ACC:
                continue

            label = class_list[int(data[5])]
            print(f"Detected: {label}, Confidence: {confidence}, Distance: {distance}")
            
            # 특정 거리에 있는 위험 객체 식별
            if distance is not None:
                if label in ["Kickboard", "Bollard"]:
                    text_to_speech(f"{label}")
                else:
                    text_to_speech(f"{distance}")
            
            # 2D라이다로 거리측정 못하는 객체
            if label == "Stairs":
                text_to_speech("Stairs ahead.")
            elif label == "Crosswalk":
                text_to_speech("Crosswalk ahead.")
                if "Green Pedestrian Light" in label:
                    text_to_speech("Green Light")
                elif "Red Pedestrian Light" in label:
                    text_to_speech("Red Light")

            elif label == "Broken Braille Sidewalk Blocks" or label == "Braille Sidewalk Blocks":
                save_image_and_location(frame, label)
                text_to_speech(f"{label} detected.")

            elif label == "Broken Bollard" or label == "Bollard":
                save_image_and_location(frame, label)
                
        # 간격을 두고 반복하여 계속 처리
        time.sleep(DELAY_SECONDS)

if __name__ == '__main__':
    try:
        videoDetection()
    except KeyboardInterrupt:
        print("Program interrupted by user.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
