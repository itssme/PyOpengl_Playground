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

    colors = {
        # "NOTHING": (0, 0, 0),
        "RED": (1, 0, 0),
        "GREEN": (0, 1, 0),
        "BLUE": (0, 0, 1),
        "LIGHT_BLUE": (0, 1, 1)
    }

    def __init__(self, x=0, y=0, z=0, size=1, x_offset=0, y_offset=0, z_offset=0, color=None):
        self.color = color
        self.vertices = ()
        self.generate_cube(x, y, z, size, x_offset, y_offset, z_offset)

    def generate_cube(self, x=0, y=0, z=0, size=1, x_offset=0, y_offset=0, z_offset=0):
        self.vertices = (
            (size + x + x_offset, -size - y + y_offset, -size - z + z_offset),
            (size + x + x_offset, size + y + y_offset, -size - z + z_offset),
            (-size - x + x_offset, size + y + y_offset, -size - z + z_offset),
            (-size - x + x_offset, -size - y + y_offset, -size - z + z_offset),
            (size + x + x_offset, -size - y + y_offset, size + z + z_offset),
            (size + x + x_offset, size + y + y_offset, size + z + z_offset),
            (-size - x + x_offset, -size - y + y_offset, size + z + z_offset),
            (-size - x + x_offset, size + y + y_offset, size + z + z_offset)
        )

    def draw(self):
        glBegin(GL_LINES)

        if self.color is not None:
            glColor3fv(self.colors[self.color])

        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.vertices[vertex])

        glEnd()
