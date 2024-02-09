import logging
from typing import Dict, List, Union
from json import load

from pygame import Surface

from config import ANIMATIONS
from blocks import Collider
from inverse_kinematics import Skeleton
from weapons import Weapon

from .animation import Animation, JSONAnimation
from .entity import Entity

ANIMATION_FRAME_SKIP: int = int(1 / ANIMATIONS["animation_speed"])


class SkeletonAnimated(Entity):
    """A SkeletonAnimated entity has a skeleton based model and
    can handle animations.

    The animations can be loaded via a dictionary containing the animation name
    and the path to the json file
    """

    def __init__(self, bounding_box_size: tuple, model_path: str, animation_paths: Dict[str, str], scale: float = 1.0) -> None:
        """Constructor of the class SkeletonAnimated
        """
        super().__init__(
            (bounding_box_size[0] * scale, bounding_box_size[1] * scale),
            has_gravity=True
        )

        logging.info("Loading model '%s'", model_path)

        # model initialization
        with open(model_path, "r", encoding="utf-8") as model_file:
            json_model = load(model_file)

        self.model = Skeleton.from_json(json_model, scale)

        # keyframe setup
        #* the keyframe updater makes the animation slower compared to the
        #* root update frequency
        self.keyframe_updater: int = ANIMATION_FRAME_SKIP - 1
        self.current_keyframe: int = 0
        self.current_animation: str = None

        self.animations: Dict[str, Animation] = dict()
        self.load_animations(animation_paths, scale)

        # weapons
        self.weapon: Weapon = None


    def set_pos(self, pos: tuple):
        super().set_pos(pos)

        vector = self.model.origin - self.model.skeleton_anchor.get_pos()

        self.model.set_origin(self.pos)
        self.model.skeleton_anchor.set_pos(self.model.origin - vector)


    def load_animations(self, animation_paths: Dict[str, str], scale: float = 1.0):
        """Loads all the animations of the model from the
        corresponding json files
        """

        for animation_name, animation_path in animation_paths.items():
            logging.info(
                "Loading '%s' '%s' animation from '%s'",
                self.__class__,
                animation_name,
                animation_path
            )

            with open(animation_path, "r", encoding="utf-8") as animation_file:
                json_animation: JSONAnimation = load(animation_file)

            animation = Animation.from_json(json_animation, self.model, scale)

            self.animations[animation_name] = animation

            logging.info(
                "Loaded '%s' animation ('%s' keyframes)",
                animation_name,
                animation.num_keyframes
            )


    def set_weapon(self, weapon: Weapon):
        self.weapon = weapon
        self.weapon.attach(self.model.get_bone("braco_d"))



    def animate(self, animation_name: str, colliders: list):
        """Animates each model bone with a list of points
        on the given animation

        Args:
            animation_name (str): the name of the current animation
            colliders (list): the list of colliders in the map
        """
        if self.current_animation is None:
            return


        self.keyframe_updater = (self.keyframe_updater + 1) % ANIMATION_FRAME_SKIP

        if self.keyframe_updater == 0:

            self.current_keyframe += 1
            if self.current_keyframe == self.animations[animation_name].num_keyframes:
                self.current_keyframe = 0

        skeleton_anchor = self.animations[animation_name].skeleton_anchor_keyframes[self.current_keyframe]

        self.model.skeleton_anchor.b.update(
            self.model.origin - (skeleton_anchor.x * self.direction, skeleton_anchor.y)
        )
        self.model.skeleton_anchor.calculate_other()


        keyframe = self.animations[animation_name].keyframes[self.current_keyframe]
        for bone_name in self.animations[animation_name].bones_order:
            # try to get a limb
            bone = self.model.get_limb(bone_name)

            # if it doesnt correspond to a limb then get the bone instead
            if bone is None:
                bone = self.model.get_bone(bone_name)

            bone.update()
            bone.follow(
                self.model.origin + (keyframe[bone_name][0].x * self.direction, keyframe[bone_name][0].y),
                keyframe[bone_name][1] * self.direction
            )

        # update the weapons
        if self.weapon is not None:
            self.weapon.update(self.direction)



    def change_animation_state(self, animation_state: str):
        """Sets the new animation state and
        resets current keyframe and keyframe updater counters

        Args:
            animation_state (str): the new animation state
        """
        self.current_animation = animation_state
        self.current_keyframe = 0
        self.keyframe_updater = 0


    def update(self, colliders: List[Collider]) -> Dict[str, Union[Collider, None]]:
        """Makes the necessary computations to update the physics of the entity
        and handles model animations
        """
        self.is_climbing = False

        vector = self.model.origin - self.model.skeleton_anchor.get_pos()


        # calculate position based on velocity
        super().update()


        #? COLLISIONS
        collisions = self.check_collisions(colliders)

        #? updates the model's bones
        # move the origin of the model to the position of
        # the bounding_box and update the anchor bone as well
        self.model.set_origin(self.pos)
        self.model.skeleton_anchor.set_pos(self.model.origin - vector)

        self.animate(self.current_animation, colliders)

        return collisions


    def show_bounding_box(self, canvas: Surface):
        super().show_bounding_box(canvas)

        # show the weapon's hitbox
        if self.weapon is not None:
            self.weapon.show_hitbox(canvas)


    def blit(self, canvas: Surface):
        """Draws the model on the given surface

        Args:
            canvas (Surface): the surface where to draw the model on
        """

        self.model.blit(canvas)
