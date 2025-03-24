import logging
import colorlog


# (DEBUG, INFO, WARNING, ERROR, CRITICAL)
logger = logging.getLogger('MQTT Broker Listener')
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
)

console_handler.setFormatter(formatter)

logger.addHandler(console_handler)