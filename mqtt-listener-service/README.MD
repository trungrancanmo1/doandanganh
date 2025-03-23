## Set up and usage
1. **Dependencies installation**
```bash
    pip install -r requirements.txt
```

2. **Set up the environment variables using a .env file or export them manually**
```bash
    export IO_KEY=<Your io.adafruit.com key>
    export IO_USERNAME=<Your io.adafruit.com username>
    export CREDENTIALS_LOCATION=<Firebase service account credentials downloaded from Project settings>
```
Or create a ./.env file and set up
```.env
    CREDENTIALS_LOCATION=
    IO_USERNAME=
    IO_KEY=
```

3. **Run the service separately from the web application back-end service**

To run the MQTT listener service independently of the web application back-end, execute the following command:

```bash
    python app.py
```