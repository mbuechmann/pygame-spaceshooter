import pygame
from pygame.constants import KEYDOWN, K_UP, KEYUP, K_LEFT, K_RIGHT, K_SPACE
from asteroid import Asteroid
from ship import Ship


class PlayState(object):
    FONT_LOCATION = 'assets/Vectorb.ttf'
    FONT_Y = 10

    def __init__(self, area):
        self.area = area
        self.ship = Ship(area)
        self.bullets = []
        self.asteroids = []
        self.asteroids.append(Asteroid(self.area))
        self.score = 0
        self.score_font = pygame.font.Font(self.FONT_LOCATION, 45)

    def logic(self, delta):
        self.ship.logic(delta)

        for asteroid in self.asteroids:
            asteroid.logic(delta)

            for bullet in self.bullets:
                if asteroid.collides_with_bullet(bullet):
                    bullet.die()
                    asteroid.die()
                    self.score += 4 - asteroid.size
                    break

            new_asteroids = []
            for asteroid in self.asteroids:
                for child in asteroid.spawn_children():
                    if asteroid.is_dead():
                        new_asteroids.append(child)

            self.asteroids = [asteroid for asteroid in self.asteroids if not asteroid.is_dead()] + new_asteroids

        for bullet in self.bullets:
            bullet.logic(delta)

        self.bullets = [bullet for bullet in self.bullets if not bullet.is_dead()]

    def render(self, screen):
        self.ship.render(screen)
        for bullet in self.bullets:
            bullet.render(screen)
        for asteroid in self.asteroids:
            asteroid.render(screen)
        self._render_score(screen)

    def handle_event(self, event):
        if event.type == KEYDOWN or event.type == KEYUP:
            if event.key == K_UP:
                self.ship.accelerate(event.type == KEYDOWN)
            if event.key == K_LEFT:
                self.ship.steer_left(event.type == KEYDOWN)
            if event.key == K_RIGHT:
                self.ship.steer_right(event.type == KEYDOWN)
            if event.type == KEYDOWN and event.key == K_SPACE:
                self.bullets.append(self.ship.shoot_bullet())

    def _render_score(self, screen):
        string = '%d' % self.score
        if self.score < 10:
            string = '000' + string
        elif self.score < 100:
            string = '00' + string
        elif self.score < 1000:
            string = '0' + string
        text = self.score_font.render(string, False, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.centerx = screen.get_rect().centerx
        text_rect.y = self.FONT_Y
        screen.blit(text, text_rect)
