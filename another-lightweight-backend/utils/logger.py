import logging
import os
from logging.handlers import RotatingFileHandler


# For loggings
if not os.path.exists("logs"):
    os.makedirs("logs")


# (DEBUG, INFO, WARNING, ERROR, CRITICAL)
logger = logging.getLogger("smart-farm")
logger.setLevel(logging.DEBUG)

# Rotate file handlers
# max capacity 1 MB
file_handler = RotatingFileHandler("logs/app.log", maxBytes=1_000_000, backupCount=3)
file_handler.setFormatter(logging.Formatter(
    "[%(asctime)s] %(levelname)s - %(module)s: %(message)s"
))

# in production, update the level of loggings
file_handler.setLevel(logging.INFO)


# Use for debugging
# Console Handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(
    "[%(levelname)s] %(message)s"
))
console_handler.setLevel(logging.DEBUG)


# Attach two handlers for the logger
# one is file handler
# one is console handler
logger.addHandler(file_handler)
logger.addHandler(console_handler)