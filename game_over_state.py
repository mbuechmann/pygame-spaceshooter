import pygame
from pygame.constants import KEYDOWN, K_SPACE
import play_state


class GameOverState(object):
    BLINK_INTERVAL = 2
    PRESS_FIRE_TEXT = "Press Fire to Start"
    GAME_OVER_TEXT = "Game Over"
    FONT_LOCATION = 'assets/Vectorb.ttf'

    def __init__(self, game):
        self.game = game

        self.game_over_font = pygame.font.Font(self.FONT_LOCATION, game.LARGE_FONT_SIZE)
        self.game_over_text = self.game_over_font.render(self.GAME_OVER_TEXT, False, (255, 255, 255))

        self.blink_time = 0
        self.press_fire_font = pygame.font.Font(self.FONT_LOCATION, game.SMALL_FONT_SIZE)
        self.press_fire_text = self.press_fire_font.render(self.PRESS_FIRE_TEXT, False, (255, 255, 255))

    def logic(self, delta):
        self.blink_time = (self.blink_time + delta) % self.BLINK_INTERVAL

    def render(self, screen):
        text_rect = self.game_over_text.get_rect()
        text_rect.centery = screen.get_rect().height / 3
        text_rect.centerx = screen.get_rect().centerx
        screen.blit(self.game_over_text, text_rect)

        if self.blink_time < self.BLINK_INTERVAL / 2:
            text_rect = self.press_fire_text.get_rect()
            text_rect.centery = screen.get_rect().height / 3 * 2
            text_rect.centerx = screen.get_rect().centerx
            screen.blit(self.press_fire_text, text_rect)

    def handle_event(self, event):
        if event.type == KEYDOWN and event.key == K_SPACE:
            self.game.set_current_state(play_state.PlayState(self.game))
