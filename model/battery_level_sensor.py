import asyncio
import json
import time
from request.mode_actuator_request import ModeActuator

class BatterySensor:
    def __init__(self, initial_level=100, decrease_rate_a=0.5, decrease_rate_b=0.25):
        self.initial_level = initial_level
        self.decrease_rate_a = decrease_rate_a
        self.decrease_rate_b = decrease_rate_b
        self.level = initial_level
        self.start_time = time.time()

    # Livello batteria che scende progressivamente quando il device è in "start"
    def get_decrease_level(self):
        elapsed_time = time.time() - self.start_time
        level = self.level - (elapsed_time * self.decrease_rate_a)
        level = max(level, 0)
        self.level = level
        return int(level)

    # Livello batteria che scende progressivamente quando il device è in "pause"
    def get_pause_level(self):
        elapsed_time = time.time() - self.start_time
        level = self.level - (elapsed_time * self.decrease_rate_b)
        level = max(level, 0)
        return int(level)


    def get_level(self, mode_actuator):
        current_level = 0
        if mode_actuator.get_mode() == ModeActuator.MODE_START:
            current_level = self.get_decrease_level()
        if mode_actuator.get_mode() == ModeActuator.MODE_PAUSE:
            current_level = self.get_pause_level()
        return int(current_level)


    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)


