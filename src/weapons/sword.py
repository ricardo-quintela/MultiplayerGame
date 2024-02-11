from .weapon import Weapon
from .hitbox import Hitbox

class Sword(Weapon):
    def __init__(self) -> None:
        super().__init__((0,0), 30, 280)

        self.hitbox = Hitbox(
            (0,0),
            (0,5),
            (50,2.5)
        )
        self.hitbox.set_pos(self.follow_line[0])

        self.attack_animations = [
            "sword_attack"
        ]
