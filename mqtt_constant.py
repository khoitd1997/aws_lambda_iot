"""
Used for storing constants related to MQTT operations
"""
import json

# Communication quality constant
UNCERTAINTY_MS = 200

# Connection Configuration Constants
PUB_QOS = 1
SUB_QOS = 1
MQTT_PORT = 8883

CLIENT_ID = "lambda_service"
ENDPT_FILE_PATH = "certs/accessPointID.txt"
AWS_ENDPOINT = ".iot.us-east-1.amazonaws.com"

AUTHORITY_CERT_PATH = "certs/VeriSign-Class_3-Public-Primary-Certification-Authority-G5.pem"
PRIVATE_KEY_PATH = "certs/private.pem.key"
CERTIFICATE_PATH = "certs/certificate.pem.crt"

# Reconnect time param in seconds
INITIAL_BACKOFF_TIME = 1
MAX_BACKOFF_TIME = 5
STABLE_TIME = 3

DRAINING_FREQ = 5  # Hz
CONNECT_DISCONNECT_TIMEOUT = 5  # seconds
OPERATION_TIMEOUT = 4  # seconds
OFFLINE_PUB_QUEUE = 3  # -1 for inifinite pub

KEEP_ALIVE_SECONDS = 300  # duration between ping to server

# how much time pass before retry
RETRY_TIMEOUT_SEC = 5
