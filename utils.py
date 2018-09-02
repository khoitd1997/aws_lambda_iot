"""
.. module:: utils
    :synopsis: include utils functions mainly for parsing the json dicts for aws messages

.. moduleauthor:: Khoi Trinh
"""


import time
import uuid


def get_directive_version(request):
    try:
        return request["directive"]["header"]["payloadVersion"]
    except:
        try:
            return request["header"]["payloadVersion"]
        except:
            return "-1"


def getUtcTimeStamp(seconds=None):
    return time.strftime("%Y-%m-%dT%H:%M:%S.00Z", time.gmtime(seconds))


def getUuid():
    return str(uuid.uuid4())


def getNameSpace(message):
    return message["directive"]["header"]["namespace"]


def getCommandName(message):
    return message["directive"]["header"]["name"]


def getCorrelationToken(message):
    return message["directive"]["header"]["correlationToken"]


def getEndpointID(echoMessage):
    return echoMessage["directive"]["endpoint"]["endpointId"]


def getPayload(echoMessage):
    return echoMessage["directive"]["payload"]


def getAccessToken(echoMessage):
    return echoMessage["directive"]["endpoint"]["scope"]["token"]
