"""
.. module:: mqtt_constant
    :synopsis: used for storing constants, contain settings and configurations for establishing connections with mqtt server

.. moduleauthor:: Khoi Trinh
"""


"""
Used for storing constants related to MQTT operations
"""
import json

# Communication quality constant

UNCERTAINTY_MS = 200
"""Uncertainty of measurement that is reported to Alexa during responses"""

# Connection Configuration Constants

PUB_QOS = 1
"""Publish Quality of service, service of 1 guarantees at least 1 delivery arrives at target, 0 means best effort not gurantee"""

SUB_QOS = 1
"""Subscribe QoS, similar to PUB_QOS"""

MQTT_PORT = 8883
"""Port used by secure MQTT service"""

CLIENT_ID = "lambda_service"
"""ID of this lambda handler function"""

ENDPT_FILE_PATH = "certs/accessPointID.txt"
"""relative file path that has accessPointID, access point ID can be obtained by obtaining the first part of the REST API in the aws IoT core console"""

AWS_ENDPOINT = ".iot.us-east-1.amazonaws.com"
"""The middle part of the endpoint that indicates regions of aws service"""

AUTHORITY_CERT_PATH = "certs/VeriSign-Class_3-Public-Primary-Certification-Authority-G5.pem"
"""Relative path to certifcate of authority"""

PRIVATE_KEY_PATH = "certs/private.pem.key"
"""Relative path to private key, downloaded from aws IoT"""

CERTIFICATE_PATH = "certs/certificate.pem.crt"
"""Relative path to device certificate, downloaded from aws IoT"""

# Reconnect time param in seconds
INITIAL_BACKOFF_TIME = 1
"""How may seconds to stop before retransmitting upon the first conflict in mqtt"""

MAX_BACKOFF_TIME = 5
"""Max seconds to stop before retransmitting upon continuous conflict in mqtt"""

STABLE_TIME = 3
"""How much time in seconds are considered stable, after this amount of time, the backoff time will be reset back to the initial level"""

DRAINING_FREQ = 5
"""How many requests that the Mqtt will try to resolve per seconds(the unit is Hz) if there is a big queue"""

CONNECT_DISCONNECT_TIMEOUT = 5
"""How many seconds to wait before concluding that the connect/disconnect operation has timed out"""

OPERATION_TIMEOUT = 4
"""How many seconds to wait before concluding that general operation(not special one like connect/disconenct) has timed out"""

OFFLINE_PUB_QUEUE = 3
"""Max number of requests to be queue while the lambda handler is offline, 0 for none, -1 for infinite"""

KEEP_ALIVE_SECONDS = 300
"""Duration between ping to mqtt server to indicate the intention to continue connection"""
