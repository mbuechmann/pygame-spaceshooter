import pygame
import numpy
from pygame.constants import KEYDOWN, K_UP, KEYUP, K_LEFT, K_RIGHT, K_SPACE
from asteroid import Asteroid
import game_over_state
from ship import Ship


class PlayState(object):
    FONT_LOCATION = 'assets/Vectorb.ttf'
    FONT_PADDING = 10
    LIVES_ORIGIN = (20, 24)
    LIVES_OFFSET = (20, 0)

    def __init__(self, game):
        self.game = game
        self.ship = Ship(game.AREA)
        self.bullets = []
        self.asteroids = []
        self.asteroids.append(Asteroid(game.AREA))
        self.score = 0
        self.level = 1
        self.lives = 3
        self.font = pygame.font.Font(self.FONT_LOCATION, game.MEDIUM_FONT_SIZE)

    def logic(self, delta):
        if self.ship is not None:
            self.ship.logic(delta)

        for bullet in self.bullets:
            bullet.logic(delta)

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

            if self.ship is not None:
                for asteroid in self.asteroids:
                    if asteroid.collides_with_ship(self.ship):
                        self.ship.die()
                        self.ship = None
                        self.lives -= 1
                        if self.lives == 0:
                            self.game.set_current_state(game_over_state.GameOverState(self.game))
                        break

        self.bullets = [bullet for bullet in self.bullets if not bullet.is_dead()]

    def render(self, screen):
        if self.ship is not None:
            self.ship.render(screen)
        for bullet in self.bullets:
            bullet.render(screen)
        for asteroid in self.asteroids:
            asteroid.render(screen)
        self._render_score(screen)
        self._render_level(screen)
        self._render_lives(screen)

    def handle_event(self, event):
        if event.type == KEYDOWN or event.type == KEYUP:
            if self.ship is not None:
                if event.key == K_UP:
                    self.ship.accelerate(event.type == KEYDOWN)
                if event.key == K_LEFT:
                    self.ship.steer_left(event.type == KEYDOWN)
                if event.key == K_RIGHT:
                    self.ship.steer_right(event.type == KEYDOWN)

            if event.type == KEYDOWN and event.key == K_SPACE:
                if self.ship is not None:
                    self.bullets.append(self.ship.shoot_bullet())
                else:
                    self.ship = Ship(self.game.AREA)

    def _render_score(self, screen):
        string = '%d' % self.score
        if self.score < 10:
            string = '000' + string
        elif self.score < 100:
            string = '00' + string
        elif self.score < 1000:
            string = '0' + string
        text = self.font.render(string, False, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.top = self.FONT_PADDING
        text_rect.right = screen.get_width() - self.FONT_PADDING
        screen.blit(text, text_rect)

    def _render_level(self, screen):
        string = '%d' % self.level
        if self.level < 10:
            string = '0' + string
        text = self.font.render(string, False, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.top = self.FONT_PADDING
        text_rect.centerx = screen.get_rect().centerx
        screen.blit(text, text_rect)

    def _render_lives(self, screen):
        shape = numpy.add(Ship.SHIP_SHAPE.coords, self.LIVES_ORIGIN)
        for x in xrange(self.lives):
            points = numpy.add(shape, numpy.multiply(self.LIVES_OFFSET, x))
            pygame.draw.lines(screen, (255, 255, 255), True, points)
