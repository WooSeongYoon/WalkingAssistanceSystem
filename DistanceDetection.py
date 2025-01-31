def readLidarData(ser, max_distance):
    """
    Read distance data from LiDAR.
    """
    try:
        if ser.in_waiting > 8:
            bytes_serial = ser.read(9)
            ser.reset_input_buffer()
            if bytes_serial[:2] == b'\x59\x59':  # TFmini Plus header check
                distance_cm = int.from_bytes(bytes_serial[2:4], 'little')
                distance_m = distance_cm / 100
                return distance_m if 0 < distance_m <= max_distance else None
                
    except Exception as e:
        print(f"LiDAR read error: {e}")
    return None
