import pygame
import math
import numpy
from bullet import Bullet
from game_object import GameObject
from shapely.geometry import Polygon
from shapely.geometry import LineString


class Ship(GameObject):

    SHIP_SHAPE = LineString([(0.0, -10.0), (5.0, 5.0), (0.0, 0.0), (-5.0, 5.0)])
    THRUSTER_SHAPE = LineString([(-3, 2), (0, 7), (3, 2)])
    MAX_SPEED = 100
    ACCELERATION = 10
    ROTATION_SPEED = 180
    TTD = 3

    def __init__(self, area):
        super(Ship, self).__init__(area)
        self.position = (area[0] / 2, area[1] / 2)
        self.speed = (0.0, 0.0)
        self.velocity = (0, 0)
        self.rotation = 0.0
        self.accelerating = False
        self.steering_left = False
        self.steering_right = False

    def render(self, screen):
        points = list(self.transform_polygon(self.SHIP_SHAPE).coords)
        pygame.draw.lines(screen, (255, 255, 255), True, points)
        points = list(self.transform_polygon(self.THRUSTER_SHAPE).coords)
        if self.accelerating:
            pygame.draw.lines(screen, (255, 255, 255), False, points)

    def logic(self, delta):
        if self.accelerating:
            a = delta * self.ACCELERATION
            v = (math.sin(self.rotation / 180 * math.pi) * a, -math.cos(self.rotation / 180 * math.pi) * a)
            self.speed = numpy.add(self.speed, v)

            speed = math.sqrt(self.speed[0]**2 + self.speed[1]**2)
            if speed > self.MAX_SPEED:
                self.speed = numpy.divide(self.speed, speed / self.MAX_SPEED)

        if self.steering_right:
            self.rotation += self.ROTATION_SPEED * delta
        if self.steering_left:
            self.rotation -= self.ROTATION_SPEED * delta
        self.rotation %= 360

        self.wrap_position()

    def accelerate(self, value):
        self.accelerating = value

    def steer_left(self, value):
        self.steering_left = value

    def steer_right(self, value):
        self.steering_right = value

    def shootBullet(self):
        points = list(self.transform_polygon(self.SHIP_SHAPE).coords)[0]
        return Bullet(self.area, points, self.rotation)
