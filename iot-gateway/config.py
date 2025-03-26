# ==================================================
# BASIC CONFIGURATION FOR SENDING AND RECEIVING DATA 
# NON-SCALABLE VERSION
# ==================================================
EMQX_USER_NAME  ='iot-gateway'
EMQX_PASSWORD   ='iot-gateway'
EMQX_URL        ='z7f54af0.ala.dedicated.aws.emqxcloud.com'


# ==================================================
# USER INFORMATION - DIRECTLY USE
# ==================================================
USER_ID         ='VVRsnPoAEqSbUa9QLwXLgj2D9Zx2'
ENV_ID          ='my_simple_garden'
SENSOR_ID       =['sensor-101', 'sensor-102', 'sensor-103']
ACTUATOR_ID     =['actuator-101', 'actuator-102', 'actuator-103', 'actuator-104']
SENSOR_TYPE     =['temperature', 'himidity', 'light']
ACTUATOR_TYPE   =['fan', 'pump', 'light', '---']
APP_NAME        = 'hcmut-smart-farm'


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