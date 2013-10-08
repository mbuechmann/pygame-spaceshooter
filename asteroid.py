import numpy
import pygame
import random
import math
from shapely.geometry import LineString
from game_object import GameObject


class Asteroid(GameObject):
    SPEED = 100
    MAX_ROTATION_SPEED = 260
    BIG_SHAPES = [
        LineString([
            (-18, 0), (-15, 10), (-3, 12), (0, 20), (7, 16), (15, 14), (20, 0), (18, -3), (15, -10), (8, -12), (0, -15),
            (-2, -12), (-12, -10)
        ])
    ]
    MEDIUM_SHAPES = [
        LineString([
            (-9, 0), (-15, 5), (-13, 9), (-5, 15), (0, 11), (5, 14), (10, 10), (15, -2), (5, -15), (-12, -14), (-15, -5)
        ]),
        LineString([
            (-14, 5), (-6, 14), (-1, 10), (1, 13), (5, 10), (10, 10), (14, -3), (7, -8), (0, -11), (-4, -13),
            (-12, -12), (-10, -3)
        ])
    ]
    SMALL_SHAPES = [
        LineString([
            (-10, 0), (-5, 1), (-3, 8), (5, 8), (8, -2), (1, -10), (-6, -9)
        ]),
        LineString([
            (-10, 8), (-7, 10), (5, 5), (9, 1), (3, -8), (-5, -5), (-7, 4)
        ]),
        LineString([
            (-6, 0), (-8, 4), (-3, 8), (0, 5), (4, 6), (6, 2), (4, -1), (2, -8), (-5, -7)
        ])
    ]
    SHAPES = [
        SMALL_SHAPES, MEDIUM_SHAPES, BIG_SHAPES
    ]

    def __init__(self, area, size=3, position=None):
        super(Asteroid, self).__init__(area)
        self.size = size
        self.area = area
        if position is None:
            self.position = self.random_position(area)
        else:
            self.position = position
        shapes = self.SHAPES[self.size - 1]
        elem = random.randrange(len(shapes))
        self.polygon = shapes[elem]
        self.rotation = random.random() * 360
        self.rotation_speed = random.random() * self.MAX_ROTATION_SPEED - self.MAX_ROTATION_SPEED
        angle = random.random() * 2 * math.pi
        self.speed = (math.cos(angle) * self.SPEED, math.sin(angle) * self.SPEED)

    def render(self, screen):
        points = list(self.transform_polygon(self.polygon)  .coords)
        pygame.draw.lines(screen, (255, 255, 255), True, points)

    def logic(self, delta):
        self.rotation = (self.rotation + self.rotation_speed * delta) % 360
        self.position = numpy.add(self.position, numpy.multiply(self.speed, delta))
        self.move(delta)

    def random_position(self, area):
        x = area[0] / 2
        y = area[1] / 2
        while area[0] / 3 < x < (area[0] / 3) * 2 and area[1] / 3 < y < (area[1] / 3) * 2:
            x = random.random() * area[0]
            y = random.random() * area[1]
        return x, y

    def spawn_children(self):
        if self.size > 1:
            return [
                Asteroid(self.area, self.size - 1, self.position), Asteroid(self.area, self.size - 1, self.position)
            ]
        else:
            return []

    def collides_with_bullet(self, bullet):
        bullet_path = LineString((bullet.last_position, bullet.position))
        return self.transform_polygon(self.polygon).intersects(bullet_path)
