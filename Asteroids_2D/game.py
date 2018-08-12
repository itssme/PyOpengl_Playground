from player import Player
from asteroid import Asteroid

from random import randrange
from time import time, sleep
from threading import Thread


def inside_polygon(x, y, vertices):
    """
    Return True if a coordinate (x, y) is inside a polygon defined by
    a list of vertices [(x1, y1, z1), (x2, x2, z2), ... , (xN, yN, zN)].
    """

    n = len(vertices)
    inside = False
    p1x, p1y, ignore_z = vertices[0]

    for i in range(1, n + 1):
        p2x, p2y, ignore_z = vertices[i % n]

        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):

                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside

        p1x, p1y = p2x, p2y
    return inside


def inside_polygon_vertices(vertices1, vertices2):
    intersects = False

    for j in xrange(0, len(vertices1)):
        x = vertices1[j][0]
        y = vertices1[j][1]

        intersects = inside_polygon(x, y, vertices2)
        if intersects:
            break

    return intersects


class Game:

    def __init__(self):
        self.player = Player()
        self.asteroids = []
        self.bullets = []
        self.level = 0
        self.create_asteroids()
        self.__collision_counter = 0

        self.collision_thread = Thread(target=self.collision_loop)
        self.collision_thread.start()

    def collision_loop(self):

        while not self.player.dead:
            start = time()

            try:
                self.check_collision_bullets()
                self.check_collision_player()
                self.check_collision_asteroids()
                try:
                    sleep(0.005 - (time() - start))
                except IOError:
                    pass  # skip sleep

            except IndexError:
                pass

    def create_asteroids(self):
        for i in xrange(self.level + 5):
            in_asteroid = True
            self.asteroids.append(Asteroid(7))
            while in_asteroid:

                x_pos = 0.0
                y_pos = 0.0

                while -0.1 < x_pos < 0.1:
                    x_pos = randrange(-100, 100)/100.0

                while -0.1 < y_pos < 0.1:
                    y_pos = randrange(-100, 100)/100.0

                self.asteroids[i].translate(x_pos, y_pos)
                in_asteroid = self.check_collision_asteroids()
                # TODO: check if this translation caused a collision and then translate the asteroid again randomly

    def tick_all_objects(self):
        self.tick_asteroids()
        self.tick_player()
        self.tick_bullets()

        if len(self.asteroids) == 0:
            self.create_asteroids()
            self.level += 1
            self.player = Player()

    def tick_asteroids(self):
        new_asteroids = []

        for i in xrange(0, len(self.asteroids)):
            if not self.asteroids[i].dead:
                new_asteroids.append(self.asteroids[i])
                self.asteroids[i].tick()

        self.asteroids = new_asteroids

    def tick_player(self):
        self.player.tick()

    def tick_bullets(self):
        new_bullets = []
        for i in xrange(0, len(self.bullets)):
            if not self.bullets[i].tick() and not self.bullets[i].dead:
                new_bullets.append(self.bullets[i])

        self.bullets = new_bullets

    def draw(self):
        # TODO: make this with GLlist stuff

        for i in xrange(0, len(self.asteroids)):
            self.asteroids[i].draw()

        for i in xrange(0, len(self.bullets)):
            self.bullets[i].draw()

        self.player.draw()

    def check_collision_asteroids(self):
        collision = False

        for i in xrange(0, len(self.asteroids)):
            for j in xrange(0, len(self.asteroids[i].vertices)):
                for z in xrange(0, len(self.asteroids)):  # TODO divide len by 2?
                    if i != z:
                        if inside_polygon(self.asteroids[i].vertices[j][0], self.asteroids[i].vertices[j][1], self.asteroids[z].vertices):
                            self.asteroids[i].collided()
                            self.asteroids[z].collided()
                            collision = True

        return collision

    def check_collision_player(self):
        for i in xrange(0, len(self.asteroids)):
                if inside_polygon_vertices(self.player.vertices, self.asteroids[i].vertices):
                    print "you died lol noob"
                    self.player.dead = True

    def check_collision_bullets(self):
        for i in xrange(0, len(self.asteroids)):
            for b in xrange(0, len(self.bullets)):
                if inside_polygon(self.bullets[b].vertices[-1][0], self.bullets[b].vertices[-1][1],
                                  self.asteroids[i].vertices):
                    self.asteroids[i].dead = True
                    self.bullets[b].dead = True

    def check_collisions(self):
        if self.__collision_counter == 5:
            self.check_collision_player()
            self.check_collision_asteroids()
            self.__collision_counter = 0
        else:
            self.__collision_counter += 1
