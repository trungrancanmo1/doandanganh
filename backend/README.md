# Garden Monitoring System - Backend

## Overview
This is the backend of a Garden Monitoring System built with Django. The system manages various aspects of a garden, including:
- **Notifications**: Sends alerts based on garden conditions.
- **Overview**: Provides a summary of all garden parameters.
- **Light**: Monitors sunlight exposure.
- **Temperature**: Records temperature changes.
- **Humidity**: Tracks moisture levels.
- **Pest Control**: Helps in tracking and managing pests.

## Installation and Setup
All steps are executed at backend/ directory.
### Steps to Run
1. **Create and activate a virtual environment (optional)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Apply database migrations**
   ```bash
   python manage.py migrate
   ```

4. **Run the development server**
   ```bash
   python manage.py runserver
   ```

The backend will now be accessible at `http://127.0.0.1:8000/`.