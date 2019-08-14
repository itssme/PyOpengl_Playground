from game_object import GameObject


class Bullet(GameObject):

    def __init__(self, speed, heading, color="WHITE"):
        GameObject.__init__(self, color)
        self.speed = speed
        self.heading = heading
        self.__last_heading = heading

        self.edges = [
            [0, 1],
            [1, 2],
            [2, 3],
            [3, 0]
        ]

        self.vertices = [
            [0, 0.01],
            [0.01, 0],
            [0, -0.01],
            [-0.01, 0],
            [0, 0]
        ]

        self.calculate_size()
        self.rotate()

    def check_off_screen(self):
        x_out = True
        y_out = True

        for vertex in self.vertices:
            if -1 < vertex[0] < 1:
                x_out = False
            if -1 < vertex[1] < 1:
                y_out = False

        if x_out or y_out:
            return True
        else:
            return False
