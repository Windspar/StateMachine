import pygame
from machine import StateMachine, State

class BaseState(State):
    def __init__(self, flip):
        # This will save the this instance to state machine
        State.__init__(self)
        self.flip = flip

        font = pygame.font.Font(None, 24)
        self.text = font.render('Press spacebar to flip', 1, (240, 240, 240))
        self.text_rect = self.text.get_rect()
        self.text_rect.centerx = self.state.machine.rect.centerx
        self.text_rect.bottom = self.state.machine.rect.bottom - 2

    def event(self, event):
        if event.type == pygame.QUIT:
            # call state machine
            self.state.machine.quit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # changes state
                self.state.flip(self.flip)

class Game(BaseState):
    def __init__(self):
        # This will save the this instance to state machine
        BaseState.__init__(self, 'Intro')

    # All draw code goes here
    def draw(self, surface):
        surface.fill((0,0,40))
        surface.blit(self.text, self.text_rect)

class Intro(BaseState):
    def __init__(self):
        # This will save the this instance to state machine
        BaseState.__init__(self, 'Game')

    # All draw code goes here
    def draw(self, surface):
        surface.fill((0,40,0))
        surface.blit(self.text, self.text_rect)

if __name__ == '__main__':
    pygame.init()
    StateMachine.screen_center()
    # Create the state machine
    StateMachine('Example Flip', 800, 600)
    # Create states
    Game()
    # Create Intro and set it to first state
    StateMachine.main_loop(Intro())
    pygame.quit()
