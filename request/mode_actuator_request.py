import json

class ModeActuator:
    MODE_START = "start"
    MODE_PAUSE = "pause"
    MODE_STOP = "stop"

    def __init__(self):
        self.mode = self.MODE_STOP

    def set_mode(self, mode):
        self.mode = mode

    def get_mode(self):
        return self.mode

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)
