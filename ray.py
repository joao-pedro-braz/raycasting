from utils import Point2D
from obstacle import Obstacle
from pygame.draw import line
from wall import Wall


class Ray():
    """
    I'm a single "ray of light".
    I have source (i.e.: my position) and
    a direction (i.e.: where I'm headed to).

    My responsabilities are:
        - Check for collisions against obstacles
        - Draw myself in the drawing canvas
    """
    NOT_COLLIDED_COLOR = (255, 255, 255)
    COLLIDED_COLOR = (255, 0, 0)

    def __init__(self, source, direction: Point2D):
        self.source = source
        self.direction = direction
        self.direction.normalize()

    def intersectLines(self, pt2, obstacle):
        x4 = self.source.position.x + pt2.x
        y4 = self.source.position.y + pt2.y

        den = obstacle.diff.x * (-pt2.y) - obstacle.diff.y * (-pt2.x)
        if den == 0:
            return False, None

        t = ((obstacle.starting_edge.x - self.source.position.x) * (self.source.position.y - y4) -
             (obstacle.starting_edge.y - self.source.position.y) * (self.source.position.x - x4)) / den
        u = -((obstacle.diff.x) * (obstacle.starting_edge.y - self.source.position.y) -
              (obstacle.diff.y) * (obstacle.starting_edge.x - self.source.position.x)) / den
        if (t > 0 and t < 1 and u > 0):
            return True, Point2D(obstacle.starting_edge.x + t *
                                 obstacle.opposite_diff.x,
                                 obstacle.starting_edge.y + t *
                                 obstacle.opposite_diff.y)
        else:
            return False, None

    def check_for_collision(self, obstacle: Obstacle):
        intersect, position = self.intersectLines(
            self.direction, obstacle)

        return intersect, position

    def draw(self, canvas, obstacles):
        collisions = []
        collided = False
        neareset_dist = None
        for obstacle in obstacles:
            _collided, end_position = self.check_for_collision(
                obstacle)
            if _collided:
                collisions.append((end_position, obstacle))
                collided = True
        if collided:
            neareset = None
            obstacle = None
            for collision, _obstacle in collisions:
                if (neareset is None or self.source.position.euclidian_distance(collision) < self.source.position.euclidian_distance(
                        neareset)):
                    neareset = collision
                    obstacle = _obstacle
            line(canvas, self.NOT_COLLIDED_COLOR,
                 self.source.position.to_tuple(), neareset.to_tuple())

            return self.source.position.euclidian_distance(
                        neareset), neareset, obstacle
            # if isinstance(obstacle, Wall):
            #     line(canvas, self.NOT_COLLIDED_COLOR,
            #          self.source.position.to_tuple(), neareset.to_tuple())
            # else:
            #     line(canvas, self.COLLIDED_COLOR,
            #          self.source.position.to_tuple(), neareset.to_tuple())
