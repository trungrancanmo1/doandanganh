import cv2 as cv
import time
import requests
import datetime

def upload_image(image_path, timestamp, access_token):
    url = "https://doandanganh.onrender.com/api/pest/image/upload/"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    files = {
        "image": open(image_path, "rb"),
    }
    data = {
        "timestamp": timestamp,
    }
    
    response = requests.post(url, headers=headers, files=files, data=data)
    
    files["image"].close()  # Close the file after request
    return response.json()

TIMESTAMP = "2025-04-01T12:00:00Z"
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ2MDAxMTA1LCJpYXQiOjE3NDUzOTYzMDUsImp0aSI6ImZlNTJjMWYxYWJmZDQzMjZhNmE5YmFkYzcxMThkYTE3IiwidXNlcl9pZCI6MSwiZW1haWwiOiJuZ3luaG9nbWluaEBnbWFpbC5jb20iLCJ1c2VybmFtZSI6InRlc3R1c2VybmFtZSIsImZpcnN0X25hbWUiOiJ0ZXN0Zmlyc3RuYW1lIiwibGFzdF9uYW1lIjoidGVzdGxhc3RuYW1lIn0.hFCx1OFeR2O5dqx36SJv6jrFAXThIG2mB6vKUY6p4W0"

cap = cv.VideoCapture(0, cv.CAP_DSHOW)

if not cap.isOpened():
  exit()

DELAY = 20
last_captured_time = time.time() + DELAY

while True:
  ret, frame = cap.read()
  if not ret:
    print("Couldn't read current frame")
    continue
  cv.imshow("Testing", frame)
  
  if time.time() - last_captured_time >= DELAY:
    last_captured_time = time.time()
    filename = "image.jpg"
    cv.imwrite(filename, frame)
    print(f"Frame saved as {filename}")
    
    now_utc = datetime.datetime.utcnow()
    timestamp = now_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"Uploading file {filename} with timestamp {timestamp}")
    print(f"Uploading at {time.time()}")
    try:
      response = upload_image(filename, timestamp, ACCESS_TOKEN)
      print(f"Response: {response}")
    except Exception as e:
      print(f"An error occurred: {e}")
      continue
    print()
  
  if cv.waitKey(1) & 0xFF == ord('q'):
    break
  
  if cv.waitKey(1) & 0xFF == ord('s'):
    filename = "image.jpg"
    cv.imwrite(filename, frame)
    print(f"Frame saved as {filename}")
    
    now_utc = datetime.datetime.utcnow()
    timestamp = now_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"Uploading file {filename} with timestamp {timestamp}")
    print(f"Uploading at {time.time()}")
    try:
      response = upload_image(filename, timestamp, ACCESS_TOKEN)
      print(f"Response: {response}")
    except Exception as e:
      print(f"An error occurred: {e}")
      continue
    print()
    
cap.release()
cv.destroyAllWindows()