import pygame
from random import choice, randint
from machine import StateMachine, State

class Block:
    def __init__(self):
        self.rect = pygame.Rect(randint(50,700), randint(50,700), 50, 50)
        self.colors = [pygame.Color(*color) for color in [(0,200,0), (200,0,0), (0,200,200)]]
        self.color = choice(self.colors)
        slow = 500
        self.direction = [(randint(0, 401) - 200) / slow, (randint(0, 401) - 200) / slow]
        self.position = list(self.rect.topleft)

    def draw(self, surface):
        surface.fill(self.color, self.rect)

    def update(self, delta, surface_rect):
        self.position[0] += self.direction[0] * delta
        self.position[1] += self.direction[1] * delta
        self.rect.topleft = list(map(int, self.position))
        boolean_clamp = False
        rect = self.rect.clamp(surface_rect)
        if rect.x != self.rect.x:
            self.direction[0] = -self.direction[0]
            boolean_clamp = True

        if rect.y != self.rect.y:
            self.direction[1] = -self.direction[1]
            boolean_clamp = True

        if boolean_clamp:
            self.rect = rect
            self.position = list(self.rect.topleft)

class Test(State):
    def __init__(self):
        State.__init__(self)
        self.state.timer(20, self.lighten)
        self.color = pygame.Color(0,0,0)
        self.colors = [pygame.Color(*color) for color in [(0,40,0), (40,0,0), (0,40,40)]]
        self.block = Block()

    def draw(self, surface):
        surface.fill(self.color)
        self.block.draw(surface)

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.state.flip('Test2', color=choice(self.colors))
        elif event.type == pygame.QUIT:
            self.state.machine.quit()

    def fade(self, timer):
        if self.color.b - timer.count < 1:
            self.color.b = 0
            timer.callback = self.lighten
        else:
            self.color.b -= timer.count

    def lighten(self, timer):
        if self.color.b + timer.count > 254:
            self.color.b = 255
            timer.callback = self.fade
        else:
            self.color.b += timer.count

    def update(self, ticks, delta):
        self.block.update(delta, self.state.machine.rect)

class Test2(State):
    def __init__(self):
        State.__init__(self)
        self.color = pygame.Color(0,40,0)

    def draw(self, surface):
        surface.fill(self.color)

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.state.flip_back()
        elif event.type == pygame.QUIT:
            self.state.machine.quit()

def main():
    pygame.init()
    StateMachine.screen_center()
    StateMachine("Test", 800, 600)
    Test2()
    StateMachine.main_loop(Test())

main()
