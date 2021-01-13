from .RCSkill import RCSkill
import keyboard  

class Getrdy(RCSkill):

    def __init__(self, start_key):
        self.name = "Getrdy"
        self.lock = True
        print("Load Getrdy Skill")
        self.start_key = start_key
    
    def go(self, frame):
        self.lock = True
        c = {"steering": 0, "throttle": 1}
        while True:
            try:
                if keyboard.is_pressed(self.start_key):
                    self.lock = False
                    break
            except:
                break
        return c
