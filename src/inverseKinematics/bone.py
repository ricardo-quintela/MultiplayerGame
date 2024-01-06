from math import sin, cos, radians

from pygame import Vector2
from pygame import Surface
from pygame.draw import line

point_O = Vector2(0,0)

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



    def calculate_b(self):
        """Calculates the B point of the bone based on the length and the angle
        """

        self.b.update(
            self.a + Vector2(self.length * cos(radians(self.angle)), self.length * sin(radians(self.angle)))
        )


    def set_pos(self, pos: tuple):
        """Sets a new position for the bone\n
        It will mantain it's previous length and angle

        Args:
            pos (tuple): the new position to assign to the bone
        """

        self.a.update(pos)


    def fixate(self, target: object):
        """Anchor this bone to a point\n\n

        The target point must be a mutable object

        Args:
            target (list, Vector2): the point to anchor the joint to
        """
        self.is_anchored = True

        self.anchor = target



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

        line(canvas, "red", self.a, self.b, 3)
