import pygame

class TickTimerData:
    def __init__(self, parent, interval, callback , pydata):
        self.parent = parent
        self.next_tick = parent.ticks + interval
        self.identity = parent.identity
        self.interval = interval
        self.callback = callback
        self.pydata = pydata
        self.stop = False
        self.count = 0

    def add(self):
        self.parent.timers[self.identity] = self

    def pop(self):
        self.stop = True
        self.parent.pop(self.identity)

    def reset(self):
        self.next_tick = self.parent.ticks + self.interval

    def restart(self):
        self.stop = False
        self.reset()

    def update(self):
        if not self.stop:
            self.count = 0
            # avoid infinite loop
            if self.interval != 0:
                while self.parent.ticks > self.next_tick:
                    self.next_tick += self.interval
                    self.count += 1

            if self.count > 0 or self.interval == 0:
                self.callback(self)

class TickTimer:
    def __init__(self):
        self.ticks = pygame.time.get_ticks()
        self.identity = 0
        self.timers = {}
        self.pop_timers = []

    def __call__(self, interval, callback, pydata=None):
        timer = TickTimerData(self, interval, callback, pydata)
        self.timers[self.identity] = timer
        self.identity += 1
        return timer

    def pop(self, identity):
        self.pop_timers.append(identity)

    def reset(self):
        for key in self.timers.keys():
            self.timers[key].reset()

    def tick(self):
        self.ticks = pygame.time.get_ticks()

    def update(self):
        self.ticks = pygame.time.get_ticks()
        for key in self.timers.keys():
            self.timers[key].update()

        for identity in self.pop_timers:
            del self.timers[identity]

        self.pop_timers = []
