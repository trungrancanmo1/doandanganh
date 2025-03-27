import os
import dotenv


dotenv.load_dotenv('./.env')

# =================================================
# SOURCE CONNECTOR CONFIGURATION
# =================================================
APP             =   os.getenv('APP')
EMQX_USER_NAME  =   os.getenv('EMQX_USER_NAME')
EMQX_PASSWORD   =   os.getenv('EMQX_PASSWORD')
EMQX_URL        =   os.getenv('EMQX_URL')
EMQX_PORT       =   os.getenv('EMQX_PORT')
TOPIC_TYPE      = ['data', 'command', 'status']
TOPIC           = '/'.join(
                            [
                                APP,
                                '+',
                                '+',
                                '+',
                                '+',
                                TOPIC_TYPE[0]
                            ]
                        )
DATA_ENCODE_SCHEME = os.getenv('DATA_ENCODE_SCHEME')


# =================================================
# DATA PROCESSING CONFIGURATION
# LEARN NETWORK IN DOCKER TO RUN THAT
# =================================================
MESSAGE_BROKER  = os.getenv('MESSAGE_BROKER')
BACK_END        = os.getenv('BACK_END')


# =================================================
# SINK CONNECTOR CONFIGURATION
# =================================================
INFLUXDB_TOKEN  = os.getenv('INFLUXDB_TOKEN')
INFLUXDB_URL    = os.getenv('INFLUXDB_URL')
INFLUXDB_ORG    = os.getenv('INFLUXDB_ORG')
INFLUXDB_BUCKET = os.getenv('INFLUXDB_BUCKET')
MEASUREMENT     = os.getenv('MEASUREMENT')