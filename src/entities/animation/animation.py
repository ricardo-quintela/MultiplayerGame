from typing import Dict, List, Tuple, TypedDict

from pygame import Vector2

JSONKeyframe = Dict[str, List[List[int, int], int]]

Keyframe = Dict[str, Tuple[Vector2, int]]

class JSONAnimation(TypedDict):
    keyframeNum: int
    keyframes: List[JSONKeyframe]

class Animation:
    """Stores the target points of an animation
    """
    def __init__(self) -> None:
        self.num_keyframes = 0
        self.keyframes: List[JSONKeyframe] = list()


    @classmethod
    def from_json(cls, json_animation: JSONAnimation):
        """Creates an instance of an Animation from json

        Args:
            json_animation (JSONAnimation): the json encoded animation keyframes

        Returns:
            Animation: the instanced animation
        """
        # instanciate the animation
        animation = cls()
        animation.num_keyframes = json_animation['keyframeNum']

        # convert the keyframe targets to pygame Vector2
        for json_keyframe in json_animation['keyframes']:

            keyframe = {
                bone_name: (Vector2(target_point), direction)
                for bone_name, (target_point, direction) in json_keyframe.items()
            }

            animation.keyframes.append(keyframe)

        return animation
