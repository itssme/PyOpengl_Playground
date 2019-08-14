from threading import Thread

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.time import Clock

from game import Game

from time import time, sleep

keys = {
    "K_LEFT": False,
    "K_RIGHT": False,
    "K_UP": False,
    "K_DOWN": False,
    "K_SPACE": False,
    "K_a": False,
    "K_d": False,
    "K_w": False,
    "K_s": False
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
        elif event.key == pygame.K_SPACE or event.key == pygame.K_LSHIFT:
            keys["K_SPACE"] = True
        elif event.key == pygame.K_a:
            keys["K_a"] = True
        elif event.key == pygame.K_d:
            keys["K_d"] = True
        elif event.key == pygame.K_w:
            keys["K_w"] = True
        elif event.key == pygame.K_s:
            keys["K_s"] = True

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT:
            keys["K_LEFT"] = False
        elif event.key == pygame.K_RIGHT:
            keys["K_RIGHT"] = False
        elif event.key == pygame.K_UP:
            keys["K_UP"] = False
        elif event.key == pygame.K_DOWN:
            keys["K_DOWN"] = False
        elif event.key == pygame.K_SPACE or event.key == pygame.K_LSHIFT:
            keys["K_SPACE"] = False
        elif event.key == pygame.K_a:
            keys["K_a"] = False
        elif event.key == pygame.K_d:
            keys["K_d"] = False
        elif event.key == pygame.K_w:
            keys["K_w"] = False
        elif event.key == pygame.K_s:
            keys["K_s"] = False


def main():
    # initialize pygame
    pygame.init()

    # https://github.com/pygame/pygame/issues/331
    # Actually this game should not use 200% of you cpu
    # however if pygame is installed via pip this happens...
    # I built pygame from github and the cpu usage went
    # to about ~20%. However for some reason the whole
    # game stated to lag and I installed it again via pip.

    display = (1200, 800)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    MAX_SPEED = 0.02

    game_manager = Game()

    last_bullet_time = time()

    clock = Clock()

    try:
        while not game_manager.player.dead:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(0)

                check_pressed(event)

            if keys["K_RIGHT"] or keys["K_d"]:
                game_manager.player.turn_right()
            if keys["K_LEFT"] or keys["K_a"]:
                game_manager.player.turn_left()
            if keys["K_UP"] or keys["K_w"]:
                new_speed = game_manager.player.speed + 0.0005 + (game_manager.player.speed * 0.01)
                if abs(new_speed) < MAX_SPEED:
                    game_manager.player.speed = new_speed
            if keys["K_DOWN"] or keys["K_s"]:
                new_speed = game_manager.player.speed - (0.0005 + (game_manager.player.speed * 0.01))
                if new_speed > -MAX_SPEED:
                    game_manager.player.speed = new_speed
            if keys["K_SPACE"]:
                if time() - last_bullet_time > 0.3:
                    game_manager.bullets.append(game_manager.player.shoot())
                    last_bullet_time = time()

            if -MAX_SPEED < game_manager.player.speed < 0:
                game_manager.player.speed -= game_manager.player.speed * 0.01
            if 0 < game_manager.player.speed < MAX_SPEED:
                game_manager.player.speed -= game_manager.player.speed * 0.01

            game_manager.tick_all_objects()

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            game_manager.draw()

            pygame.display.flip()
            clock.tick(60)

    except KeyboardInterrupt:
        game_manager.player.dead = True


if __name__ == '__main__':
    main()
