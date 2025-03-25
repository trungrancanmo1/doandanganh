import os
import dotenv


dotenv.load_dotenv('./.env')

# =================================================
# SOURCE CONNECTOR CONFIGURATION
# =================================================
APP_NAME        = 'hcmut-smart-farm'
EMQX_USER_NAME  =   os.getenv('EMQX_USER_NAME')
EMQX_PASSWORD   =   os.getenv('EMQX_PASSWORD')
EMQX_URL        =   os.getenv('EMQX_URL')
PORT            = 1883
TOPIC_TYPE      = ['data', 'command', 'status']
TOPIC = '/'.join(
    [
        APP_NAME,
        '+',
        '+',
        '+',
        '+',
        TOPIC_TYPE[0]
    ]
)
DATA_DECODE = 'utf-8'


# =================================================
# DATA PROCESSING CONFIGURATION
# =================================================
MESSAGE_BROKER  = 'redis://localhost:6379/0'
BACK_END = 'redis://localhost:6379/0'


# =================================================
# SINK CONNECTOR CONFIGURATION
# =================================================