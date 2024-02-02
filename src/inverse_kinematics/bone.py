from math import sin, cos, radians
from typing import Sequence

from pygame import Vector2
from pygame import Surface
from pygame.draw import line

from .exceptions import PointNotFoundException

from config import DEBUG

class Bone:
    def __init__(self, x: int, y: int, length: float, angle: float, name: str = "") -> None:
        """Constructor of the class Bone

        Args:
            x (int): the x coord of the bone
            y (int): the y coord of the bone
            length (float): the length of the bone
            angle (float): the angle of the bone (degrees)
            name (str): the name of the bone
        """

        self.a = Vector2(x, y)

        self.length = length
        self.angle = angle

        self.name = name

        # calculate b
        self.b = Vector2(0, 0)

        self.calculate_b()

        # joint
        self.is_anchored = False
        self.anchor = None

        self.attachment = self.b
        self.other = self.a

        self.attachment_is_b = 1



    def calculate_b(self):
        """Calculates the B point of the bone based on the length and the angle
        """

        self.b.update(
            self.a + Vector2(self.length * cos(radians(self.angle)), self.length * sin(radians(self.angle)))
        )

    def calculate_other(self):
        """Calculates the B point of the bone based on the length and the angle
        """

        self.other.update(
            self.attachment + Vector2(self.length * cos(radians(self.angle + 180 * self.attachment_is_b)), self.length * sin(radians(self.angle + 180 * self.attachment_is_b)))
        )


    def set_pos(self, pos: tuple):
        """Sets a new position for the bone\n
        It will mantain it's previous length and angle

        Args:
            pos (tuple): the new position to assign to the bone
        """

        self.a.update(pos)


    def fixate(self, target: Vector2, attachment_point_name: str):
        """Anchor this bone to a point\n\n

        The target point must be a mutable object

        Args:
            target (list, Vector2): the point to anchor the joint to
        """
        self.is_anchored = True

        self.anchor = target

        if attachment_point_name == "a":
            self.attachment = self.a
            self.other = self.b
            self.attachment_is_b = 0

        elif attachment_point_name == "b":
            self.attachment = self.b
            self.other = self.a
            self.attachment_is_b = 1

        else:
            return PointNotFoundException(f"No such point '{attachment_point_name}' on bone")


    def follow(self, target: Sequence[float], _):
        """Moves point a to the target and re-calculates b to
        match the bone length

        Args:
            target (Vector2): the target to follow
        """

        self.angle += (self.other - self.attachment).angle_to(target - self.attachment)

        self.calculate_other()



    def set_rotation(self, angle: int):
        """Set the rotation of the bone

        Args:
            angle (int): the angle of the bone
        """
        self.angle = angle


    def update(self):
        """Updates the bone position
        """

        if self.is_anchored:
            self.a.update(self.anchor)

        self.calculate_b()


    def blit(self, canvas: Surface):
        """Draw the bone on the given Surface

        Args:
            canvas (Surface): the Surface where to draw the bone
        """

        line(canvas, DEBUG["skeleton_bone_color"], self.a, self.b, 3)
