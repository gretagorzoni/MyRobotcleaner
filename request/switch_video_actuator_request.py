import json

class VideoSwitchActuator:
    SWITCH_ON = "On"
    SWITCH_OFF = "Off"

    def __init__(self):
        self.switch = self.SWITCH_OFF

    def set_switch(self, switch):
        self.switch = switch

    def get_switch(self):
        return self.switch

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)
