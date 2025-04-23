# ==================================================
# BASIC CONFIGURATION FOR SENDING AND RECEIVING DATA 
# NON-SCALABLE VERSION
# ==================================================
EMQX_USER_NAME  ='iot-gateway'
EMQX_PASSWORD   ='iot-gateway'
EMQX_URL        ='j1c5ac51.ala.dedicated.aws.emqxcloud.com'


# ==================================================
# USER INFORMATION - DIRECTLY USE
# ==================================================
USER_ID         ='VVRsnPoAEqSbUa9QLwXLgj2D9Zx2'
ENV_ID          ='my_simple_garden'
SENSOR_ID       =['sensor-101', 'sensor-102', 'sensor-103']
SENSOR_TYPE     =['temperature', 'humidity', 'light']
ACTUATOR_ID     =['actuator-101', 'actuator-102', 'actuator-103', 'actuator-104']
ACTUATOR_TYPE   =['fan', 'pump', 'light', 'heater']
APP_NAME        ='hcmut-smart-farm'
ENCODE_SCHEME   ='utf-8'


def make_topic(device_id : str, topic_type : str, device_type : str) -> str:
    '''
    - device_id must be in SENSOR_ID and ACTUATOR_ID
    - topic_type : 'command', 'data'
    - device_type must be in SENSOR_TYPE and ACTUATOR_TYPE

    example : 
    # listen on command topic (only yours)
    - hcmut-smart-farm/VVRsnPoAEqSbUa9QLwXLgj2D9Zx2/my_simple_garden/actuator-103/cooler/command
    # public to data topic (only yours)
    - hcmut-smart-farm/VVRsnPoAEqSbUa9QLwXLgj2D9Zx2/my_simple_garden/sensor-101/temperature/data
    '''
    topic = '/'.join (
        [
            APP_NAME,
            USER_ID,
            ENV_ID,
            device_id,
            device_type,
            topic_type
        ]
    )

    # print(topic)
    return topic


# ==================================================
# DATA TEMPLATE FOR SENSORS
# ==================================================
sample_sensor_data =  {
    "user_id": "VVRsnPoAEqSbUa9QLwXLgj2D9Zx2",
    "env_id": "my_simple_garden",
    "sensor_id": "sensor-101",
    ##########################
    "timestamp": "",
    "type": "temperature",
    "value": 40.1,
    "state": 0 # optional, for on or off
}


# ==================================================
# DATA TEMPLATE FOR ACTUATORS
# ==================================================
sample_actuator_data =  {
    "user_id": "VVRsnPoAEqSbUa9QLwXLgj2D9Zx2",
    "env_id": "my_simple_garden",
    "actuator_id": "actuator-101",
    ##########################
    "timestamp": "",
    "type": "fan",
    "value": 40.1 ########### always float
}