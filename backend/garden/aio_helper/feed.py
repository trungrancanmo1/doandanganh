from Adafruit_IO import Client, Feed, RequestError

def get_or_create_feed(key: str, client: Client):
    existing_feed_names = list(map(lambda feed: feed.name, client.feeds()))
    if key in existing_feed_names:
        return client.feeds(key)
    new_feed = Feed(name=key)
    return client.create_feed(new_feed)