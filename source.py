from utils import Point2D
from ray import Ray
from math import cos, sin, radians
from pygame.draw import circle


class Source():
    """
    I'm a source of "light rays".
    I have a starting point and
    a list of rays.

    My responsabilities are:
        - Generate my rays
        - Draw my rays
        - Move around
    """
    COLOR = (255, 20, 20)

    def __init__(self, position: Point2D):
        self.position = position
        self.rays = []

    def preview(self, canvas, mouse_position: Point2D):
        circle(canvas, self.COLOR, mouse_position.to_tuple(), 5)

    def generate_rays(self, precision):
        for i in range(0, int(360 * precision)):
            self.rays.append(
                Ray(self, Point2D(cos(radians(i / precision)), sin(radians(i / precision)))))

    def move(self, new_position: Point2D):
        self.position = new_position

    def draw(self, canvas, obstacles):
        dist = []
        for ray in self.rays:
            distance = ray.draw(canvas, obstacles)
            if distance is not None:
                dist.append(distance)
        circle(canvas, self.COLOR, self.position.to_tuple(), 5)

        return dist

