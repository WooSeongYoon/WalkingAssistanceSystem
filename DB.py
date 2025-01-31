from pymongo import MongoClient
from bson import Binary
from datetime import datetime
import os
import gps_test05 as GPS
import cv2
     
def DB_Update(lat, lng, status, image_path, loc, damage):
    """
    MongoDB 튜플 업데이트
    """
    try:
        # 이미지 경로 확인
        if not os.path.isfile(image_path):
            print(f"Image file not found: {image_path}")
            return False

        # MongoDB 연결
        client = MongoClient(f"mongodb+srv://21928296:n9Dx8ngcU2pD0lyj@database.2vxog.mongodb.net/?retryWrites=true&w=majority&appName=database")
        db = client['database']
        collection = db['myCollection']  # 사용할 컬렉션 선택

        with open(image_path, 'rb') as image_file:
            binary_image = Binary(image_file.read())

        data = {
            "lat": lat,
            "lng": lng,
            "status": status,
            "image": binary_image,
            "loc": loc,
            "date": datetime.now().isoformat(),
            "damage": damage
        }

        collection.update_one(
            {"lat": lat, "lng": lng},  # 기존의 튜플 확인
            {"$set": data},            # Update 내용
            upsert=True                # 일치하는 항목이 없는 경우 삽입
        )
        print("Data inserted successfully.")
        return True
        
    except Exception as e:
        print(f"Database insert error: {e}")
        return False