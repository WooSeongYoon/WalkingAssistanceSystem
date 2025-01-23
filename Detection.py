import os
import cv2
import serial
import ultralytics
import DistanceDetection
import DB
import GPS

ser = serial.Serial("/dev/ttyAMA0", 115200)
model = ultralytics.YOLO('./BaseModel/11S_E100_1.0Ver/weights/best.pt')

classTxt = open('./classes.txt', 'r')
data = classTxt.read()
class_list = data.split('\n')
classTxt.close()

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)

MAX_DISTANCE = 1.0  # 탐지 최대 거리 = 1M
MIN_ACC = 0.6 # 최소 정확도 = 60%

def videoDetection(cap, model, class_list, ser, MIN_ACC, MAX_DISTANCE):
    while True:
        ret, frame = cap.read()
        if not ret:
            print('Cam Error')
            break

        detection = model(frame)[0]
        distance = DistanceDetection.readLidarData(ser, MAX_DISTANCE)
        print(distance)

        for data in detection.boxes.data.tolist():
            cross = False

            confidence = float(data[4])
            if confidence < MIN_ACC:
                continue

            label = class_list[int(data[5])]
            
            if (distance is not None):

                text = (f"전방에 {distance} 앞에 무엇인가 있습니다.")
                os.system(f'espeak "{text}"')


                if ((label == "Kickboard") or (label == "Bollard")):
                    text = (f"전방 {distance}앞에 {label}가 있습니다.")
                    os.system(f'espeak "{text}"')
            

            if (label == "Stairs"):
                text = ("전방에 계단이 있습니다.")
                os.system(f'espeak "{text}"')

            elif (label == "Crosswlk"):
                cross = True
                text = ("전방에 횡단보도가 있습니다.")
                os.system(f'espeak "{text}"')

            elif (label == "Broken Braille Sidewalk Blocks"):
                damage = True
                img = './saved_image.jpg'
                cv2.imwrite(img, frame)
                DB.DB_insert(GPS.get_GPS()[2], GPS.get_GPS()[3], label, img, GPS.get_GPS()[0], damage)
                
                text = "전방 보도블록 파손 확인"
                os.system(f'espeak "{text}"')
                
            elif (label == "Braille Sidewalk Blocks"):
                damage = False
                img = './saved_image.jpg'
                cv2.imwrite(img, frame)
                DB.DB_insert(GPS.get_GPS()[2], GPS.get_GPS()[3], label, img, GPS.get_GPS()[0], damage)
            
            if (cross == True):
                if (label == "Green Pedestirian Light"):
                    text = "초록불입니다."
                    os.system(f'espeak "{text}"')
                    print("초록불입니다.")
                elif (label == "Red Pedestrian Light"):
                    text = "빨간불입니다."
                    os.system(f'espeak "{text}"')
                    print("빨간불입니다.")

                print("정상임")

if __name__ == '__main__':
    videoDetection(cap, model, class_list, ser, MIN_ACC, MAX_DISTANCE)
