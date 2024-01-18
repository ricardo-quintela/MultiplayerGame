import logging
from typing import Dict, List
from json import loads
from math import cos, pi

from pygame import Surface, Vector2

from config import ENTITIES, ANIMATIONS, PHYSICS
from utils import MovementKeys
from blocks import Collider
from inverseKinematics import Skeleton
from .animation import Animation, JSONAnimation

from .entity import Entity

KEYFRAME_STEP: float = (ANIMATIONS["leg_target"] * 2) / ANIMATIONS["keyframes"]
COSSINE_RADIUS: float = 2 * ANIMATIONS["leg_target"] / pi

class Player(Entity):
    def __init__(self, hitbox_size) -> None:
        """Constructor of the class Player
        """
        super().__init__(hitbox_size, has_gravity=True)

        # model initialization
        with open("skeleton.json", "r", encoding="utf-8") as model_file:
            json_model = loads(model_file.read())

        self.model = Skeleton.from_json(json_model)

        # animation initialization
        self.current_swing_leg = 0

        self.leg_l_target = Vector2(self.pos)
        self.leg_r_target = Vector2(self.pos)
        self.leg_targets = [self.leg_l_target, self.leg_r_target]

        # keyframe setup
        self.current_keyframe = 0
        self.keyframe_step = -self.direction * ANIMATIONS["leg_target"] / 2 * KEYFRAME_STEP

        self.leg_is_grounded = [False, False]

        self.animations: Dict[str, Animation] = dict()
        self.load_animations()


    def set_pos(self, pos: tuple):
        super().set_pos(pos)

        self.leg_l_target.update(pos)
        self.leg_r_target.update(pos)


    def load_animations(self):
        # TODO: load animations

        animation_paths = ANIMATIONS["animation_paths"]["player"]

        for animation_name, animation_path in animation_paths.items():
            logging.debug("Loading '%s' animation from '%s'", animation_name, animation_path)

            with open(animation_path, "r", encoding="utf-8") as animation_file:
                animation_json: JSONAnimation = loads(animation_file.read())

            animation = Animation.from_json(animation_json)

            self.animations[animation_name] = animation

            logging.debug(
                "Loaded '%s' animation ('%s' keyframes)",
                animation_name,
                animation.num_keyframes
            )



    def calculate_target_pos(self, colliders: List[Collider], target_leg_pos: Vector2) -> Vector2:
        """Calculates the target postion of the leg

        Args:
            colliders (list): the list of colliders in the map
            pos: (Vector2): the player's position
            direction: (int): the direction the player is facing

        Returns:
            Vector2: the target position of the leg end effector
        """
        self.leg_is_grounded[self.current_swing_leg] = False

        for collider in colliders:

            if self.pos.y - ANIMATIONS["leg_target_height"] > collider.bounding_box.top:
                logging.debug("WALL: %s", collider)
                continue

            if collider.bounding_box.collidepoint(target_leg_pos):
                logging.debug("STEP: %s", collider)
                self.leg_is_grounded[self.current_swing_leg] = True
                return Vector2(target_leg_pos.x, collider.bounding_box.top)

        return target_leg_pos



    def animate(self, animation_name: str, colliders: list):
        """Animates each model bone with a list of points
        on the given animation

        Args:
            animation_name (str): the name of the current animation
            colliders (list): the list of colliders in the map
        """

        self.current_keyframe += 1
        if self.current_keyframe == self.animations[animation_name].num_keyframes:
            self.current_keyframe = 0

        keyframe = self.animations[animation_name].keyframes[self.current_keyframe]
        for bone_name, target in keyframe.items():
            # try to get a limb
            bone = self.model.get_limb(bone_name)

            # if it doesnt correspond to a limb then get the bone instead
            if bone is None:
                bone = self.model.get_bone(bone_name)

            bone.follow(self.pos + target[0], target[1] * self.direction)
            logging.debug("ANIMATION_UPDATE: current_keyframe: %s | bone: %s | target_pos: %s | direction: %s", self.current_keyframe, bone_name, self.pos + target[0], target[1])




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
            super().move((0,-ENTITIES["jump_height"]))
            self.is_jumping = True


    def update(self, colliders: List[Collider]):
        """Makes the necessary computations to update the physics of the player
        """
        self.is_climbing = False
        self.leg_is_grounded[self.current_swing_leg] = False

        vector = self.model.origin - self.model.get_bone("tronco").a

        #? LEG ANIMATION
        self.animate("walking", colliders)

        #? hitbox y lifting based on y of leg
        if self.is_moving and self.leg_is_grounded[(self.current_swing_leg + 1) % 2] and self.leg_targets[(self.current_swing_leg + 1) % 2].y < self.pos.y:

            logging.debug("(IS_CLIMBING) NEW_Y: %s", self.bounding_box.bottom)
            self.is_climbing = True
            self.vel.y -= ANIMATIONS["leg_climbing_acc"]


        # calculate position based on velocity
        super().update()

        #? COLLISIONS
        self.check_collisions(colliders)



        #? updates the player model bones

        # move the origin of the model to the position of
        # the bounding_box and update the anchor bone as well
        self.model.set_origin(self.pos)
        self.model.get_bone("tronco").a.update(self.model.origin - vector)

        # update the skeleton object
        self.model.update()


    def blit(self, canvas: Surface):
        """Draws the player model on the given surface

        Args:
            canvas (Surface): the surface where to draw the player on
        """

        self.model.blit(canvas)
