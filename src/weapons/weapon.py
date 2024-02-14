from typing import Union, Tuple, List
from math import cos, sin, radians

from pygame import Vector2, Surface
from pygame.draw import line

from inverse_kinematics import Bone
from config import DEBUG

from .hitbox import Hitbox


class Weapon:
    def __init__(self, start_pos: Union[Vector2, Tuple[int, int]], length: int, angle: float = 0) -> None:
        self.angle = angle
        self.length = length
        self.follow_line = [
            Vector2(start_pos),
            Vector2(0,0)
        ]

        self.attack_animations: List[str] = list()

        self.attachment: Bone = None
        self._calculate_b(self.follow_line, self.angle, 1)

        self.hitbox: Hitbox = None



    def _calculate_b(self, _line: List[Vector2], angle: float, direction: int):
        """Calculates the b point based on the rotation angle
        and the length of the weapon
        """
        if self.attachment is None:
            return

        angle = direction * angle + self.attachment.angle
        _line[1] = _line[0] + self.length * Vector2(
            cos(radians(angle)),
            sin(radians(angle)),
        )


    def attach(self, bone: Bone):
        """Attaches the weapon to a bone in a skeleton

        Args:
            bone (Bone): the skeleton's bone
        """
        self.attachment = bone
        self.follow_line[0] = bone.b


    def update(self, direction: int):
        """Updates the weapon's hitbox
        """
        self._calculate_b(self.follow_line, self.angle, direction)

        if self.hitbox is None:
            return

        self.hitbox.set_pos(self.follow_line[1])

        angle = direction * self.angle + self.attachment.angle
        self.hitbox.set_rotation(angle)



    def show_hitbox(self, canvas: Surface):
        """Shows the weapon's bounding box as a line

        Args:
            canvas (Surface): the surface where to draw the bounding box
        """
        line(canvas, DEBUG["weapon_hbox_color"], self.follow_line[0], self.follow_line[1])

        if self.hitbox is None:
            return

        self.hitbox.blit(canvas)
