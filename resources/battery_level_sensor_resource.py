'''import aiocoap
import aiocoap.resource as resource
import senml
from request.mode_actuator_request import ModeActuator
from request.switch_video_actuator_request import VideoSwitchActuator


class BatterySensorResource(resource.Resource):

    def __init__(self, battery_sensor, mode_actuator, video_switch, position_sensor):
        super().__init__()
        self.battery_sensor = battery_sensor
        self.mode_actuator = mode_actuator
        self.video_switch = video_switch
        self.position_sensor = position_sensor


    async def render_get(self, request):
        print("GET Request Received ...")
        current_level = self.battery_sensor.get_level(mode_actuator=self.mode_actuator)
        if current_level < 15:
            # Invia il comando di tornare alla stazione di ricarica
            self.video_switch.set_switch(VideoSwitchActuator.SWITCH_OFF)
            if current_level < 5:
                # Invia il comando di spegnersi
                self.mode_actuator.set_mode(ModeActuator.MODE_STOP)
                if current_level == 0:
                    return aiocoap.Message(payload=b"0")
                return aiocoap.Message(payload=b"shutting_down")
            return aiocoap.Message(payload=b"return_to_charging_station")

        payload = str(current_level).encode("utf-8")
        return aiocoap.Message(payload=payload)'''

'''
import aiocoap
import aiocoap.resource as resource
import json
from kpn_senml import *
import aiocoap.numbers as numbers
from senml import *

from request.mode_actuator_request import ModeActuator
from request.switch_video_actuator_request import VideoSwitchActuator


class BatterySensorResource(resource.Resource):

    def __init__(self, battery_sensor, mode_actuator, video_switch, position_sensor):
        super().__init__()
        self.battery_sensor = battery_sensor
        self.mode_actuator = mode_actuator
        self.video_switch = video_switch
        self.position_sensor = position_sensor
        self.ct = numbers.media_types_rev['application/senml+json']

        # Imposta gli attributi standard per la Resource Discovery CoAP
        self.rt = "battery-sensor"
        #self.iface = b"sensor"

    async def render_get(self, request):
        print("GET Request Received ...")
        current_level = self.battery_sensor.get_level(mode_actuator=self.mode_actuator)

        if current_level < 15:
            # Invia il comando di tornare alla stazione di ricarica
            self.video_switch.set_switch(VideoSwitchActuator.SWITCH_OFF)
            if current_level < 5:
                # Invia il comando di spegnersi
                self.mode_actuator.set_mode(ModeActuator.MODE_STOP)
                if current_level == 0:
                    # Creazione della lettura del sensore nel formato SenML
                    record = SenmlRecord(name="battery_level", unit="percent", value=0)
                else:
                    # Creazione della lettura del sensore nel formato SenML
                    record = SenmlRecord(name="battery_level", value=current_level) # value="shutting_down")
            else:
                # Creazione della lettura del sensore nel formato SenML
                record = SenmlRecord(name="battery_level", unit="percent", value=current_level)

            # Costruire il pacchetto SenML contenente la lettura del sensore
            senml_data = SenmlPack(self)

            # Aggiungere il record al documento SenML
            senml_data.add(record)

            # Convertire il pacchetto SenML in una stringa JSON
            senml_json = senml_data.to_json()

            # Impostare il formato di contenuto della risposta come application/senml+json
            response = aiocoap.Message(payload=senml_json.encode("utf-8"))
            response.opt.content_format = 11560  # Valore per il formato SenML JSON

            return response

        # Altrimenti, restituisci il livello di batteria come testo
        payload = str(current_level).encode("utf-8")
        return aiocoap.Message(content_format=numbers.media_types_rev['application/senml+json'],
                               payload=payload)

'''
import aiocoap
import json
import aiocoap.resource as resource
#from kpn_senml import *

from request.mode_actuator_request import ModeActuator
from request.switch_video_actuator_request import VideoSwitchActuator

class BatterySensorResource(resource.Resource):

    def __init__(self, battery_sensor, mode_actuator, video_switch, position_sensor):
        super().__init__()
        self.battery_sensor = battery_sensor
        self.mode_actuator = mode_actuator
        self.video_switch = video_switch
        self.position_sensor = position_sensor

    async def render_get(self, request):
        print("GET Request Received ...")
        current_level = self.battery_sensor.get_level(mode_actuator=self.mode_actuator)
        if current_level < 15:
            # Invia il comando di tornare alla stazione di ricarica
            self.video_switch.set_switch(VideoSwitchActuator.SWITCH_OFF)
            if current_level < 5:
                # Invia il comando di spegnersi
                self.mode_actuator.set_mode(ModeActuator.MODE_STOP)
                if current_level == 0:
                    # Creazione della lettura del sensore nel formato SenML
                    record = {"n": "battery_status", "u": "percent", "v": current_level}
                else:
                    # Creazione della lettura del sensore nel formato SenML
                    record = {"n": "battery_status", "u": "string", "v": "shutting_down"}
            else:
                # Creazione della lettura del sensore nel formato SenML
                record = {"n": "battery_status", "u": "string", "v": "returning_to_churging_station"}
        else:
            # Creazione della lettura del sensore nel formato SenML
            record = {"n": "battery_status", "u": "percent", "v": current_level}

        # Costruire il pacchetto SenML contenente la lettura del sensore
        senml_data = [record]

        # Convertire il pacchetto SenML in una stringa JSON
        senml_json = json.dumps(senml_data)

        # Creare la risposta CoAP con la stringa JSON come payload
        response = aiocoap.Message(payload=senml_json.encode("utf-8"))
        response.opt.content_format = 11560  # Valore per il formato SenML JSON

        return response



