from typing import Sequence, Tuple, Union
from numpy import array, float32
from numpy.linalg import det
from pygame import Vector2, Rect

Line = Sequence[Union[Vector2, Tuple[int, int]]]


def _ccw(point: Vector2, line: Line) -> bool:
    """Returns True if the given points are in counter clock wise order

    Args:
        point (Vector2): the first point
        line (Line): the remaining two points

    Returns:
        bool: True if the points are in counter clock wise order
    """
    arr = array(
        (
            (1, point[0], point[1]),
            (1, line[0][0], line[0][1]),
            (1, line[1][0], line[1][1])
        ),
        dtype=float32
    )
    return det(arr) > 0


class BoundingBox(Rect):
    """Class that inherits from pygame.Rect
        having the exact same behaviour, however
        this one implements more collision related methods
    """

    def collideline(self, line: Line) -> bool:
        """Returns True if the given line collides with the given Rect

        Args:
            line (Line): a line to check the collisions

        Returns:
            bool: True if collided, False otherwise
        """

        rect_sides = (
            (self.bottomleft, self.topleft),
            (self.bottomright, self.topright),
            (self.topleft, self.topright),
            (self.bottomleft,self.bottomright)
        )

        for rect_side in rect_sides:
            # calculating the determinants
            r_first_la = _ccw(line[0], rect_side)
            r_first_lb = _ccw(line[1], rect_side)

            l_second_ra = _ccw(rect_side[0], line)
            l_second_rb = _ccw(rect_side[1], line)

            if r_first_la != r_first_lb and l_second_ra != l_second_rb:
                return True

        return False
