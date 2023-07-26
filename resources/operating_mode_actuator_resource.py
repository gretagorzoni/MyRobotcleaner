import aiocoap.resource as resource
import aiocoap
from aiocoap.numbers.codes import Code

class ModeActuatorResource(resource.Resource):
    def __init__(self, mode_actuator):
        super().__init__()
        self.mode_actuator = mode_actuator

    async def render_get(self, request):
        print("GET Request Received ...")
        mode = self.mode_actuator.get_mode()
        payload = mode.encode("utf-8")
        return aiocoap.Message(payload=payload)

    async def render_put(self, request):
        payload = request.payload.decode("utf-8")
        self.mode_actuator.set_mode(payload)
        return aiocoap.Message(code=aiocoap.CHANGED, payload=b"Mode updated")

    async def render_post(self, request):
        self.mode_actuator.set_mode("start")
        return aiocoap.Message(code=aiocoap.CHANGED, payload=b"Mode updated")
