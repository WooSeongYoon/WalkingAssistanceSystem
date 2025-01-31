import requests
import gps

def get_GPS():
    """
    GPS 데이터(위도, 경도) 찾기
    """
    try:
        session = gps.gps(host="localhost", port="2947")
        session.stream(gps.WATCH_ENABLE | gps.WATCH_JSON)
        
        for report in session:
            if report['class'] == 'TPV':
                lat = getattr(report, 'lat', None)
                lng = getattr(report, 'lon', None)
                if lat and lng:
                    return f"{lat:.4f}", f"{lng:.4f}"
    except Exception as e:
        print(f"GPS error: {e}")
    return None, None

def get_address_from_GPS(lat, lng):
    """
    Naver Reverse Geocoding API사용하여 GPS(경도, 위도)로 도로명 주소와 지번 주소 찾기
    """
    url = "https://naveropenapi.apigw.ntruss.com/map-reversegeocode/v2/gc"
    headers = {
        "X-NCP-APIGW-API-KEY-ID": 'ecr1lhz9yb',
        "X-NCP-APIGW-API-KEY": '2A5HEaJZNendKtooBAbe6JA0qxBV9bGhTN6qxA3j'
    }
    params = {"coords": f"{lng},{lat}", "sourcecrs": "EPSG:4326", "orders": "roadaddr,addr", "output": "json"}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status() # HTTP 오류 발생 시 예외 처리
        data = response.json()
        
        if data['status']['code'] != 0:
            print(f"API error: {data['status']['message']}")
            return None, None
        
        addresses = data.get('results', [])
        # 주소 확인 불가
        if not addresses:
            print("There is no address for that coordinate.")
            return None, None
        
        # 지번 주소 추출
        region = addresses[0].get('region', {})
        jibun_address = " ".join(
            value.get('name', 'N/A') for key, value in region.items() if key.startswith('area') and key != 'area0'
        )
        # 도로명 주소 출력
        land = addresses[0].get('land', {})
        if land.get("type") == "": # 건물
            road_address = f"{land.get('name', 'N/A')} {land.get('number1', '')}".strip()
        else: # 도로
            road_address = f"{land.get('number1', '')}"
        return road_address, jibun_address

    except requests.RequestException as e:
        print(f"API request error: {e}")
        return None, None
