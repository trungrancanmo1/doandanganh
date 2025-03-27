import serial
import time
import json
from config import make_topic
from datetime import datetime
# from mqtt_broker_to_iot_gateway import send_to_device
from iot_gateway_to_mqtt_broker import send_to_broker

# Device setup
PORT = 'COM22'
BAUDRATE = 115200
TIMEOUT = 1

ser = serial.Serial(PORT, BAUDRATE, timeout=TIMEOUT)
print(f"Serial port {PORT} opened successfully.")

def receive_serial_data():
    try:
        if ser.in_waiting > 0:
            received_bytes = ser.readline().strip()
            try:
                received_string = received_bytes.decode('utf-8')
                return received_string
            except UnicodeDecodeError:
                print(f"Error decoding received bytes: {received_bytes}")
                return None
        else:
            return None

    except serial.SerialException as e:
        print(f"Error opening serial port {PORT}: {e}")
        return None
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print(f"Serial port {PORT} closed.")
            
def parse_data_to_dict(data):
    data_dict = {}
    pairs = data.split(', ')

    for pair in pairs:
        key_value = pair.split(': ')
        if len(key_value) == 2:
            key = key_value[0].strip()
            value_str = key_value[1].strip()
            try:
                value = float(value_str)
            except ValueError:
                value = value_str  # Keep as string if conversion fails
            data_dict[key] = value
        
    return data_dict

if __name__ == "__main__":
    read_interval = 2  # Check for data every 2 seconds
    try:
        while True:
            data = receive_serial_data()
            if data:
                data = parse_data_to_dict(data)
                print(f"Received data: {data}")
                for type, value in data.items():
                    data_formatted =  { 
                        "user_id": "VVRsnPoAEqSbUa9QLwXLgj2D9Zx2",
                        "env_id": "my_simple_garden",
                        "sensor_id": "sensor-101",
                        ##########################
                        "timestamp": str(datetime.now().astimezone()),
                        "type": type,
                        "value": value ########### always float
                    }
                    payload = json.dumps(data_formatted).encode('utf-8')
                    topic = make_topic('sensor-101', 'data', type)
                    print(f"Send data to broker: {json.dumps(data_formatted, indent=4)}")
                    send_to_broker(payload=payload, topic=topic)
                # Process the received data here
            else:
                print(f"No data received on {PORT} within the timeout.")
            time.sleep(read_interval)

    except KeyboardInterrupt:
        print("Exiting serial receiver.")