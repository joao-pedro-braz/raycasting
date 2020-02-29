from obstacle import Obstacle
from pygame import color

class Wall(Obstacle):
    COLOR = color.Color(200, 200, 200)

    def __init__(self, starting_edge, ending_edge):
        super().__init__(starting_edge, ending_edge)
