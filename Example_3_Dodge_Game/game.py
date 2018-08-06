import pygame
from pygame.locals import *

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
    glTranslatef(randrange(-50, 50)/10.0, randrange(-50, 50)/10.0, -30)

    cube = Cube(randrange(1, 100)/75.0, randrange(1, 100)/75.0)

    object_passed = False
    while not object_passed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            check_pressed(event)

        if keys["K_LEFT"]:
            glTranslatef(-0.1, 0, 0)
        if keys["K_RIGHT"]:
            glTranslate(0.1, 0, 0)
        if keys["K_UP"]:
            glTranslate(0, 0.1, 0)
        if keys["K_DOWN"]:
            glTranslate(0, -0.1, 0)

        coords = glGetDoublev(GL_MODELVIEW_MATRIX)
        #print(coords)

        camera_x = coords[3][0]
        camera_y = coords[3][1]
        camera_z = coords[3][2]

        if camera_z < 0:
            object_passed = True
            glTranslate(abs(camera_x/2) if camera_x < 0 else -camera_x/2, abs(camera_y)/2 if camera_y < 0 else -camera_y/2, 0)
        #print camera_z

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glTranslate(0, 0, speed)
        cube.draw()
        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == '__main__':
    pygame.init()

    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, display[0] / display[1], 0.1, 500.0)

    for i in range(1, 10):
        print "main"
        main(i/10.0)
    pygame.quit()
    quit()
