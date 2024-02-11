from typing import List, Tuple
from math import cos, sin, radians

from pygame.draw import line
from pygame import Vector2, Surface
from numpy import array, matmul

from utils import BoundingBox


class Hitbox:
    def __init__(self, *points: Tuple[float, float]) -> None:
        lines: List[List[Vector2]] = list()

        for i in range(-1, len(points) - 1):
            lines.append([Vector2(points[i]), Vector2(points[i + 1])])

        self.center = Vector2(0, 0)
        for _line in lines:
            self.center += _line[0]
        self.center /= len(lines)

        self.angle: float = 0

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

    def set_rotation(self, angle: float):
        """Sets the rotation of the hitbox to a new value

        Args:
            angle (float): the new angle
        """
        self.angle = angle

    def rotate(self, point: Vector2) -> Vector2:
        """Rotates a given point of the hitbox

        Args:
            point (Vector2): the point to rotate

        Returns:
            Vector2: the rotated point
        """
        angle = self.angle
        rotation_matrix = array(
            (
                (cos(radians(angle)), -sin(radians(angle))),
                (sin(radians(angle)), cos(radians(angle))),
            )
        )

        new_point = matmul(rotation_matrix, point - self.center)

        return self.center + Vector2(new_point[0], new_point[1])

    def colliderect(self, bbox: BoundingBox) -> bool:
        """Returns true if the hitbox collides with a given BoundingBox

        Args:
            bbox (BoundingBox): the bounding box to check collisions with

        Returns:
            bool: True if it collided, False otherwise
        """
        for vector in self.relative_vectors:
            if bbox.collideline(
                (
                    self.rotate(self.center - vector[0]),
                    self.rotate(self.center - vector[1]),
                )
            ):
                return True

    def blit(self, canvas: Surface):
        """Draws the hitbox on the given surface

        Args:
            canvas (Surface): the surface to draw the hibox on
        """
        for vector in self.relative_vectors:
            line(
                canvas,
                "red",
                self.rotate(self.center - vector[0]),
                self.rotate(self.center - vector[1]),
            )

    def __repr__(self) -> str:
        string = "Hitbox("
        for i, vector in enumerate(self.relative_vectors):
            string += str(self.center - vector[0])
            if i < len(self.relative_vectors) - 1:
                string += ", "
        return string + ")"
