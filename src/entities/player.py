import logging
from typing import List
from pygame import Surface, Vector2

from math import cos, pi

from config import ENTITIES, ANIMATIONS
from utils import load_skeleton
from utils import MovementKeys
from blocks import Block
from .entity import Entity

KEYFRAME_STEP = (ANIMATIONS["LEG_TARGET"] * 2) / ANIMATIONS["KEYFRAMES"]
COSSINE_RADIUS = 2 * ANIMATIONS["LEG_TARGET"] / pi

class Player(Entity):
    def __init__(self, hitbox_size) -> None:
        """Constructor of the class Player
        """
        super().__init__(hitbox_size, has_gravity=True)

        self.model = load_skeleton("skeleton.json")

        self.leg_l_target = Vector2(self.pos)
        self.leg_r_target = Vector2(self.pos)

        self.hip = self.model.get_limb("coxa_e").anchor

        self.current_swing_leg = 0

        self.leg_targets = [self.leg_l_target, self.leg_r_target]

        self.current_keyframe = -ANIMATIONS["KEYFRAMES"] / 2
        self.cossine_step = -self.direction * ANIMATIONS["LEG_TARGET"] / 2 * KEYFRAME_STEP

        self.leg_is_grounded = [False, False]


    def set_pos(self, pos: tuple):
        super().set_pos(pos)

        self.leg_l_target.update(pos)
        self.leg_r_target.update(pos)



    def calculate_target_pos(self, colliders: List[Block], target_leg_pos: Vector2) -> Vector2:
        """Calculates the target postion of the leg

        Args:
            colliders (list): the list of colliders in the map
            pos: (Vector2): the player's position
            direction: (int): the direction the player is facing

        Returns:
            Vector2: the target position of the leg end effector
        """
        self.leg_is_grounded[self.current_swing_leg] = False

        for block in colliders:

            if self.pos.y + ANIMATIONS["LEG_TARGET_HEIGHT"] < block.bounding_box.top:
                continue

            if block.bounding_box.collidepoint(target_leg_pos):
                self.leg_is_grounded[self.current_swing_leg] = True
                return Vector2(target_leg_pos.x, block.bounding_box.top)

        return target_leg_pos



    def move_legs(self, colliders: list):
        """Moves the legs using procedural movement calculation
        algorithms

        Args:
            colliders (list): the list of colliders in the map
        """

        if self.is_jumping:
            return

        if not self.is_moving:
            return

        self.current_keyframe += 1
        self.cossine_step += KEYFRAME_STEP * self.direction

        #! RAYCAST OF TARGET POS
        # calculate the target position
        target_leg_pos_x = self.pos.x + self.current_keyframe * KEYFRAME_STEP * self.direction
        target_leg_pos = Vector2(
            target_leg_pos_x,
            self.pos.y - cos(self.cossine_step / COSSINE_RADIUS) * COSSINE_RADIUS
        )


        if self.current_keyframe <= 0:
            final_target_leg_pos = target_leg_pos
        else:
            final_target_leg_pos = self.calculate_target_pos(colliders, target_leg_pos)

        self.leg_targets[self.current_swing_leg].update(final_target_leg_pos)


        if self.leg_is_grounded[self.current_swing_leg] or self.current_keyframe == ANIMATIONS["KEYFRAMES"] / 2:
            self.current_swing_leg = (self.current_swing_leg + 1) % 2
            self.current_keyframe = -ANIMATIONS["KEYFRAMES"] / 2
            self.cossine_step = -self.direction * ANIMATIONS["LEG_TARGET"] / 2 * KEYFRAME_STEP


        logging.debug(
            "CURRENT_KEYFRAME: %s | CURRENT_LEG: %s | FINAL_TARGET_LEG_POS: %s | COSSINE: %s",
            self.current_keyframe,
            self.current_swing_leg,
            final_target_leg_pos,
            cos(target_leg_pos_x / COSSINE_RADIUS) * COSSINE_RADIUS
        )



    def move(self, movement_keys: MovementKeys):
        """Checks for movement input and gives the player
        a velocity vector based on the movement direction

        Args:
            movement_keys (dict): the movement keys that are being pressed
        """
        if movement_keys["left"]:
            super().move((-5,0))
        if movement_keys["right"]:
            super().move((5,0))

        if not (movement_keys["left"] or movement_keys["right"]):
            self.is_moving = False

        if not self.is_jumping and movement_keys["jump"]:
            super().move((0,-ENTITIES["JUMP_HEIGHT"]))
            self.is_jumping = True

    def update(self, colliders: List[Block]):
        """Makes the necessary computations to update the physics of the player
        """
        self.is_climbing = False
        self.leg_is_grounded[self.current_swing_leg] = False

        vector = self.model.origin - self.model.get_bone("tronco").a

        #? LEG ANIMATION
        self.move_legs(colliders)

        # calculate position based on velocity
        super().update()


        #? hitbox y lifting based on y of leg
        if self.is_moving and self.leg_is_grounded[(self.current_swing_leg + 1) % 2] and self.leg_targets[(self.current_swing_leg + 1) % 2].y < self.pos.y:
            logging.debug("(IS_CLIMBING) NEW_Y: %s", self.bounding_box.bottom)
            self.is_climbing = True
            self.vel.y -= ANIMATIONS["LEG_CLIMBING_ACC"]

        #? COLLISIONS
        self.check_collisions(colliders)



        #? updates the player model bones

        # move the origin of the model to the position of
        # the bounding_box and update the anchor bone as well
        self.model.set_origin(self.pos)
        self.model.get_bone("tronco").a.update(self.model.origin - vector)

        # make the limbs follow specific points
        self.model.get_limb("coxa_e").follow(self.leg_l_target, self.direction)
        self.model.get_limb("coxa_d").follow(self.leg_r_target, self.direction)
        self.model.get_limb("antebraco_e").follow(self.bounding_box.midleft, -self.direction)
        self.model.get_limb("antebraco_d").follow(self.bounding_box.midright, -self.direction)

        # update the skeleton object
        self.model.update()


    def blit(self, canvas: Surface):
        """Draws the player model on the given surface

        Args:
            canvas (Surface): the surface where to draw the player on
        """

        self.model.blit(canvas)
