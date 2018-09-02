"""
.. module:: lambda_master_handler
    :synopsis: define the master handler responsible for gluing different modules together to handle an aws request

.. moduleauthor:: Khoi Trinh
"""

import logging
import time
import json
import uuid

import utils
import translator
import lambda_mqtt_manager
import mqtt_constant


class MasterHandler:

    def __init__(self):
        """
        docstring create a master handler project, create a logger as well as an mqtt manager for mqtt related task
            :param self: the instance of MasterHandler class
        """

        self._logger = logging.getLogger()
        """Instance of logger used for logging purpose"""
        self._logger.setLevel(logging.DEBUG)

        self._mqttManager = lambda_mqtt_manager.MqttManager()
        """Instance of an mqtt manager, used by the master handler for communicating with aws mqtt"""

    _replyReceived = False
    """flags used for signalling if the correct reply has been received by mqtt callback function"""

    _replyMessage = ""
    """message received by mqtt callback function"""

    _expectedTopic = ""
    """the topic that the master handler is expecting to receive from, the _replyReceived flag is only set if the expected topic mateched the received topic"""

    @staticmethod
    def subCallBack(client, userdata, message):
        """
        The mqtt subscribe callback function, used for receiving messages from the IoT devices
            :param client: derpecated param
            :param userdata: deperated param
            :param message: an object that contains the main payload as well as the topic that payload comes from
        """
        print("Expected topic: ")
        print(MasterHandler._expectedTopic)
        print("Received a new message: ")
        print(message.payload)
        print("from topic: ")
        print(message.topic)
        print("--------------\n\n")

        # only signal the MasterHandler if the message comes from correct topic
        if str(message.topic) == MasterHandler._expectedTopic:
            MasterHandler._replyReceived = True
            MasterHandler._replyMessage = message.payload

        else:
            print("Wrong topic received\n")

    def handleDiscoveryV3(self, request):
        """
        Used to handle discovery request, which lets Alexa know the list of devices that is available and what they can do
            :param self: the instance of master hander
            :param request: the request received by the lambda handler
        """
        response = {
            "event": {
                "header": {
                    "namespace": "Alexa.Discovery",
                    "name": "Discover.Response",
                    "payloadVersion": "3",
                    "messageId": utils.getUuid()
                },
                "payload": {
                    "endpoints": self._mqttManager.awsDeviceList
                }
            }
        }
        return response

    def handleNonDiscoveryV3(self, request, context):
        """
        Most requests are handled here, the handler will parse the necessary detail, forward it to the correct devices(using endpoint-ID to identify who to send to), wait for repy and then either timeout or tranlsate the reply of the IoT device into something that Alexa can understand and then hand it to the original lambda_handler in lambda_main
            :param self: instance of master handler
            :param request: the request received by lambda handler
            :param context: execution contex, not used
        """
        request_namespace = utils.getNameSpace(request)
        request_name = utils.getCommandName(request)

        # special case, for authorization accept grant, reply with authorizing response
        if request_namespace == "Alexa.Authorization":
            if request_name == "AcceptGrant":
                response = {
                    "event": {
                        "header": {
                            "namespace": "Alexa.Authorization",
                            "name": "AcceptGrant.Response",
                            "payloadVersion": "3",
                            "messageId": utils.getUuid()
                        },
                        "payload": {}
                    }
                }

        else:
            # TODO: add error handling
            # parse the message for necessary detail and then send it to IoT device
            appliance = self.getApplicanceByMessage(request)
            iotMessage = translator.Translator.translateToIoT(request)
            MasterHandler._replyReceived = False
            MasterHandler._replyMessage = ""
            MasterHandler._expectedTopic = appliance.pubTopic
            self._mqttManager.mqttPub(iotMessage, appliance.subTopic)

            while False == self._replyReceived:
                pass

            response = translator.Translator.translateToEcho(
                json.loads(self._replyMessage.decode('utf8')), request)

        return response

    def handleErrorResponse(self, request, errorType, errorMessage):
        """
        Used for creating a response to Amazon that indicates something wrong has happened
            :param self: instance of master handler
            :param request: the request received by lambda handler
            :param errorType: type of error encountered, limited number of types supported
            :param errorMessage: error message to be included in the payload
        """
        response = {
            "event": {
                "header": {
                    "namespace": "Alexa",
                    "name": "ErrorResponse",
                    "payloadVersion": "3",
                    "messageId": utils.getUuid(),
                    "correlationToken": utils.getCorrelationToken(request)
                },
                "endpoint": {
                    "scope": {
                        "type": "BearerToken",
                        "token": request["directive"]["endpoint"]["scope"]["token"]
                    },
                    "endpointId": utils.getEndpointID(request)
                },
                "payload": {
                    # TODO: may need to customize payload based on error type
                    "type": errorType,
                    "message": errorMessage,
                }
            }
        }
        return response

    def getApplicanceByMessage(self, message):
        """
        Parse the message sent by Alexa for the target endpoint ID and then look for that endpoint in the database list in the mqtt manager
            :param self: instance of master handler
            :param message: the message received by lambda handler from Alexa
        """
        for appliance in self._mqttManager.iotObjList:
            if appliance.awsObjectProfile["endpointId"] == utils.getEndpointID(message):
                return appliance
        return None
