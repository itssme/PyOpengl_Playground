from OpenGL.GL import *
from OpenGL.GLU import *

from math import sin, cos, sqrt, radians


class GameObject:
    colors = {
        # "NOTHING": (0, 0, 0),
        "WHITE": (1, 1, 1),
        "RED": (1, 0, 0),
        "GREEN": (0, 1, 0),
        "BLUE": (0, 0, 1),
        "LIGHT_BLUE": (0, 1, 1)
    }

    def __init__(self, color):
        self.vertices = []
        self.edges = []
        self.speed = 0
        self.heading = 0
        self.__last_heading = 0
        self.color = color
        self.size = 0
        self.dead = False

    def tick(self):
        alpha = self.heading
        beta = 90
        gamma = 180 - alpha - beta

        b = self.speed

        a = sin(radians(alpha)) * b / sin(radians(beta))
        c = sin(radians(gamma)) * b / sin(radians(beta))

        self.translate(a, c)
        self.rotate()
        return self.check_off_screen()

    def translate(self, x, y):
        for i in xrange(0, len(self.vertices)):
            if x != 0: self.vertices[i][0] = self.vertices[i][0] + x
            if y != 0: self.vertices[i][1] = self.vertices[i][1] + y

    def draw(self):
        #glBegin(GL_LINES)

        if self.color is not None:
            glColor3fv(self.colors[self.color])

        for edge in self.edges:
            for vertex in edge:
                glVertex2fv(self.vertices[vertex])

        #glEnd()

    def rotate(self):
        angle = radians(self.__last_heading - self.heading)
        self.__last_heading = self.heading
        cx, cy = self.vertices[-1][0], self.vertices[-1][1]

        for i in xrange(0, len(self.vertices)):
            px, py = self.vertices[i][0],  self.vertices[i][1]

            s = sin(angle)
            c = cos(angle)

            px -= cx
            py -= cy

            # rotate point
            xnew = px * c - py * s
            ynew = px * s + py * c

            px = xnew + cx
            py = ynew + cy

            self.vertices[i][0], self.vertices[i][1] = px, py

    def calculate_size(self):
        max_point = max(self.vertices)
        min_point = min(self.vertices)

        self.size = sqrt((min_point[0] - max_point[0]) ** 2 + (min_point[1] - max_point[1]) ** 2)

    def check_off_screen(self):
        x_out = True
        y_out = True

        for vertex in self.vertices:
            if -1 < vertex[0] < 1:
                x_out = False
            if -1 < vertex[1] < 1:
                y_out = False

        if x_out:
            if self.vertices[0][0] < -1:
                self.translate(2 + self.size*1.1, 0)
            else:
                self.translate(-2 - self.size*1.1, 0)

        if y_out:
            if self.vertices[0][1] < -1:
                self.translate(0, 2 + self.size*1.1)
            else:
                self.translate(0, -2 - self.size*1.1)

        if x_out or y_out:
            return True
        else:
            return False
