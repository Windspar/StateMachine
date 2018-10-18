import os
import pygame
from .state import StateMethods, State
from .eventbus import EventBus

class StateMachine:
    def __init__(self, title, width, height, flags=0, bus=EventBus()):
        pygame.display.set_caption(title)
        self.surface = pygame.display.set_mode((width, height), flags)
        self.rect = self.surface.get_rect()
        self.clock = pygame.time.Clock()
        self.current = None
        self.instances = {}
        self.delta = 0

        self.bus = bus
        self.bus.listener('Next State', self.listener_next_state)

        # changable variables
        self.running = False
        self.fps = 30

        StateMethods.machine = self

    def listener_next_state(self, state_name, *args, **kwargs):
        # clean up
        if self.current:
            self.current.drop()

        if isinstance(state_name, State):
            self.current = state_name
            previous_state = None
            regain_focus = True
        else:
            regain_focus = False
            previous_state = self.current
            self.current = self.instances[state_name]

        # start the next state
        self.current.state.screen_entrance(regain_focus, previous_state, *args, **kwargs)

    def loop(self, state):
        # set the initial state
        self.listener_next_state(state)
        self.running = True
        while self.running:
            self.bus.process()
            for event in pygame.event.get():
                self.current.state.screen_event(event)

            self.current.state.screen_draw(self.surface)
            pygame.display.flip()
            self.delta = self.clock.tick(self.fps)

    def quit(self):
        self.running = False

    @classmethod
    def load_states(cls, path):
        pass

    @staticmethod
    def main_loop(state):
        StateMethods.machine.loop(state)

    @staticmethod
    def screen_center():
        os.environ['SDL_VIDEO_CENTERED'] = '1'

    @staticmethod
    def screen_position(x, y):
        os.environ['SDL_VIDEO_WINDOW_POS'] = '{0}, {1}'.format(x, y)
