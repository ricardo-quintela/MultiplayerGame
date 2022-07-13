from math import sin, cos, radians, atan2

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

        # joint
        self.isBound = False
        self.joint = None



    def calculate_b(self) -> Vector2:
        """Calculates the B point of the bone based on the length and the angle

        Returns:
            Vector2: the cartesian coordinates of point b
        """

        self.b.update(self.a + Vector2(self.length * cos(radians(self.angle)), self.length * sin(radians(self.angle))))


    def set_pos(self, pos: tuple):
        """Sets a new position for the bone\n
        It will mantain it's previous length and angle

        Args:
            pos (tuple): the new position to assign to the bone
        """

        self.a.update(pos)


    def bind(self, target):
        """Bind this bone to a joint\n\n

        The target point must be a mutable object

        Args:
            target (list, Vector2): the point to bind the joint to
        """
        self.isBound = True

        self.joint = target


    def follow(self, target: tuple):
        """Makes the bone align and follow a given target

        Args:
            target (tuple): the position of the target
        """
        
        # create a vector 2 to ease calculations

        # calculate the direction of the vector
        direction = target - self.a

        # calculate the angle based on the direction
        self.angle = point_O.angle_to(direction)

        # set the magnitude of the direction vector to the length of this vector and invert it
        if direction.length() > 0:
            direction.scale_to_length(self.length)
            direction *= -1

        # set A to the coordinates of the target - length
        self.a.update(target + direction)
        



    def update(self):
        """Updates the bone position
        """

        self.calculate_b()

        # follow its bound joint
        if self.isBound:
            self.follow(self.joint)


    def blit(self, canvas: Surface):
        """Draw the bone on the given Surface

        Args:
            canvas (Surface): the Surface where to draw the bone
        """

        line(canvas, "black", self.a, self.b, 3)
