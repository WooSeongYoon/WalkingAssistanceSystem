import serial

# LiDAR에서 거리 데이터를 읽는 함수
def readLidarData(ser, SPECIFIED_MAX_DISTANCE):
    if ser.in_waiting > 8:
        bytes_serial = ser.read(9)
        ser.reset_input_buffer()
        
        if bytes_serial[:2] == b'\x59\x59':  # TFmini Plus 헤더 확인
            distance_cm = int.from_bytes(bytes_serial[2:4], 'little')
            distance_m = distance_cm / 100
            
            if distance_m is not None and distance_m <= SPECIFIED_MAX_DISTANCE:
                return distance_m  # 거리 (미터 단위)
    return None