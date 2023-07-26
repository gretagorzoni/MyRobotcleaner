import asyncio
import random

import aiocoap.resource as resource
import aiocoap
from request.mode_actuator_request import ModeActuator

class PositionSensorResource(resource.Resource):
    def __init__(self, position_sensor, mode_actuator):
        super().__init__()
        self.position_sensor = position_sensor
        self.mode_actuator = mode_actuator
        self.last_position = (0, 0)


    async def render_get(self, request):
        print("GET Request Received ...")
        if self.mode_actuator.get_mode() == ModeActuator.MODE_START:
            position = self.position_sensor.get_position()
            self.last_position = position
            payload = f"{position[0]}, {position[1]}".encode("utf-8")
            return aiocoap.Message(payload=payload)

        if self.mode_actuator.get_mode() == ModeActuator.MODE_PAUSE:
            payload = f"{self.last_position[0]}, {self.last_position[1]}".encode("utf-8")
            return aiocoap.Message(payload=payload)

        return aiocoap.Message(payload=b"0, 0")
