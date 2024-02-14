from pygame import Vector2

from .weapon import Weapon
from .hitbox import Hitbox

class Sword(Weapon):
    def __init__(self) -> None:
        super().__init__((0,0), 30, 278)

        self.hitbox = Hitbox(
            (0,0),
            (0,5),
            (50,2.5)
        )
        self.hitbox.set_pos(self.follow_line[0])

        self.attack_animations = [
            "sword_attack"
        ]

        self.stun_durations = [
            5
        ]

        self.knockback_velocities = [
            Vector2(10,-10)
        ]

        self.valid_frames = [
            [5,6]
        ]
