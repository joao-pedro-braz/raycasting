from source import Source
from utils import Point2D
from numpy import interp, cross
from math import cos, sin, radians, atan2, degrees, ceil
from ray import Ray
from pygame.draw import line, circle


class Player(Source):
    """
    I'm a type of source of "light rays".
    Besides the traits that a Source class has,
    I do also have a fov (field of view, in angles) and
    a direction (a vector, of type Point2D)

    My responsabilities are:
        - Generate my rays, based upon my fov and direction
        - Move around
        - Draw my rays and the scene I'm viewing
    """

    def __init__(self, position: Point2D, fov: int, direction: Point2D):
        super().__init__(position)
        self.fov = radians(fov)
        self.minus_half_fov = -self.fov / 2
        self.half_fov = self.fov / 2
        self.direction = direction
        self.calculate_angle_of_view()
        self.mini_width_height = None
        self.max_partial_height = None
        self.min_partial_height = None
        self.fov_in_degrees = degrees(self.fov)
        self.angle = atan2(self.direction.x, self.direction.y)
        self.y_offset = 0

    def generate_rays(self, precision):
        self.precision = precision
        angle = atan2(self.direction.y, self.direction.x)
        _from = angle - self.fov / 2
        to = angle + self.fov / 2
        for i in range(0, precision):
            _angle = interp(i, [0, precision], [_from, to])
            self.rays.append(Ray(self, Point2D(cos(_angle), sin(_angle))))

    def rotate(self, mouse_position: Point2D):
        self.direction = mouse_position
        self.calculate_angle_of_view()
        self.rays = []
        self.generate_rays(self.precision)

    def calculate_angle_of_view(self):
        self.angle_of_view = atan2(self.direction.x, self.direction.y)

    def draw(self, mini_canvas, canvas, obstacles, width, heigth, mini_width, mini_height):
        distances = super().draw(mini_canvas, obstacles)
        if self.mini_width_height is None:
            self.mini_width_height = (mini_width ** 2 + mini_height ** 2)
        if self.max_partial_height is None:
            self.max_partial_height = heigth * 0.8
        if self.min_partial_height is None:
            self.min_partial_height = heigth * 0
        x_pos = 0
        for distance, collision, obstacle in distances:
            if distance is not None:
                d = collision - self.position
                angle = atan2(d.x, d.y)
                diff = angle - self.angle_of_view
                distance = distance
                _heigth = heigth * self.fov_in_degrees / (distance * cos(diff))
                base_color = interp(
                    distance ** 2, [0, self.mini_width_height], [100, 20])
                obstacle.COLOR.hsva = (
                    obstacle.COLOR.hsva[0], int(obstacle.COLOR.hsva[1]), base_color, obstacle.COLOR.hsva[3])
                line(canvas, obstacle.COLOR, (x_pos, (heigth / 2 - _heigth / 2) + self.y_offset),
                     (x_pos, (heigth / 2 + _heigth / 2) + self.y_offset), ceil(width / self.precision))
                x_pos += ceil(width / self.precision)

    def between_boundaries(self, width, heigth, amount):
        return amount.x < width and amount.x > 0 and amount.y < heigth and amount.y > 0

    def walk_front(self, clock, width, heigth):
        amount = self.position + self.direction.normalized() * \
            (clock.get_time() / 10)
        if self.between_boundaries(width, heigth, amount):
            self.position = amount

    def walk_backwards(self, clock, width, heigth):
        amount = self.position - self.direction.normalized() * \
            (clock.get_time() / 10)
        if self.between_boundaries(width, heigth, amount):
            self.position = amount

    def walk_paralel_left(self, clock, width, heigth):
        amount = self.position + self.direction.perpendicular_clock_wise().normalized() * \
            (clock.get_time() / 10)
        if self.between_boundaries(width, heigth, amount):
            self.position = amount

    def walk_paralel_right(self, clock, width, heigth):
        amount = self.position - self.direction.perpendicular_clock_wise().normalized() * \
            (clock.get_time() / 10)
        if self.between_boundaries(width, heigth, amount):
            self.position = amount

    def rotate_left(self, clock, width, heigth):
        self.angle -= 0.015 * \
            (clock.get_time() / 10)
        self.rotate(
            Point2D(cos(self.angle) * width, sin(self.angle) * heigth))

    def rotate_rigth(self, clock, width, heigth):
        self.angle += 0.015 * \
            (clock.get_time() / 10)
        self.rotate(
            Point2D(cos(self.angle) * width, sin(self.angle) * heigth))

    def rotate_up(self, clock, width, heigth):
        self.y_offset -= 10 * \
            (clock.get_time() / 10)

    def rotate_down(self, clock, width, heigth):
        self.y_offset += 10 * \
            (clock.get_time() / 10)
