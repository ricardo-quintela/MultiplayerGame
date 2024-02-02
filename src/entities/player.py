from typing import Tuple

from pygame import Surface
from pygame.draw import circle

from utils import MovementKeys
from config import ENTITIES, ANIMATIONS, MODELS

from .skeleton_animated import SkeletonAnimated


ANIMATION_FRAME_SKIP = 1 / ANIMATIONS["animation_speed"]


class Player(SkeletonAnimated):
    def __init__(self, bounding_box_size) -> None:
        """Constructor of the class Player"""
        super().__init__(
            bounding_box_size,
            MODELS["player"],
            ANIMATIONS["animation_paths"]["player"],
            MODELS["scale"],
        )

        # animations
        self.current_animation = "idling"

        # map navigation
        self.current_room: Tuple[int, int] = (0,0)


    def move(self, movement_keys: MovementKeys):
        """Checks for movement input and gives the player
        a velocity vector based on the movement direction

        Args:
            movement_keys (dict): the movement keys that are being pressed
        """
        previous_is_moving = self.is_moving

        if movement_keys["left"]:
            super().move((-ENTITIES["acc_x"], 0))
        if movement_keys["right"]:
            super().move((ENTITIES["acc_x"], 0))

        if not (movement_keys["left"] or movement_keys["right"]):
            self.is_moving = False

        if not self.is_jumping and movement_keys["jump"]:
            super().move((0, -ENTITIES["jump_height"]))
            self.is_jumping = True

        # change the state depending on the animation
        if previous_is_moving ^ self.is_moving:
            if self.is_moving:
                self.change_animation_state("walking")
                return
            self.change_animation_state("idling")


    def blit(self, canvas: Surface):
        super().blit(canvas)

        # * DEBUG POINTS ================================
        circle(canvas, "aqua", self.model.get_bone("perna_e").b, 4)
        circle(canvas, "orange", self.model.get_bone("perna_d").b, 4)
        circle(canvas, "aqua", self.model.get_bone("braco_e").b, 4)
        circle(canvas, "orange", self.model.get_bone("braco_d").b, 4)
