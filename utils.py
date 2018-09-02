"""
.. module:: utils
    :synopsis: include utils functions mainly for parsing the json dicts for aws messages

.. moduleauthor:: Khoi Trinh
"""


import time
import uuid


def get_directive_version(request):
    """
    Get the version directive to be either v2 or v3
        :param request: the request set to the hander
    """
    try:
        return request["directive"]["header"]["payloadVersion"]
    except:
        try:
            return request["header"]["payloadVersion"]
        except:
            return "-1"


def getUtcTimeStamp(seconds=None):
    """
    Used for returning current time for timestamp purpose in aws reply
        :param seconds=None: get current utc time
    """
    return time.strftime("%Y-%m-%dT%H:%M:%S.00Z", time.gmtime(seconds))


def getUuid():
    """
    Get unique ID for message
    """
    return str(uuid.uuid4())


def getNameSpace(message):
    """
    Return namespace of the command received
        :param message: message sent to the lambda handler
    """
    return message["directive"]["header"]["namespace"]


def getCommandName(message):
    """
    Get the command name in the json message sent to the lambda handler
        :param message: message sent to the lambda handler
    """
    return message["directive"]["header"]["name"]


def getCorrelationToken(message):
    """
    Get the Correleation token for the of the Alexa message
        :param message: message sent to the lambda handler
    """
    return message["directive"]["header"]["correlationToken"]


def getEndpointID(echoMessage):
    """
    Get the uniqe target endpoint ID of Alexa message so that it can be compared with database
        :param echomessage: message sent to the lambda handler
    """
    return echoMessage["directive"]["endpoint"]["endpointId"]


def getPayload(echoMessage):
    """
    Get the paylod component of the message sent to lambda
        :param echomessage: message sent to the lambda handler
    """
    return echoMessage["directive"]["payload"]


def getAccessToken(echoMessage):
    """
    Get Access Token of Alexa message
        :param echomessage: message sent to the lambda handler
    """
    return echoMessage["directive"]["endpoint"]["scope"]["token"]
