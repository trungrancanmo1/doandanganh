## Set up and usage
1. **Set up the environment variable or use .env file**
```bash
    pip install adafruit-io
    export IO_KEY=<Your io.adafruit.com key>
    export IO_USERNAME=<Your io.adafruit.com username>
```

2. **Import and use the package's util as mqtt_subscriber_start**
```python
    from afsubscriber import mqtt_subscriber_start
    mqtt_subscriber_start()
```