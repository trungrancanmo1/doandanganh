from Adafruit_IO import Client, RequestError
from collections import deque

def get_unread_data_from_feed(key: str, client: Client):
    result = deque([])
    while True:
        try:
            data = client.receive_next(key)
            result.appendleft(data)
        except RequestError:
            return list(result)