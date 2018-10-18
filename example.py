import pygame
from machine import StateMachine, State


class Example(State):
    def __init__(self):
        # This will save the this instance to state machine
        State.__init__(self)

    # All draw code goes here
    def draw(self, surface):
        surface.fill((0,40,0))

    # Process all event here
    def event(self, event):
        if event.type == pygame.QUIT:
            # call state machine
            self.state.machine.quit()

if __name__ == '__main__':
    pygame.init()
    StateMachine.screen_center()
    # Create the state machine
    StateMachine('Example', 800, 600)
    # Create Example and set it to first state
    StateMachine.main_loop(Example())
    pygame.quit()
