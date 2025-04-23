import requests
import json

BASE_URL = "http://localhost:8000"

def post_data(header, data):
    try:
        response = requests.post(f"{BASE_URL}/data",
                                 headers=header,
                                 data=data)
        response.raise_for_status()
        print(f"POST /data Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"POST /data Error: {e}")

if __name__ == "__main__":
    data = json.dumps({"message": "Hello server from client!"})
    header = {"Content-type": "application/json"}
    post_data(header, data)