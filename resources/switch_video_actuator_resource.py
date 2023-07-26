import aiocoap.resource as resource
import aiocoap
from aiocoap.numbers.codes import Code

class VideoSwitchActuatorResource(resource.Resource):
    def __init__(self, video_switch_actuator):
        super().__init__()
        self.video_switch_actuator = video_switch_actuator

    async def render_get(self, request):
        switch = self.video_switch_actuator.get_switch()
        payload = switch.encode("utf-8")
        return aiocoap.Message(payload=payload)

    async def render_post(self, request):
        self.video_switch_actuator.set_switch("ON")
        return aiocoap.Message(code=aiocoap.CHANGED, payload=b"Switch updated")
