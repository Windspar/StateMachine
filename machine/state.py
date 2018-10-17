import pygame
from .timer import TickTimer

class StateMethods:
    machine = None

    def __init__(self, parent):
        self.parent = parent
        self.timer = TickTimer()
        self.previous_state = None

    def flip(self, classname, *args, **kwargs):
        self.machine.bus.register_event("Next State", classname, *args, **kwargs)
        #self.machine.next_state = classname, args, kwargs

    def flip_back(self, *args, **kwargs):
        self.machine.bus.register_event("Next State", self.previous_state, *args, **kwargs)
        #self.machine.next_state = self.previous_state, args, kwargs

    def screen_entrance(self, regain_focus, previous_state, *args, **kwargs):
        if previous_state:
            self.previous_state = previous_state

        self.timer.tick()
        self.timer.reset()
        self.parent.__dict__.update(kwargs)
        self.parent.entrance(regain_focus, *args)

    def screen_draw(self, surface):
        self.parent.draw(surface)
        self.timer.update()
        self.parent.update(self.timer.ticks, self.machine.delta)

    def screen_event(self, event):
        self.parent.event(event)

class State:
    def __init__(self, state_name=None):
        self.state = StateMethods(self)
        if state_name is None:
            state_name = self.__class__.__name__

        self.state.machine.instances[state_name] = self

    def draw(self, surface):
        pass

    def drop(self):
        pass

    def entrance(self, regain_focus):
        pass

    def event(self, event):
        pass

    def update(self, ticks, delta):
        pass
