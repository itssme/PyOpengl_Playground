import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from cube import Cube

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


def main():
    pygame.init()

    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 500.0)

    glTranslatef(0.0, 0.0, -10)
    glRotatef(20, 20, 45, 0)

    cube = Cube()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            check_pressed(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    glTranslate(0, 0, 0.1)
                elif event.button == 5:
                    glTranslate(0, 0, -0.1)

        if keys["K_LEFT"]:
            glTranslatef(-0.1, 0, 0)
        elif keys["K_RIGHT"]:
            glTranslate(0.1, 0, 0)
        elif keys["K_UP"]:
            glTranslate(0, 0.1, 0)
        elif keys["K_DOWN"]:
            glTranslate(0, -0.1, 0)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        cube.draw()
        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == '__main__':
    main()
