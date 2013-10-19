import pygame
from pygame.constants import KEYDOWN, K_ESCAPE
from game_over_state import GameOverState
import time


class Game(object):

    AREA = (800, 800)
    LARGE_FONT_SIZE = 45
    MEDIUM_FONT_SIZE = 20
    SMALL_FONT_SIZE = 15

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.AREA)
        self.current_state = GameOverState(self)
        self.running = True

    def set_current_state(self, state):
        self.current_state = state

    def run(self):
        last_time = time.time()

        while self.running:
            now = time.time()
            delta = now - last_time
            self.handle_events()
            self.logic(delta)
            self.render()
            last_time = now

    def handle_events(self):
        event = pygame.event.poll()
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            self.running = False
        else:
            self.current_state.handle_event(event)

    def logic(self, delta):
        self.current_state.logic(delta)

    def render(self):
        self.screen.fill((0, 0, 0))
        self.current_state.render(self.screen)
        pygame.display.flip()
