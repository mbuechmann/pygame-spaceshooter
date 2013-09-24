from pygame.constants import KEYDOWN, K_UP, KEYUP, K_LEFT, K_RIGHT, K_SPACE
from asteroid import Asteroid
from ship import Ship


class PlayState(object):
    def __init__(self, area):
        self.area = area
        self.ship = Ship(area)
        self.bullets = []
        self.asteroids = []
        self.asteroids.append(Asteroid(self.area))

    def logic(self, delta):
        self.ship.logic(delta)

        for bullet in self.bullets:
            bullet.logic(delta)

        self.bullets = [bullet for bullet in self.bullets if not bullet.is_dead()]

        for asteroid in self.asteroids:
            asteroid.logic(delta)
            new_asteroids = [child for asteroids in self.asteroids if asteroid.is_dead() for asteroid in asteroids for
                             children in asteroid.spawnChildren() for child in children]
            self.asteroids = [asteroid for asteroid in self.asteroids if not asteroid.is_dead()] + new_asteroids

    def render(self, screen):
        self.ship.render(screen)
        for bullet in self.bullets:
            bullet.render(screen)
        for asteroid in self.asteroids:
            asteroid.render(screen)

    def handle_event(self, event):
        if event.type == KEYDOWN or event.type == KEYUP:
            if event.key == K_UP:
                self.ship.accelerate(event.type == KEYDOWN)
            if event.key == K_LEFT:
                self.ship.steer_left(event.type == KEYDOWN)
            if event.key == K_RIGHT:
                self.ship.steer_right(event.type == KEYDOWN)
            if event.type == KEYDOWN and event.key == K_SPACE:
                self.bullets.append(self.ship.shootBullet())
