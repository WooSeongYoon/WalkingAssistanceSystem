from pymongo import MongoClient
from bson import Binary
from datetime import datetime

def DB_insert(lat, lng, status, image_path, loc, damage):
    # 연결
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
        "date": str(datetime.now()),
        "damege": damage
    }
    
    collection.insert_one(data)