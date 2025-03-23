# Flask RESTful Backend Service

## Overview

This project is a lightweight backend service built using Flask and Flask-RESTful. It provides a simple and scalable REST API for handling various operations.

## Features

- RESTful API endpoints
- Easy to extend and maintain
- Lightweight and fast
- Follows best practices for Flask development
- Integrated Swagger UI for API testing

## Requirements

- Python 3.7 or higher
- pip (Python package manager)

## Installation

1. Clone the repository:
    ```bash
    cd another-lightweight-backend
    ```

2. Create a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the development server:
    ```bash
    Export the required environment variables:

    ```bash
    export SERVICE_ACCOUNT_KEY="your_service_account_key"
    export JWT_SECRET_KEY="your_jwt_secret_key"
    ```

    Alternatively, you can use a `.env` file to manage environment variables. Create a `.env` file in the project root directory and add the following:

    ```
    SERVICE_ACCOUNT_KEY=your_service_account_key
    JWT_SECRET_KEY=your_jwt_secret_key
    ```

    Then, use a library like `python-dotenv` to load the variables automatically in your application:

    ```python
    from dotenv import load_dotenv
    load_dotenv()
    ```
    python app.py
    ```

2. Access the API at `http://127.0.0.1:5000`.

3. Test the API using Swagger UI:
    Open your browser and navigate to `http://127.0.0.1:5000/swagger-ui` to explore and test the available API endpoints. 
    SWAGGER_URL = "/api/docs"
    API_URL = "/static/swagger.yaml" for API testings
    or using API testing tools like Postman or Insomnia

## Project Structure

```
another-lightweight-backend/
├── app.py               # Main application file
├── resources/           # API resource files
├── models/              # Database models
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or suggestions, please contact [dung.lebk2210573@hcmut.edu.vn]. Flask RESTful Backend Service