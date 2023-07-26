import logging
import asyncio
import aiocoap.resource as resource
import aiocoap
import warnings
import time
from model.battery_level_sensor import BatterySensor
from model.position_sensor import PositionSensor
from request.mode_actuator_request import ModeActuator
from request.switch_video_actuator_request import VideoSwitchActuator
from resources.battery_level_sensor_resource import BatterySensorResource
from resources.position_sensor_resource import PositionSensorResource
from resources.operating_mode_actuator_resource import ModeActuatorResource
from resources.switch_video_actuator_resource import VideoSwitchActuatorResource

logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server-1").setLevel(logging.INFO)

warnings.simplefilter(action='ignore', category=FutureWarning)

class RobotCleanerCoapProcess:
    def __init__(self, port):

        self.video_switch_actuator = None
        self.mode_actuator = None
        self.position_sensor = None
        self.battery_sensor = None
        asyncio.run(self.main(port))

    async def main(self, port):
        root = resource.Site()

        # Creazione degli oggetti per i sensori e gli attuatori
        self.battery_sensor = BatterySensor()
        self.position_sensor = PositionSensor(0, 0)
        self.mode_actuator = ModeActuator()
        self.video_switch_actuator = VideoSwitchActuator()

        # Creazione delle risorse
        battery_resource = BatterySensorResource(self.battery_sensor, self.mode_actuator, self.video_switch_actuator, self.position_sensor)
        position_resource = PositionSensorResource(self.position_sensor, self.mode_actuator)
        mode_resource = ModeActuatorResource(self.mode_actuator)
        video_switch_resource = VideoSwitchActuatorResource(self.video_switch_actuator)

        # Aggiunta delle risorse alla root del server
        root.add_resource(['battery_level'], battery_resource)
        root.add_resource(['position'], position_resource)
        root.add_resource(['operating_mode'], mode_resource)
        root.add_resource(['video_switch'], video_switch_resource)

        # Avvio del server CoAP
        asyncio.Task(aiocoap.Context.create_server_context(root, bind=('127.0.0.1', port)))

        print("CoAP server started on port ", str(port))
        await asyncio.sleep(3600)  # Il server rimane attivo per 1 ora

if __name__ == "__main__":
    robot = RobotCleanerCoapProcess(port=5693)
