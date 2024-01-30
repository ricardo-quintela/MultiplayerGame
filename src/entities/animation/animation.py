from typing import Dict, List, Tuple, TypedDict

from pygame import Vector2

JSONKeyframe = Dict[str, Tuple[Tuple[int], int]]

Keyframe = Dict[str, Tuple[Vector2, int]]

class JSONAnimation(TypedDict):
    keyframeNum: int
    keyframes: Tuple[JSONKeyframe]

class Animation:
    """Stores the target points of an animation
    """
    def __init__(self) -> None:
        self.name = ""
        self.num_keyframes = 0
        self.keyframes: List[Keyframe] = list()


    @classmethod
    def from_json(cls, json_animation: JSONAnimation, scale: float = 1.0):
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
                bone_name: (Vector2(target_point) * scale, direction)
                for bone_name, (target_point, direction) in json_keyframe.items()
            }

            animation.keyframes.append(keyframe)

        return animation


    def __repr__(self) -> str:
        return f"Animation(name='{self.name}', num_keyframes='{self.num_keyframes}')"
