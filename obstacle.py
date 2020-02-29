from utils import Point2D
from pygame.draw import line
from pygame import color


class Obstacle():
    """
    I'm a obstacle for "light rays".
    I have two edges (start and end),
    that are my boundaries.

    My responsabilities are:
        - Draw myself in the drawing canvas
        - Act as a boudary for light rays
    """
    COLOR = color.Color(0, 50, 255)

    def __init__(self, starting_edge: Point2D, ending_edge: Point2D):
        self.starting_edge = starting_edge
        self.ending_edge = ending_edge
        self.diff = self.starting_edge - self.ending_edge
        self.opposite_diff = self.diff * -1

    @staticmethod
    def preview(canvas, starting_edge: Point2D, ending_edge: Point2D):
        line(canvas, Obstacle.COLOR, starting_edge.to_tuple(),
             ending_edge.to_tuple(), 5)

    def draw(self, canvas):
        line(canvas, self.COLOR, self.starting_edge.to_tuple(),
             self.ending_edge.to_tuple(), 5)
