import requests

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

# Example usage
image_path = "flappy_bird.jpg"
timestamp = "2025-04-01T12:00:00Z"
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ1MzkyODEwLCJpYXQiOjE3NDQ3ODgwMTAsImp0aSI6Ijg4MTMzMTQ5MmRjMjQ5MmJhNmNjMWFjNjM4YTFiY2ViIiwidXNlcl9pZCI6NCwiZW1haWwiOiJ0ZXN0QGVtYWlsLmNvbSIsInVzZXJuYW1lIjoidGVzdHVzZXJuYW1lIiwiZmlyc3RfbmFtZSI6IkZpcnN0bmFtZSIsImxhc3RfbmFtZSI6Ikxhc3RuYW1lIn0.kv57ajudK5OqkFRQ_AiHOUj1mGw9SvSqZTnYuPVno9w"

response = upload_image(image_path, timestamp, access_token)
print(response)
