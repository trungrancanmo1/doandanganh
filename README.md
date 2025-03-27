# HCMUT Smart Farm IoT Application

This project is a template for an IoT-based smart farm application. It consists of three main components:

1. **Front-End**: A dashboard for monitoring and controlling the farm.
2. **Back-End**: A Django-based server for managing data and APIs.
3. **Local Data Processing Service**: A simulation of the IoT data pipeline (with message queue as Redis).

---

## Project Structure

```
hcmut-smart-farm/
├── front-end/               # Dashboard (React/HTML/JS)
├── back-end/                # Django server
├── iot-gateway/             # IoT Gateway for device communication
├── local_data_process_service/ # Local data processing service
└── README.md                # Project documentation
```

---

## Components

### 1. Front-End (Dashboard)
- **Description**: A user interface for visualizing farm data and sending commands.
- **Technologies**: React.js or plain HTML/JavaScript.
- **Setup**:
    ```bash
    cd frontend/frontend
    npm install
    npm start
    ```

### 2. Back-End (Django)
- **Description**: A Django-based server for handling APIs and managing data.
- **Technologies**: Django, Django REST Framework.
- **Setup**:
    ```bash
    cd backend
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

- **Prepare Environment Variables**:
    Create a `.env` file in the `backend` directory with the necessary environment variables. See the .env.example for further information.

- **Run the Server**:
    ```bash
    python manage.py runserver
    ```

### 3. Local Data Processing Service
- **Description**: Simulates IoT data generation and processing.
- **Technologies**: Python.
- **Setup**:
    ```bash
    cd local_data_process_service
    ```
---

## Getting Started

1. Clone the repository:
     ```bash
     git clone
     cd hcmut-smart-farm
     ```

2. Follow the setup instructions for each component.

3. Run all components and ensure they are connected.

---

## Future Improvements
- Add real IoT device integration.
- Enhance the dashboard with more visualizations.
- Implement advanced data analytics.
- ADD more users and more environments ⚠️⚠️⚠️
---

## License
This project is licensed under the MIT License.