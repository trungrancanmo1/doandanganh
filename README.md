# HCMUT Smart Farm

HCMUT Smart Farm is an IoT-based system designed to monitor and control smart farming environments.

## Project Structure

```
hcmut-smart-farm/
├── dashboard-service/       # Dashboard (React/HTML/JS)
├── iot-gateway/             # IoT gateway (Python)
├── microservices/           # Backend microservices
├── virtual-iot-gateway/     # Virtual IoT gateway (for testing)
└── README.md                # Project documentation
```

- **dashboard-service**: ReactJS dashboard for monitoring and control.
- **iot-gateway**: Python application managing farm sensors.
- **microservices**: Multiple backend services supporting the system.
- **virtual-iot-gateway**: Virtual gateway for local/system testing.

## Getting Started

1. **Clone the repository:**
    ```bash
    git clone https://github.com/trungrancanmo1/doandanganh.git
    cd doandanganh/
    ```
2. **Install and set up each component as described below.**

---

## Components

### 1. Dashboard Service

- **Description:** User interface for visualizing farm data and sending commands.
- **Technologies:** React.js, HTML, JavaScript.
- **Setup:**
    ```bash
    cd dashboard-service
    npm install
    npm start
    ```

### 2. IoT Gateway

- **Description:** Python-based gateway to manage sensors and devices at the farm.
- **Technologies:** Python, Yolobit.
- **Device Setup:** See [Yolobit devices](https://eduall.vn/s/may-tinh-lap-trinh-mini-yolobit/)
- **Setup:**
    ```bash
    cd iot-gateway
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
- **Run:**
    ```bash
    python main.py
    ```

### 3. Microservices

- **Description:** Backend microservices supporting the system.
- **Technologies:** Python, Go, Java.
- **Run all services:**
    ```bash
    cd microservices
    docker compose up --detach
    ```
- **Run RestAPI service separately:**
    ```bash
    cd legacy-api
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    cd garden
    python manage.py runserver
    ```

### 4. Virtual IoT Gateway

- **Description:** Python script simulating the IoT gateway for testing.
- **Technologies:** Python.
- **Setup:**
    ```bash
    cd virtual-iot-gateway
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```
- **Run:**
    ```bash
    python main.py
    ```

---

## Future Improvements

- Integrate with real IoT devices.
- Enhance dashboard visualizations.
- Implement advanced data analytics.
- Support multiple users and environments.

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss your ideas.

## License

This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).