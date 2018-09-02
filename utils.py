"""
.. module:: utils
    :synopsis: include utils functions mainly for parsing the json dicts for aws messages

.. moduleauthor:: Khoi Trinh
"""


import time
import uuid


def get_directive_version(request):
    """
    docstring here
        :param request:
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
    docstring here
        :param seconds=None:
    """
    return time.strftime("%Y-%m-%dT%H:%M:%S.00Z", time.gmtime(seconds))


def getUuid():
    """
    docstring here
    """
    return str(uuid.uuid4())


def getNameSpace(message):
    """
    docstring here
        :param message: 
    """
    return message["directive"]["header"]["namespace"]


def getCommandName(message):
    """
    docstring here
        :param message: 
    """
    return message["directive"]["header"]["name"]


def getCorrelationToken(message):
    """
    docstring here
        :param message: 
    """
    return message["directive"]["header"]["correlationToken"]


def getEndpointID(echoMessage):
    """
    docstring here
        :param echoMessage: 
    """
    return echoMessage["directive"]["endpoint"]["endpointId"]


def getPayload(echoMessage):
    """
    docstring here
        :param echoMessage: 
    """
    return echoMessage["directive"]["payload"]


def getAccessToken(echoMessage):
    """
    docstring here
        :param echoMessage: 
    """
    return echoMessage["directive"]["endpoint"]["scope"]["token"]
