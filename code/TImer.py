from settings import *

class Timer:
    def __init__(self,duration,func=None,repeat=False,autostart=False):
        self.duration=duration
        self.shoot_time=0
        self.active=False
        self.func=func
        self.repeat=repeat
        if autostart:
            self.activate()
    def __bool__(self):
        return self.active
    def activate(self):
        self.active=True
        self.shoot_time=pygame.time.get_ticks()

    def deactive(self):
        self.active=False
        self.shoot_time=0
        if self.repeat:self.activate()

    def update(self):
        if pygame.time.get_ticks()-self.shoot_time>=self.duration:
            if self.func and self.shoot_time!=0: self.func()
            self.deactive()
            

        