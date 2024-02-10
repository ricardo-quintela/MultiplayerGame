from typing import List, Tuple
from math import cos, sin, radians

from pygame.draw import line
from pygame import Vector2, Surface
from numpy import array, matmul


class Hitbox:
    def __init__(self, *points: Tuple[float, float]) -> None:
        lines: List[List[Vector2]] = list()

        for i in range(-1, len(points) - 1):
            lines.append([Vector2(points[i]), Vector2(points[i+1])])

        self.center = Vector2(0,0)
        for _line in lines:
            self.center += _line[0]
        self.center /= len(lines)

        self.angle: float = 0
        self.direction = 1

        self.relative_vectors = [
            [self.center - _line[0], self.center - _line[1]] for _line in lines
        ]

    def set_pos(self, pos: Vector2, direction: int):
        """Sets the hitbox's center to a new position

        Args:
            pos (Vector2): the new position
            direction (float): the direction that the hitbox must be rotating
        """
        self.center.update(pos)
        self.direction = direction


    def set_rotation(self, angle: float):
        self.angle = angle


    def rotate(self, point: Vector2) -> Vector2:
        angle = self.direction * self.angle
        rotation_matrix = array(
            (
                (cos(radians(angle)), -sin(radians(angle))),
                (sin(radians(angle)), cos(radians(angle)))
            )
        )

        new_point = matmul(rotation_matrix, point - self.center)

        return self.center + Vector2(new_point[0], new_point[1])


    def blit(self, canvas: Surface):
        """Draws the hitbox on the given surface

        Args:
            canvas (Surface): the surface to draw the hibox on
        """
        for vector in self.relative_vectors:
            line(canvas, "red", self.rotate(self.center - vector[0]), self.rotate(self.center - vector[1]))
