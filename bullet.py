import numpy
import pygame
import math
from game_object import GameObject


class Bullet(GameObject):

    SPEED = 450
    TTL = 3

    def __init__(self, area, position, rotation):
        super(Bullet, self).__init__(area)
        self.position = position
        self.last_position = position
        self.vx = math.sin(rotation / 180 * math.pi) * self.SPEED
        self.vy = -math.cos(rotation / 180 * math.pi) * self.SPEED
        self.speed = (self.vx, self.vy)
        self.ttl = self.TTL

    def render(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.position[0] - 1, self.position[1] - 1, 2, 2))

    def logic(self, delta):
        delta_speed = numpy.multiply(self.speed, delta)
        self.last_position = numpy.subtract(self.position, delta_speed)
        self.move(delta)
        self.ttl -= delta

    def is_dead(self):
        return self.dead or self.ttl <= 0
