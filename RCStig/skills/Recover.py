from .RCSkill import RCSkill
import time

class Recover(RCSkill):

    def __init__(self):
      self.name = "Recover"
      self.runtime = 0
      self.start_controlls = False
      self.max_runtime = 660
      self.lock = True

      print("Load Recover Skill")

    def activate(self, start_controlls):
      self.lock = True
      self.runtime = 0
      self.start_time = int(round(time.time() * 1000))
      self.start_controlls = start_controlls
      if self.start_controlls["steering"] == 0:
        self.start_controlls["steering"] = -0.3

    def go(self, frame):
      self.runtime = int(round(time.time() * 1000)) - self.start_time
      if self.runtime < self.max_runtime:
        c = {"steering": (self.start_controlls["steering"]*(-1)) - 0.3, "gear": -1, "throttle": 0.9}
      else:
        c = {"steering": self.start_controlls["steering"], "gear": 1, "throttle": 1}
        self.lock = False
      
      return c

