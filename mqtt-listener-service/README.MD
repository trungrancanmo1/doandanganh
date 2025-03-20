## Set up and usage
1. **Set up the environment variables using a .env file or export them manually**
```bash
    pip install adafruit-io firebase-admin flask python-dotenv
    export IO_KEY=<Your io.adafruit.com key>
    export IO_USERNAME=<Your io.adafruit.com username>
```

2. **Run the service separately from the web application back-end service**

To run the MQTT listener service independently of the web application back-end, execute the following command:

```bash
    python app.py
```