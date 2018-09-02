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


""" Master Handler Class Area """


class MasterHandler:

    def __init__(self):
        self._logger = logging.getLogger()
        self._logger.setLevel(logging.DEBUG)
        self._mqttManager = lambda_mqtt_manager.MqttManager()

    _replyReceived = False
    _replyMessage = ""
    _expectedTopic = ""

    @staticmethod
    def subCallBack(client, userdata, message):
        print("Expected topic: ")
        print(MasterHandler._expectedTopic)
        print("Received a new message: ")
        print(message.payload)
        print("from topic: ")
        print(message.topic)
        print("--------------\n\n")
        if str(message.topic) == MasterHandler._expectedTopic:
            MasterHandler._replyReceived = True
            MasterHandler._replyMessage = message.payload

        else:
            print("Wrong topic received\n")

    def handleDiscoveryV3(self, request):

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
        request_namespace = utils.getNameSpace(request)
        request_name = utils.getCommandName(request)

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
        for appliance in self._mqttManager.iotObjList:
            if appliance.awsObjectProfile["endpointId"] == utils.getEndpointID(message):
                return appliance
        return None
