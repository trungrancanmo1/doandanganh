import os
from dotenv import load_dotenv


# Load environment variables from .env (only once)
load_dotenv()


# available ENVIROMENT VARIABLES
SERVICE_ACCOUNT_KEY = os.getenv('SERVICE_ACCOUNT_KEY')
if not SERVICE_ACCOUNT_KEY:
    raise ValueError("SERVICE_ACCOUNT_KEY is not provided!")