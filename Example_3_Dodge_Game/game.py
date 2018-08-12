import pygame

from objloader import *
from pygame.locals import *
from sys import argv

from OpenGL.GL import *
from OpenGL.GLU import *

from cube import Cube
from random import randrange

keys = {
    "K_LEFT": False,
    "K_RIGHT": False,
    "K_UP": False,
    "K_DOWN": False
}


def check_pressed(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            keys["K_LEFT"] = True
        elif event.key == pygame.K_RIGHT:
            keys["K_RIGHT"] = True
        elif event.key == pygame.K_UP:
            keys["K_UP"] = True
        elif event.key == pygame.K_DOWN:
            keys["K_DOWN"] = True

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT:
            keys["K_LEFT"] = False
        elif event.key == pygame.K_RIGHT:
            keys["K_RIGHT"] = False
        elif event.key == pygame.K_UP:
            keys["K_UP"] = False
        elif event.key == pygame.K_DOWN:
            keys["K_DOWN"] = False


def main(speed):
    glTranslatef(0, 0, -30)

    cubes = []

    if "--nighmare" in argv:
        for i in range(1):
            cubes.append(OBJ("objects/cube_2.obj"))
            cubes[i].translate(5, 0, 0)
    else:
        cubes = []
        cubes_size = 150 + int(speed * 25)
        for i in range(cubes_size):
            x_rand = randrange(1, 100) / 100.0
            y_rand = randrange(1, 100) / 100.0
            z_offset = randrange(-100 - i // 2, -10 - i // 2)
            x_offset = randrange(-600, 600) / 100.0 * z_offset / 20
            y_offset = randrange(-600, 600) / 100.0 * z_offset / 20
            color = Cube.colors.keys()
            color = color[randrange(0, len(color))]
            cubes.append(Cube(x_rand, y_rand, x_offset=x_offset, y_offset=y_offset, z_offset=z_offset,
                              color=color))  # TODO random color

    coords = glGetDoublev(GL_MODELVIEW_MATRIX)
    camera_x = coords[3][0]
    camera_y = coords[3][1]
    camera_z = coords[3][2]
    print camera_z

    dead = False
    while not dead:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            check_pressed(event)

        if keys["K_LEFT"]:
            glTranslatef(speed/4, 0, 0)
        if keys["K_RIGHT"]:
            glTranslate(-speed/4, 0, 0)
        if keys["K_UP"]:
            glTranslate(0, -speed/4, 0)
        if keys["K_DOWN"]:
            glTranslate(0, speed/4, 0)

        coords = glGetDoublev(GL_MODELVIEW_MATRIX)
        #print(coords)

        camera_x = coords[3][0]
        camera_y = coords[3][1]
        camera_z = coords[3][2]

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glTranslate(0, 0, speed)
        speed *= 1.005

        new_cubes = []
        for i in range(0, len(cubes)):
            cubes[i].draw()
            if cubes[i].vertices[0][2] < -camera_z:  # delete the cubes after they pass the player
                new_cubes.append(cubes[i])

        cubes = new_cubes
        pygame.display.flip()
        #pygame.time.wait(10)

        # TODO: check for death
        if len(cubes) == 0:
            dead = True  # not the real death condition

    coords = glGetDoublev(GL_MODELVIEW_MATRIX)

    camera_x = coords[3][0]
    camera_y = coords[3][1]
    camera_z = coords[3][2]

    glTranslate(abs(camera_x) if camera_x < 0 else -camera_x,
                abs(camera_y) if camera_y < 0 else -camera_y,
                -camera_z)


if __name__ == '__main__':
    pygame.init()

    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    glLightfv(GL_LIGHT0, GL_POSITION, (-40, 200, 100, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(45, display[0] / display[1], 0.1, 200.0)

    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW)

    for i in range(1, 10):
        print "main"
        main(i/2.0)
    pygame.quit()
    quit()
