class Point2D:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    @staticmethod
    def from_tuple(_tuple):
        return Point2D(_tuple[0], _tuple[1])

    def from_top_left_coordinate(x, y, width, height):
        return Point2D(x - width / 2, y - height / 2)

    def is_empty(self):
        return self.x is 0 or 0.0 and self.y is 0 or 0.0

    def to_tuple(self):
        return (int(self.x), int(self.y))

    def to_tuple_without_int(self):
        return (self.x, self.y)

    def to_top_left_coordinate(self, width, height):
        return self.x + width / 2, self.y + height / 2

    def euclidian_distance(self, p2):
        return ((self.x - p2.x) ** 2 + (self.y - p2.y) ** 2) ** 0.5

    def magnitude(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def normalize(self):
        magnitude = self.magnitude()
        if magnitude != 0:
            self.x /= magnitude
            self.y /= magnitude

    def normalized(self):
        magnitude = self.magnitude()
        x = self.x
        y = self.y
        if magnitude != 0:
            x /= magnitude
            y /= magnitude
        return Point2D(x, y)

    def perpendicular_clock_wise(self):
        return Point2D(self.y, -self.x)

    def perpendicular_counter_clock_wise(self):
        return Point2D(-self.y, self.x)

    def __add__(self, other):
        if isinstance(other, Point2D):
            return Point2D(self.x + other.x, self.y + other.y)
        elif type(other) is tuple:
            return Point2D(self.x + other[0], self.y + other[1])
        elif type(other) is float or int:
            return Point2D(self.x + other, self.y + other)
        else:
            raise ValueError(
                """
                The other parameter should be a instace of Point2D
                or a tuple or a int or a float
                """)

    def __sub__(self, other):
        if isinstance(other, Point2D):
            return Point2D(self.x - other.x, self.y - other.y)
        elif type(other) is tuple:
            return Point2D(self.x - other[0], self.y - other[1])
        elif type(other) is float or int:
            return Point2D(self.x - other, self.y - other)
        else:
            raise ValueError(
                """
                The other parameter should be a instace of Point2D
                or a tuple or a int or a float
                """)

    def __mul__(self, other):
        if isinstance(other, Point2D):
            return Point2D(self.x * other.x, self.y * other.y)
        elif type(other) is tuple:
            return Point2D(self.x * other[0], self.y * other[1])
        elif type(other) is float or int:
            return Point2D(self.x * other, self.y * other)
        else:
            raise ValueError(
                """
                The other parameter should be a instace of Point2D
                or a tuple or a int or a float
                """)

    def __truediv__(self, other):
        if isinstance(other, Point2D):
            return Point2D(self.x / other.x, self.y / other.y)
        elif type(other) is tuple:
            return Point2D(self.x / other[0], self.y / other[1])
        elif type(other) is float or int:
            return Point2D(self.x / other, self.y / other)
        else:
            raise ValueError(
                """
                The other parameter should be a instace of Point2D
                or a tuple or a int or a float
                """)
