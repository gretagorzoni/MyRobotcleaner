import json
import random
import asyncio
import time

class PositionSensor:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def initial_position(self):
        self.x = 0.0
        self.y = 0.0
        return self.x, self.y

    def set_position(self, position):
        self.position = position

    def get_position(self):
        self.x = random.uniform(0, 1)
        self.y = random.uniform(0, 1)
        self.timestamp = int(time.time())
        return self.x, self.y

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)