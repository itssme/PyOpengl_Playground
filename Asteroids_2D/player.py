from game_object import GameObject
from bullet import Bullet


class Player(GameObject):

    def __init__(self, color="WHITE"):
        GameObject.__init__(self, color)
        self.speed = 0
        self.heading = 0
        self.heading_step = 5

        self.edges = [
            [0, 1],
            [1, 2],
            [2, 3],
            [3, 0]
        ]

        self.vertices = [
            [0, 0.05],
            [0.02, 0],
            [0, 0.02],
            [-0.02, 0],
            [0, 0.02]  # middle point
        ]

        self.calculate_size()

        self.__last_heading = 0

    def turn_right(self):
        self.heading = (self.heading + self.heading_step) % 360

    def turn_left(self):
        self.heading = (self.heading - self.heading_step) % 360

    def shoot(self):
        bullet = Bullet(0.025, self.heading)
        bullet.translate(self.vertices[0][0], self.vertices[0][1])
        return bullet
