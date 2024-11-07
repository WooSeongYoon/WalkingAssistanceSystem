import requests
import geocoder

def get_GPS():
    # 네이버 클라우드 플랫폼에서 발급받은 API 키 입력
    client_id = 'ecr1lhz9yb'
    client_secret = '2A5HEaJZNendKtooBAbe6JA0qxBV9bGhTN6qxA3j'
    # IP 기반으로 대략적인 현재 위치의 위도, 경도 가져오기
    g = geocoder.ip('me')
    

    # 현재 위치의 위도, 경도 출력
    if g.ok:
        latitude, longitude = g.latlng
        latitude = 35.8997267
        longitude = 128.8549113
        print(f"현재 위치의 위도: {latitude}, 경도: {longitude}")
    else:
        print("현재 위치의 GPS 좌표를 가져올 수 없습니다.")
        exit()

    # 네이버 Reverse Geocoding API URL
    url = "https://naveropenapi.apigw.ntruss.com/map-reversegeocode/v2/gc"

    # 요청 헤더에 API 키 포함
    headers = {
        "X-NCP-APIGW-API-KEY-ID": client_id,
        "X-NCP-APIGW-API-KEY": client_secret
    }

    # 요청 파라미터에 GPS 좌표 포함 (경도, 위도 순서로 입력)
    params = {
        "coords": f"{longitude},{latitude}",  # 좌표 (경도, 위도 순서)
        "orders": "roadaddr,addr",            # 도로명 주소와 지번 주소 요청
        "output": "json"                      # JSON 형식으로 응답받기
    }

    # API 요청 보내기
    response = requests.get(url, headers=headers, params=params)

    # 응답 처리
    if response.status_code == 200:
        data = response.json()
        if data['status']['code'] == 0:  # 요청 성공
            addresses = data['results']
            if addresses:
                road_address = addresses[0].get('land', {}).get('name', 'N/A')
                jibun_address = addresses[0].get('region', {}).get('area1', {}).get('name', 'N/A')
                print(f"도로명 주소: {road_address}")
                print(f"지번 주소: {jibun_address}")
            else:
                print("해당 좌표에 대한 주소가 없습니다.")
        else:
            print(f"오류: {data['status']['message']}")
    else:
        print(f"HTTP 오류 코드: {response.status_code}")
    
    return road_address, jibun_address, latitude, longitude