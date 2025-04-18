import os
import dotenv


dotenv.load_dotenv('./.env')

# =================================================
# MQTT BROKER CONNECTOR CONFIGURATION
# =================================================
MAIN_APP        =   os.getenv('MAIN_APP')
APP             =   os.getenv('APP')
EMQX_USER_NAME  =   os.getenv('EMQX_USER_NAME')
EMQX_PASSWORD   =   os.getenv('EMQX_PASSWORD')
EMQX_URL        =   os.getenv('EMQX_URL')
EMQX_PORT       =   os.getenv('EMQX_PORT')
TOPIC_TYPE      = ['data', 'command', 'status']
TOPIC           = '/'.join(
                            [
                                MAIN_APP,
                                '+',
                                '+',
                                '+',
                                '+',
                                TOPIC_TYPE[0]
                            ]
                        )
EMQX_ENCODE_SCHEME = os.getenv('EMQX_ENCODE_SCHEME')


# =================================================
# KAFKA CONNECTOR CONFIGURATION
# =================================================
KAFKA_CLUSTER               = os.getenv('KAFKA_CLUSTER')
KAFKA_BOOTSTRAP_SERVER      = os.getenv('KAFKA_BOOTSTRAP_SERVER')
KAFKA_TOPIC                 = os.getenv('KAFKA_TOPIC')
KAFKA_ENCODE_SCHEME         = os.getenv('KAFKA_ENCODE_SCHEME')
KAFKA_LINGER_TIME           = os.getenv('KAFKA_LINGER_TIME')
KAFKA_BATCH_SIZE            = os.getenv('KAFKA_BATCH_SIZE')
KAFKA_SECURITY_PROTOCOL     = os.getenv('KAFKA_SECURITY_PROTOCOL')
KAFKA_SASL_MECHANISM        = os.getenv('KAFKA_SASL_MECHANISM')
KAFKA_USERNAME              = os.getenv('KAFKA_USERNAME')
KAFKA_PASSWORD              = os.getenv('KAFKA_PASSWORD')
KAFKA_GROUP_ID              = os.getenv('KAFKA_GROUP_ID')


# =================================================
# DEPRECATED 😵
# DATA PROCESSING CONFIGURATION
# LEARN NETWORK IN DOCKER TO RUN THAT
# =================================================
MESSAGE_BROKER  = os.getenv('MESSAGE_BROKER')
BACK_END        = os.getenv('BACK_END')


# =================================================
# DEPRECATED 😵
# SINK CONNECTOR CONFIGURATION
# =================================================
INFLUXDB_TOKEN  = os.getenv('INFLUXDB_TOKEN')
INFLUXDB_URL    = os.getenv('INFLUXDB_URL')
INFLUXDB_ORG    = os.getenv('INFLUXDB_ORG')
INFLUXDB_BUCKET = os.getenv('INFLUXDB_BUCKET')
MEASUREMENT     = os.getenv('MEASUREMENT')