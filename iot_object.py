"""
.. module:: project_documentation
    :synopsis: define a class representation of an IoT target(like pc controller) of the lambda handler

.. moduleauthor:: Khoi Trinh
"""

from abc import ABCMeta, abstractmethod
import utils
import copy

pcControllerAwsProfile = {
    "endpointId": "endpoint-001",
    "manufacturerName": "Kd",
    "friendlyName": "my computer",
    "description": "Controller that controls and monitor the desktop PC",
    "displayCategories": [
        "SWITCH", "TEMPERATURE_SENSOR"
    ],
    "cookie": {},
    "capabilities": [
        {
            "type": "AlexaInterface",
            "interface": "Alexa",
            "version": "3"
        },
        {
            "type": "AlexaInterface",
            "interface": "Alexa.PowerController",
            "version": "3",
            "properties": {
                "supported": [
                    {
                        "name": "powerState"
                    }
                ],
                "proactivelyReported": True,
                "retrievable": True
            }
        },
        {
            "type": "AlexaInterface",
            "interface": "Alexa.EndpointHealth",
            "version": "3",
            "properties": {
                "supported": [
                    {
                        "name": "connectivity"
                    }
                ],
                "proactivelyReported": True,
                "retrievable": True
            }
        },
        {
            "type": "AlexaInterface",
            "interface": "Alexa.TemperatureSensor",
            "version": "3",
            "properties": {
                "supported": [
                    {
                        "name": "temperature"
                    }
                ],
                "proactivelyReported": True,
                "retrievable": True
            }
        }
    ]
}
"""the pc controller aws profile"""

# source: https://developer.amazon.com/fr/docs/device-apis/alexa-temperaturesensor.html

bedRoomLightAwsProfile = {
    "endpointId": "endpoint-002",
    "manufacturerName": "Kd",
                        "friendlyName": "bed room light",
                        "description": "Controller for bed room light",
                        "displayCategories": [
                            "SWITCH"
                        ],
    "cookie": {},
    "capabilities": [
        {
            "type": "AlexaInterface",
            "interface": "Alexa",
            "version": "3"
        },
        {
            "type": "AlexaInterface",
            "interface": "Alexa.PowerController",
            "version": "3",
            "properties": {
                "supported": [
                    {
                        "name": "powerState"
                    }
                ],
                "proactivelyReported": True,
                "retrievable": True
            }
        }
                        ]
}
"""the bed room light controller aws profile"""

thermostatAwsProfile = {
    "endpointId": "endpoint-004",
    "manufacturerName": "Kd",
                        "friendlyName": "thermostat",
                        "description": "Adjust temperature level",
                        "displayCategories": [
                            "THERMOSTAT"
                        ],
    "cookie": {},
    "capabilities": [
        {
            "type": "AlexaInterface",
            "interface": "Alexa",
            "version": "3"
        },
                            {
                                "type": "AlexaInterface",
                                "interface": "Alexa.ThermostatController",
                                "version": "3",
                                "properties": {
                                    "supported": [
                                        {
                                            "name": "AdjustTargetTemperature"
                                        },
                                        {
                                            "name": "SetTargetTemperature"
                                        }
                                    ],
                                    "proactivelyReported": True,
                                    "retrievable": True
                                }
        },
                            {
                                "type": "AlexaInterface",
                                "interface": "Alexa.EndpointHealth",
                                "version": "3",
                                "properties": {
                                    "supported": [
                                        {
                                            "name": "connectivity"
                                        }
                                    ],
                                    "proactivelyReported": True,
                                    "retrievable": True
                                }
        }
                        ]
}
"""the thermostat aws profile"""


class IotObject:
    """Represents an IoT devices that can be discovered by Alexa smart home"""

    def __init__(self, pubTopic, subTopic, awsObjectProfile):
        """
        create iot objects
            :param self: 
            :param pubTopic: MQTT topic that this device publishses to 
            :param subTopic: MQTT topic that this device subscribes to
            :param awsObjectProfile: the dictionary containing the aws profile of this object, the profile allocates the endpoints, specifies the capabilities, friendly name(which the user called to invoke)
        """
        self.subTopic = subTopic
        self.pubTopic = pubTopic
        self.awsObjectProfile = awsObjectProfile


pcController = IotObject(
    "/pcRes", "/pcReq", pcControllerAwsProfile)


bedRoomLightController = IotObject(
    "/bedRoomLightRes", "/bedRoomLightReq", bedRoomLightAwsProfile)


IOT_OBJ_LIST = [pcController, bedRoomLightController]
""" List of all IoT devices that are supported by this lambda function"""
