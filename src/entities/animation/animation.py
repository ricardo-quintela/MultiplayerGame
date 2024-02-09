from typing import Dict, List, Tuple, TypedDict

from pygame import Vector2

from inverse_kinematics import Skeleton

JSONKeyframe = Dict[str, Tuple[Tuple[int], int]]

Keyframe = Dict[str, Tuple[Vector2, int]]

BoneName = str

class JSONAnimation(TypedDict):
    keyframeNum: int
    keyframes: Tuple[JSONKeyframe]

class Animation:
    """Stores the target points of an animation
    """
    def __init__(self) -> None:
        self.name = ""
        self.num_keyframes = 0
        self.skeleton_anchor_keyframes: List[Vector2] = list()
        self.keyframes: List[Keyframe] = list()
        self.bones_order: List[BoneName] = list()


    @classmethod
    def from_json(cls, json_animation: JSONAnimation, skeleton: Skeleton, scale: float = 1.0):
        """Creates an instance of an Animation from json

        Args:
            json_animation (JSONAnimation): the json encoded animation keyframes
            scale (float, Optional): the scale

        Returns:
            Animation: the instanced animation
        """
        # instanciate the animation
        animation = cls()
        animation.num_keyframes = json_animation['keyframeNum']

        # convert the keyframe targets to pygame Vector2
        for json_keyframe in json_animation['keyframes']:

            keyframe = {
                bone_name: (
                    Vector2(int(target_point[0]), int(target_point[1])) * scale,
                    direction
                )
                for bone_name, (target_point, direction) in json_keyframe.items()
            }

            animation.keyframes.append(keyframe)

        # convert the skeleton anchor position to pygame Vector2
        for anchor_keyframe in json_animation['skeletonAnchorKeyframes']:
            animation.skeleton_anchor_keyframes.append(
                Vector2(int(anchor_keyframe[0]), int(anchor_keyframe[1])) * scale
            )


        # the order that the bones should be animated
        for bone_name in animation.keyframes[0]:
            if skeleton.get_limb(bone_name) is None:
                animation.bones_order.insert(0, bone_name)
                continue
            animation.bones_order.append(bone_name)

        print(animation.bones_order)

        return animation


    def __repr__(self) -> str:
        return f"Animation(name='{self.name}', num_keyframes='{self.num_keyframes}')"
