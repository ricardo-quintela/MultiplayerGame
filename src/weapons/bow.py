from typing import List

from pygame import Surface, Vector2
from pygame.draw import line
from config import DEBUG

from inverse_kinematics.bone import Bone

from .weapon import Weapon

class Bow(Weapon):
    def __init__(self) -> None:
        super().__init__((0,0), 30, 113)

        self.follow_line: List[List[Vector2]] = [
            [Vector2(0,0), Vector2(0,0)],
            [Vector2(0,0), Vector2(0,0)],
        ]
        self._calculate_b(self.follow_line[0], self.angle, 1)
        self._calculate_b(self.follow_line[1], (360 - self.angle), 1)

        self.attack_animations = [
            "bow_attack"
        ]

    def attach(self, bone: Bone):
        self.attachment = bone
        self.follow_line[0][0] = bone.b
        self.follow_line[1][0] = bone.b


    def update(self, direction: int):
        self._calculate_b(self.follow_line[0], self.angle, direction)
        self._calculate_b(self.follow_line[1], (360 - self.angle), direction)


    def show_hitbox(self, canvas: Surface):
        line(canvas, DEBUG["weapon_hbox_color"], self.follow_line[0][0], self.follow_line[0][1])
        line(canvas, DEBUG["weapon_hbox_color"], self.follow_line[1][0], self.follow_line[1][1])
