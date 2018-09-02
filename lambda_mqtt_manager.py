"""
.. module:: lambda_mqtt_manager
    :synopsis: define mqtt manager responsible for all communications with amazon aws server

.. moduleauthor:: Khoi Trinh
"""


"""
This is the mqtt manager, used for quick pub/sub opepration
"""

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from AWSIoTPythonSDK.MQTTLib import DROP_OLDEST
import mqtt_constant
import lambda_master_handler
import iot_object
import logging
import time
import json
import copy

# source: https://github.com/aws/aws-iot-device-sdk-python/blob/master/samples/basicPubSub/basicPubSub.py

# TODO: implement a queue for message handling

# source: https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python


class MqttManager:
    def __init__(self):
        self.awsDeviceList = []
        self.iotObjList = iot_object.IOT_OBJ_LIST
        self.createLogger()
        self.createAWSClient()

    def createLogger(self):
        # Configure logging
        self._logger = logging.getLogger("AWSIoTPythonSDK.core")
        self._logger.setLevel(logging.DEBUG)
        streamHandler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        streamHandler.setFormatter(formatter)
        self._logger.addHandler(streamHandler)

    def createAWSClient(self):

        # configure AWS client with credentials and connection info
        with open(mqtt_constant.ENDPT_FILE_PATH, 'r') as idFile:
            iotID = idFile.read().replace('\n', '')
        self._myAWSIoTMQTTClient = None
        self._myAWSIoTMQTTClient = AWSIoTMQTTClient(mqtt_constant.CLIENT_ID)
        self._myAWSIoTMQTTClient.configureEndpoint(
            iotID + mqtt_constant.AWS_ENDPOINT, mqtt_constant.MQTT_PORT)
        self._myAWSIoTMQTTClient.configureCredentials(
            mqtt_constant.AUTHORITY_CERT_PATH, mqtt_constant.PRIVATE_KEY_PATH, mqtt_constant.CERTIFICATE_PATH)

        # AWSIoTMQTTClient connection configuration
        self._myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(
            mqtt_constant.INITIAL_BACKOFF_TIME, mqtt_constant.MAX_BACKOFF_TIME, mqtt_constant.STABLE_TIME)
        self._myAWSIoTMQTTClient.configureOfflinePublishQueueing(
            mqtt_constant.OFFLINE_PUB_QUEUE, DROP_OLDEST)
        self._myAWSIoTMQTTClient.configureDrainingFrequency(
            mqtt_constant.DRAINING_FREQ)
        self._myAWSIoTMQTTClient.configureConnectDisconnectTimeout(
            mqtt_constant.CONNECT_DISCONNECT_TIMEOUT)  # 10 sec
        self._myAWSIoTMQTTClient.configureMQTTOperationTimeout(
            mqtt_constant.OPERATION_TIMEOUT)

        while False == self._myAWSIoTMQTTClient.connect(mqtt_constant.KEEP_ALIVE_SECONDS):
            pass

        # AWS subscription configuration
        for iotObject in iot_object.IOT_OBJ_LIST:
            self._myAWSIoTMQTTClient.subscribe(
                iotObject.pubTopic, mqtt_constant.SUB_QOS, lambda_master_handler.MasterHandler.subCallBack)
            self.awsDeviceList.append(iotObject.awsObjectProfile)

    def mqttPub(self, package, pubTopic):
        message = {}

        if "Alexa.Debug" == package["namespace"]:
            message["properties"] = []
            message["properties"].append(package)
        else:
            message = package

        messageJson = json.dumps(message)
        self._myAWSIoTMQTTClient.publish(
            pubTopic, messageJson, mqtt_constant.PUB_QOS)
