"""
.. module:: translator
    :synopsis: define a translator class responsible for translating commands from Alexa to IoT devices command and vice versa 

.. moduleauthor:: Khoi Trinh
"""

import mqtt_constant
import utils
import copy

# a skeleton message being sent to the IoT
iotMessagePrototype = {
    "namespace": "Alexa.PowerController",
    "name": "TurnOff",
    "payload": {
    }
}
"""Contain a skeleton dictionary of a message to be sent to the IoT Devices, translator base on this for the final message"""

iotReplyPrototype = {
    "namespace": "Alexa.BrightnessController",
    "name": "brightness",
    "value": 50
}
"""A skeleton dictionary that represents typical reply by IoT devices, the translator copy this, extract the data from the IoT reply into the copy, and then attach into the final response to Alexa"""


# a skeleton properties section of echo response
echoPropertiesPrototype = {
    "namespace": "Alexa.PowerController",
    "name": "powerState",
    "value": "OFF",
    "timeOfSample": "2017-09-27T18:30:30.45Z",
    "uncertaintyInMilliseconds": mqtt_constant.UNCERTAINTY_MS
}
"""A skeleton dictionary represents a typical member of the properties list in the Discovery response to Alexa"""

# a skeleton echo message
echoResponsePrototype = {
    "context": {
        "properties": [
        ]
    },
    "event": {
        "header": {
            "namespace": "Alexa",
            "name": "StateReport",
            "payloadVersion": "3",
            "messageId": "5f8a426e-01e4-4cc9-8b79-65f8bd0fd8a4",
            "correlationToken": "dFMb0z+PgpgdDmluhJ1LddFvSqZ/jCc8ptlAKulUj90jSqg=="
        },
        "endpoint": {
            "scope": {
                "type": "BearerToken",
                "token": "access-token-from-Amazon"
            },
            "endpointId": "endpoint-001"
        },
        "payload": {}
    }
}
"""A skeleton dictionary representing a response to Alexa, translator will fill this out with appropriate details and then return as the lambda final responses(if it passes the json validate test)"""


class Translator:
    """Responsible for translating from Alexa commands to commands for IoT and replies of IoT devices to Alexa responses to users"""

    @staticmethod
    def translateToEcho(iotMessage, echoMessage):
        """
        docstring here
            :param iotMessage: the message received from and IoT device 
            :param echoMessage: the echo message originally received by the lambda handler
            :return: the final dict to be returned as return result of the lambda handler
        """
        response = copy.deepcopy(echoResponsePrototype)

        """handle the propeprties part of the response"""

        # always report connectivity status

        for pperty in iotMessage["properties"]:
            tempPpty = copy.deepcopy(iotReplyPrototype)
            tempPpty["timeOfSample"] = utils.getUtcTimeStamp()
            tempPpty["uncertaintyInMilliseconds"] = mqtt_constant.UNCERTAINTY_MS
            tempPpty["namespace"] = pperty["namespace"]
            tempPpty["name"] = pperty["name"]
            tempPpty["value"] = pperty["value"]

            # used for debugging only
            if "Alexa.Debug" == pperty["namespace"]:
                tempPpty["namespace"] = "Alexa.PowerController"
                tempPpty["name"] = "powerState"
                tempPpty.pop("payload", None)
                tempPpty["value"] = "OFF"

            response["context"]["properties"].append(tempPpty)

        response["context"]["properties"].append({
            "namespace": "Alexa.EndpointHealth",
            "name": "connectivity",
            "value": {
                    "value": "OK"
            },
            "timeOfSample": utils.getUtcTimeStamp(),
            "uncertaintyInMilliseconds": mqtt_constant.UNCERTAINTY_MS
        })

        """handle the event part of the response"""
        if("ReportState" == utils.getCommandName(echoMessage)):
            response["event"]["header"]["namespace"] = "Alexa"
            response["event"]["header"]["name"] = "StateReport"
        else:
            response["event"]["header"]["namespace"] = "Alexa"
            response["event"]["header"]["name"] = "Response"

        response["event"]["endpoint"]["endpointId"] = utils.getEndpointID(
            echoMessage)
        response["event"]["header"]["messageId"] = utils.getUuid()
        response["event"]["endpoint"]["scope"]["token"] = utils.getAccessToken(
            echoMessage)
        response["event"]["header"]["correlationToken"] = utils.getCorrelationToken(
            echoMessage)

        return response

    @staticmethod
    def translateToIoT(echoMessage):
        """
        docstring here
            :param echoMessage: message to be translated to IoT
            :return: the translated dict to be sent to IoT
        """
        # extract the name and namespace part of the request and fwd it to the iot device
        response = iotMessagePrototype
        response["namespace"] = utils.getNameSpace(echoMessage)
        response["name"] = utils.getCommandName(echoMessage)
        response["payload"] = utils.getPayload(echoMessage)
        return response
