from shapely.affinity import rotate, translate


class GameObject(object):

    def __init__(self, area):
        self.area = area
        self.speed = (0, 0)
        self.dead = False

    def wrap_position(self):
        self.position = (
            (self.position[0] + self.speed[0]) % self.area[0], (self.position[1] + self.speed[1]) % self.area[1]
        )

    def transform_polygon(self, geometry):
        g2 = rotate(geometry, self.rotation, (0, 0))
        g3 = translate(g2, self.position[0], self.position[1])
        return g3

    def is_dead(self):
        return self.dead
