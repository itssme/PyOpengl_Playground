from OpenGL.GL import *
from OpenGL.GLU import *


class Cube:
    edges = (
        (0, 1),
        (0, 3),
        (0, 4),
        (2, 1),
        (2, 3),
        (2, 7),
        (6, 3),
        (6, 4),
        (6, 7),
        (5, 1),
        (5, 4),
        (5, 7)
    )

    def __init__(self, x=0, y=0, z=0, size=1):
        self.vertices = (
            (size + x, -size - y, -size - z),
            (size + x, size + y, -size - z),
            (-size - x, size + y, -size - z),
            (-size - x, -size - y, -size - z),
            (size + x, -size - y, size + z),
            (size + x, size + y, size + z),
            (-size - x, -size - y, size + z),
            (-size - x, size + y, size + z)
        )

    def draw(self):
        glBegin(GL_LINES)

        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.vertices[vertex])

        glEnd()
