import logging
from typing import List, Tuple
from pygame import Surface, Vector2

from math import cos, pi

from config import ENTITIES, ANIMATIONS, PHYSICS
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
        super().__init__(hitbox_size, has_gravity=True) #TODO: implement gravity

        self.model = load_skeleton("skeleton.json")

        self.leg_l_target = Vector2(self.pos)
        self.leg_r_target = Vector2(self.pos)

        self.hip = self.model.get_limb("coxa_e").anchor

        self.current_swing_leg = 0

        self.leg_targets = [self.leg_l_target, self.leg_r_target]

        self.current_keyframe = -ANIMATIONS["KEYFRAMES"] / 2
        self.cossine_step = -self.direction * ANIMATIONS["LEG_TARGET"] / 2 * KEYFRAME_STEP

        self.leg_is_grounded = False


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

        for block in colliders:
            if block.bounding_box.collidepoint(target_leg_pos):
                self.leg_is_grounded = True
                return Vector2(target_leg_pos.x, block.bounding_box.top)


        self.leg_is_grounded = False
        return target_leg_pos


        # # ray cast the target position until it reaches the limit of the bounding_box
        # while target_leg_pos.y < self.pos.y:

        #     # check collisions of the target point for each object
        #     for block in colliders:

        #         # TODO: maybe calculate the intersection of the circumference and the block's top
        #         # done with x = a - sqrt(-b^2 + r^2 + 2*b*y - y^2)


        #         # if the point collides with an object and its top is between
        #         # the allowed step heightset the target position to the top of the block
        #         if block.bounding_box.collidepoint(target_leg_pos) and block.bounding_box.top >= self.pos.y - ANIMATIONS["LEG_TARGET_HEIGHT"]:
        #             target_leg_pos.y = block.bounding_box.top
        #             self.leg_is_grounded = True
        #             break # break the for loop


        #     else: # update the target y position if the for loop completes without breaking
        #         target_leg_pos.y += ANIMATIONS["LEG_SCANNER_STEP"]
        #         continue # continue the while loop

        #     break # break if the program doesnt enter else

        # return target_leg_pos



    def move_legs(self, colliders: list):
        """Moves the legs using procedural movement calculation
        algorithms

        Args:
            colliders (list): the list of colliders in the map
        """

        if self.is_jumping:
            return

        self.current_keyframe += 1
        self.cossine_step += KEYFRAME_STEP * self.direction

        #! RAYCAST OF TARGET POS
        # calculate the target position
        target_leg_pos_x = self.pos.x + self.current_keyframe * KEYFRAME_STEP * self.direction
        target_leg_pos = Vector2(
            target_leg_pos_x,
            self.pos.y - cos(self.cossine_step / COSSINE_RADIUS) * ANIMATIONS["LEG_TARGET_HEIGHT"]
        )


        if self.current_keyframe <= 25:
            final_target_leg_pos = target_leg_pos
        else:
            final_target_leg_pos = self.calculate_target_pos(colliders, target_leg_pos)

        self.leg_targets[self.current_swing_leg].update(final_target_leg_pos)


        if self.leg_is_grounded or self.current_keyframe == ANIMATIONS["KEYFRAMES"] / 2:
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

    def update(self, colliders: list):
        """Makes the necessary computations to update the physics of the player
        """
        self.is_climbing = False

        vector = self.model.origin - self.model.get_bone("tronco").a

        #? LEG ANIMATION
        if self.is_moving:
            self.move_legs(colliders)

        # calculate position based on velocity
        super().update()


        #? hitbox y lifting based on y of leg
        if self.is_moving and self.leg_targets[(self.current_swing_leg + 1) % 2].y < self.pos.y:
            logging.debug("(IS_CLIMBING) NEW_Y: %s", self.bounding_box.bottom)
            self.is_climbing = True
            self.vel.y = -ANIMATIONS["LEG_CLIMBING_ACC"]

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
