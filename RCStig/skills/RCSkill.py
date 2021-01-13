from logging import fatal


class RCSkill(object):

    def __init__(self):
        self.name = "RCSkill"
        self.lock = False

    def go(frame):
        return {1,1,1,1,1,1}

    def activate(self, current_controls):
        print("activate skill:" + self.name)
    
    def reset(self):
        print("reset skill:" + self.name)