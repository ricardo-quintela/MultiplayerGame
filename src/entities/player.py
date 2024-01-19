import logging
from typing import Dict, List
from json import loads

from pygame import Surface
from pygame.draw import circle

from config import ENTITIES, ANIMATIONS, MODELS
from utils import MovementKeys
from blocks import Collider
from inverseKinematics import Skeleton
from .animation import Animation, JSONAnimation

from .entity import Entity


class Player(Entity):
    def __init__(self, hitbox_size) -> None:
        """Constructor of the class Player
        """
        super().__init__(hitbox_size, has_gravity=True)

        # model initialization
        with open(MODELS["player"], "r", encoding="utf-8") as model_file:
            json_model = loads(model_file.read())

        self.model = Skeleton.from_json(json_model)

        # keyframe setup
        self.current_keyframe = 0
        self.current_animation = "walking"

        self.animations: Dict[str, Animation] = dict()
        self.load_animations()


    def load_animations(self):
        """Loads all the animations of the player from the
        corresponding json files
        """

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

            bone.follow(self.model.origin + (target[0].x * self.direction, target[0].y), target[1] * self.direction)
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

        vector = self.model.origin - self.model.get_bone("tronco").a

        # calculate position based on velocity
        super().update()

        #? updates the player model bones
        # move the origin of the model to the position of
        # the bounding_box and update the anchor bone as well
        self.model.set_origin(self.pos)
        self.model.get_bone("tronco").a.update(self.model.origin - vector)

        # update the skeleton object
        self.model.update()

        #? COLLISIONS
        self.check_collisions(colliders)

        #? LEG ANIMATION
        self.animate(self.current_animation, colliders)



    def blit(self, canvas: Surface):
        """Draws the player model on the given surface

        Args:
            canvas (Surface): the surface where to draw the player on
        """

        self.model.blit(canvas)

        circle(canvas, "aqua", self.model.get_bone("perna_e").b, 4)
        circle(canvas, "orange", self.model.get_bone("perna_d").b, 4)
        circle(canvas, "aqua", self.model.get_bone("braco_e").b, 4)
        circle(canvas, "orange", self.model.get_bone("braco_d").b, 4)
