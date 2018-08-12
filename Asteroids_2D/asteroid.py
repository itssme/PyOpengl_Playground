from random import randrange
from math import sin, radians

from game_object import GameObject


class Asteroid(GameObject):
    def __init__(self, corners, color="WHITE", size_divider=175.0):
        GameObject.__init__(self, color)

        self.size_divider = size_divider
        self.generate_asteroid(corners)

        self.speed = randrange(10, 100) / 10000.0
        self.heading = randrange(0, 360)
        self.__last_heading = self.heading
        self.rotate()
        self.calculate_size()

    def generate_asteroid(self, corners):
        degree_range = 360 / corners
        size = randrange(25, 30)

        for i in xrange(corners):
            self.edges.append([i, i + 1])

            alpha = randrange(i * degree_range + degree_range / 4, (i + 1) * degree_range - degree_range / 4)
            beta = 90
            gamma = 180 - alpha - beta

            b = randrange(size-10, size+10) / 175.0

            a = sin(radians(alpha)) * b / sin(radians(beta))
            c = sin(radians(gamma)) * b / sin(radians(beta))

            self.vertices.append([c, a, 0])

            """
            print self.vertices
            print "a: " + str(a)
            print "b: " + str(b)
            print "c: " + str(c)
            print "alpha: " + str(alpha)
            print "beta:  " + str(beta)
            print "gamma: " + str(gamma)
            
            sinussatz
            # formel: a=sin(alpha)*(b/sin(beta))
            # formel: gamma = 180 - (alpha+beta)
            # formel: c=sin(gamma)*(a/sin(alpha))
            """

        self.edges[-1][1] = 0

        # this is the middle point, it has NO purpose for opengl and is only used in game_object.rotate and in translate
        self.vertices.append([0, 0, 0])

    def collided(self):
        self.speed = abs(self.speed) if self.speed < 0 else -self.speed
        self.speed *= 2
        self.tick()
        self.speed = self.speed / 2

