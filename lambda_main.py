"""
.. module:: lambda_main
    :synopsis: entry point for lambda handler

"""


# Borrow a lot from:
# https://github.com/alexa/alexa-smarthome/tree/master/sample_lambda/python

# -*- coding: utf-8 -*-

# Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Amazon Software License (the "License"). You may not use this file except in
# compliance with the License. A copy of the License is located at
#
#     http://aws.amazon.com/asl/
#
# or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, express or implied. See the License for the specific
# language governing permissions and limitations under the License.

import logging
import time
import json
import uuid
import sys
sys.path.append('src/')
sys.path.append('validator/')

import utils
import lambda_master_handler

import sys
import os
from validation import validate_message

from AWSIoTPythonSDK.exception.AWSIoTExceptions import disconnectTimeoutException, connectTimeoutException

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(req, context):
    """
    This is where the program begins and where the program will end, its return value will be forwarded to Alexa 
        :param req: the message from Alexa
        :param context: execution context of the message, not used
        :return: json dict that if valid, will be turned into Alexa speech response to user 
    """

    try:
        logger.info("Directive:")
        logger.info(json.dumps(req, indent=4, sort_keys=True))
        version = utils.get_directive_version(req)

        if version == "3":
            try:
                masterHandler = lambda_master_handler.MasterHandler()

            except connectTimeoutException:
                logger.warning("Connection timeout")

            logger.info("Received v3 directive!")

            if req["directive"]["header"]["name"] == "Discover":
                # discovery is used to help Alexa knows what devices exist as well as what can be done with them
                response = masterHandler.handleDiscoveryV3(req)
            else:
                response = masterHandler.handleNonDiscoveryV3(req, context)
            # logger.info("Resp:")
            # logger.info(json.dumps(response, indent=4, sort_keys=True))

            # check the response against amazon json schema
            validate_message(req, response)

            # disconnect from mqtt server
            try:
                while False == masterHandler._mqttManager._myAWSIoTMQTTClient.disconnect():
                    pass
            except disconnectTimeoutException:
                logger.warning("Disconnect timed out")

        else:
            # we shouldn't be receiving v2 directive for the devices that are being used
            logger.info("Received v2 directive!")

            response = masterHandler.handleErrorResponse(
                req, "Unsupported Directive Version", "V2 directive Received")

        return response
    except ValueError as error:
        logger.error(error)
        raise
