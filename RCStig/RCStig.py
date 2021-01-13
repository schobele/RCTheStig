#!/usr/bin/env python3
from re import T
from .skills import Class3Model
from .skills import Recover
from .skills import Getrdy
from collections import deque
from skimage.measure import compare_ssim
from skimage.color import rgb2gray
from skimage.util import crop


class RCStig(object):
    
    def __init__(self, name, race):
        self.name = name
        self.steering = 0
        self.throttle = 0.8
        self.gear = 1
        self.frame_counter = 0
        self.frame_history = deque([])
        self.frame_history_counter = 0
        self.history_ssim_score = 0

        #slow but okay c3m = Class3Model.Class3Model(left_val=-0.75, right_val=0.75,throttle=0.6, min_acc=76)
        #c3m = Class3Model.Class3Model(left_val=-0.81, right_val=0.81,throttle=0.74, min_acc=76)
        c3m = Class3Model.Class3Model(left_val=-0.79, right_val=0.79,throttle=0.58, min_acc=76, model_path="./RCStig/models/classification_model_6")

        recover = Recover.Recover()
        getready = Getrdy.Getrdy(start_key="q")

        self.skills = {"getready": getready, "drive_default": c3m, "recover": recover}
        self.race = race
        self.active_skill = self.skills["getready"]

    def act(self, frame):
        frame = rgb2gray(frame)
        #frame = frame[0:149, 0:320] # for deltax_i8_02

        self.frame_counter += 1;
        if self.frame_counter % 5 == 0:
            self.frame_history_counter += 1
            self.frame_history.append(frame)
            if len(self.frame_history) > 5:
                self.frame_history.popleft()
        
        self.check_skill(frame)

        if self.active_skill:
            reaction = self.active_skill.go(frame)
            self.update_controls(reaction)
        else:
            self.active_skill = self.skills[0]

    def update_controls(self, controls):
        self.steering = controls["steering"]
        if "throttle" in controls:
            self.throttle = controls["throttle"]
        if "gear" in controls:
            self.gear = controls["gear"]

    def activate_skill(self, skill):
        if self.active_skill:
            self.active_skill.reset()
        self.skillprogress = 0.0
        skill.activate({"steering":self.steering, "throttle": self.throttle, "gear": self.gear})
        self.active_skill = skill

    def check_need_recover(self, frame):
        recover_needed = False
        if len(self.frame_history) >= 5:
            score = compare_ssim( self.frame_history[0], frame)
            if score > 0.7 and self.history_ssim_score > 0.7:
                recover_needed = True
                print("score1: ", score)
            self.history_ssim_score = score
        return recover_needed

    def check_skill(self, frame):
        new_skill = self.skills["drive_default"]
        
        if self.check_need_recover(frame):
            new_skill = self.skills["recover"]
        
        if self.active_skill.lock == False and self.active_skill.name != new_skill.name:
            self.activate_skill(new_skill)

    def getControls(self):
        return {"steering":self.steering, "throttle": self.throttle, "gear": self.gear}
