import base64
import os
from bson import json_util
from pymongo import MongoClient
from flask import Flask, render_template, request, redirect, flash
from werkzeug.utils import secure_filename
import ultralytics

app = Flask(__name__)

# MongoDB 클라이언트 설정
client = MongoClient('mongodb+srv://21928296:n9Dx8ngcU2pD0lyj@database.2vxog.mongodb.net/?retryWrites=true&w=majority&appName=database')
db = client['database']
collection = db['myCollection']

# 파일 업로드 폴더 설정
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# YOLO 모델 로드
try:
    model = ultralytics.YOLO('./BaseModel/11S_E100_1.0Ver/weights/best.pt')  # 모델 경로 확인
except Exception as e:
    print(f"Error loading YOLO model: {e}")

# 업로드 폴더가 없으면 생성
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    return render_template('index04.html')

@app.route('/get_marker_data', methods=['GET'])
def get_marker_data():
    data = []
    for doc in collection.find():
        image_data = doc.get('image', None)

        if image_data:
            image_data = base64.b64encode(image_data).decode('utf-8')
            image_data = f"data:image/jpeg;base64,{image_data}"

        data.append({
            'lat': doc.get('lat'),
            'lng': doc.get('lng'),
            'status': doc.get('status'),
            'image': image_data,
            'loc': doc.get('loc'),
            'date': doc.get('date')
        })

    return json_util.dumps(data)

@app.route('/upload_broken_image', methods=['GET', 'POST'])
def upload_broken_image():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or file.filename == '':
            flash('No file selected')
            return redirect(request.url)

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        try:
            # 파일 저장
            file.save(filepath)
        except Exception as e:
            flash(f"Error saving file: {e}")
            return redirect(request.url)

        try:
            # YOLO 모델로 파손 여부 재검사
            results = model(filepath)  # YOLO 모델 실행
            results.save()  # 결과 이미지 저장

            # 파손 여부 결과
            damaged_detected = any(label == 'damaged' for label in results.pandas().xyxy[0]['name'])

            if damaged_detected:
                message = "파손된 보도블럭이 감지되었습니다. 수리가 필요합니다."
            else:
                message = "보도블럭이 수리되었습니다."
                # 상태를 'Repair Braille Sidewalk Blocks'로 업데이트
                collection.find_one_and_update(
                    {"lat": request.form.get('lat'), "lng": request.form.get('lng')},
                    {"$set": {"status": "Repair Braille Sidewalk Blocks"}}
                )
                message += " 상태가 Repair Braille Sidewalk Blocks로 변경되었습니다."
            
            return render_template('result.html', message=message, result_image=filename)
        
        except Exception as e:
            flash(f"Error processing image with YOLO: {e}")
            return redirect(request.url)

    return render_template('upload.html')

# 업로드 페이지 템플릿
@app.route('/upload.html')
def upload_page():
    return 

# 결과 페이지 템플릿
@app.route('/result.html')
def result_page():
    return 

if __name__ == '__main__':
    app.secret_key = 'supersecretkey'  # 플래시 메시지 표시를 위해 필요
    app.run(debug=True)
