from typing import List

from pygame import Surface, Vector2
from pygame.draw import line, circle


from config import ENTITIES, MODELS, ANIMATIONS, ENEMIES
from blocks import Collider
from utils import collideline

from .skeleton_animated import SkeletonAnimated
from .player import Player


class Enemy(SkeletonAnimated):
    def __init__(self, bounding_box_size: tuple) -> None:
        super().__init__(
            bounding_box_size,
            MODELS["player"],
            ANIMATIONS["animation_paths"]["player"],
            MODELS["scale"]
        )

        self.current_animation = "idling"
        self.detected_player = False

        self.detection_ray = self.model.get_bone("pescoco").a.copy() + self.direction * (100, 0)

        self.distance_from_player = 0


    def move(self):
        if abs(self.distance_from_player) < 100:
            self.is_moving = False

        elif self.detected_player:
            super().move((self.direction * ENTITIES["acc_x"], 0))



    def check_on_platform(self, platform_collider: Collider) -> bool:
        if platform_collider is None:
            return False

        friction_decay_iterations = abs(int(round(self.vel.x / platform_collider.friction, 0)))

        total_friction = 0
        for i in range(1, friction_decay_iterations + 1):
            total_friction += i * platform_collider.friction

        return platform_collider.bounding_box.collidepoint(
            self.pos + (self.direction * (self.bounding_box.width + total_friction), 1)
        )


    def update(self, colliders: List[Collider], player: Player):
        previous_is_moving = self.is_moving

        collisions = super().update(colliders)

        if self.check_on_platform(collisions["top"]):
            self.move()
        else:
            self.is_moving = False

        #! Player detection
        # check intersection between player's bounding box and the detection ray
        if not self.detected_player:

            # update detection ray to a fixed distance
            self.detection_ray.update(
                self.model.get_bone("pescoco").a +
                self.direction * Vector2(ENEMIES["player_detection_ray_size"], 0) +
                self.vel
            )

            self.detected_player = collideline(
                (self.model.get_bone("pescoco").a, self.detection_ray),
                player.bounding_box
            )

        # if the player has been detected then follow him
        else:
            self.detection_ray.update(player.bounding_box.center)

            self.distance_from_player = self.pos.x - player.pos.x
            self.direction = -1 if self.distance_from_player > 0 else 1



        # change the state depending on the animation
        if previous_is_moving ^ self.is_moving:
            if self.is_moving:
                self.change_animation_state("walking")
                return
            self.change_animation_state("idling")



    def blit(self, canvas: Surface):
        super().blit(canvas)

        line(canvas, "blue", self.model.get_bone("pescoco").a, self.detection_ray, 1)