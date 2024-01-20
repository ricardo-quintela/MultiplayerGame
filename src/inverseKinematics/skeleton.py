from typing import List, Dict, Sequence, Union
import logging

from pygame import Surface, Vector2

from .bone import Bone
from .limb import Limb
from .types import JSONSkeleton

class Skeleton:

    def __init__(self) -> None:
        """Constructor of the class skeleton\n\n

        A skeleton is a set of bones that can be customized and controlled all at once
        """

        self.bones: List[Bone] = list()
        self._names: Dict[str ,int] = dict()

        self.limbs: List[Limb] = list()
        self._limbs_names: Dict[str ,int] = dict()

        self.origin = Vector2(0,0)

        self.skeleton_anchor: Bone = None


    def set_origin(self, pos: Sequence[int]):
        """Updates the origin of the skeleton

        Args:
            pos (tuple): the position where to move the origin to
        """
        if len(pos) != 2:
            raise IndexError(f"Received an invalid position - length: '{pos}'")

        self.origin.update(pos)


    def add(self, bone: Bone):
        """Adds a bone to the skeleton

        Args:
            bone (Bone): the bone to add
        """

        # assign a name to the bone if it has no name and add it to the names dict
        if bone.name == "":
            self._names[str(len(self.bones))] = len(self.bones)
        else:
            self._names[bone.name] = len(self.bones)

        # add the bone to the list
        self.bones.append(bone)


    def new_limb(self, name: str = ""):
        """Adds a new limb to the skeleton

        Args:
            name (str, optional): the name of the limb. Defaults to "".
        """


        if name == "":
            self._limbs_names[str(len(self.limbs))] = len(self.limbs)
        else:
            self._limbs_names[name] = len(self.limbs)

        self.limbs.append(Limb(name))


    def get_bone(self, name: str) -> Bone:
        """Returns a bone on the skeleton by the given name

        Args:
            name (str): the name of the bone

        Raises:
            KeyError: if the bone doenst exist in the skeleton

        Returns:
            Bone: the bone on the skeleton
        """
        return self.bones[self._names[name]]


    def get_limb(self, name: str) -> Union[Limb, None]:
        """Returns a limb on the skeleton by the given name

        Args:
            name (str): the name of the limb

        Raises:
            KeyError: if the limb doenst exist in the skeleton

        Returns:
            (Limb | None): the limb on the skeleton or None if the given name is not a limb
        """
        if name not in self._limbs_names:
            return

        return self.limbs[self._limbs_names[name]]


    def update(self):
        """Updates all the bones in the skeleton
        """

        for bone in self.bones:
            bone.update()

        for limb in self.limbs:
            limb.update()


    def blit(self, canvas: Surface):
        """Draw all the bones on the given Surface

        Args:
            canvas (Surface): the Surface where to draw the bones
        """

        for bone in self.bones:
            bone.blit(canvas)



    def __repr__(self) -> str:
        """Returns a string representation of the object

        Returns:
            str: the string representation of the object
        """
        string = "Origin: " + str(self.origin.x) + ", " + str(self.origin.y) + "\n"

        bones = list(self._names.keys())

        for limb in self._limbs_names:
            string += limb + ":\n"
            for bone in self.get_limb(limb).bones:
                string += "\t" + bone.name + "\n"
                bones.remove(bone.name)

        for bone in bones:
            string += bone + "\n"

        return string


    @classmethod
    def from_json(cls, json_model: JSONSkeleton):
        """Loads the skeleton model from the given json

        Args:
            json_model (JSONSkeleton): the json skeleton

        Returns:
            Skeleton: the Skeleton instance
        """

        # all the bones are placed relative to the origin
        origin = json_model["origin"]

        # create a skeleton object
        skeleton = cls()
        skeleton.set_origin(origin)

        # add the bones to the skeleton (they dont need to be in order because
        # the skeleton object allows hash searching by the name of the bone/limb)
        for bone in json_model["segments"]:
            skeleton.add(
                Bone(
                    bone["a"][0] + origin[0],
                    bone["a"][1] + origin[1],
                    bone["length"],
                    bone["angle"],
                    bone["name"]
                )
            )


        #? create limbs with connected bones
        # iterate through all the segments
        for segment in json_model["segments"]:

            # if the segment is linked to some other
            if segment["links"][0]:

                # get the segment that is linked to it
                parent = segment["links"][0].split(".") if segment["links"][0] is not None else None

                # and the name of the bone
                name = segment["name"]

                # create a limb object and attach them together
                skeleton.new_limb(parent[0])
                skeleton.get_limb(parent[0]).set_master(skeleton.get_bone(parent[0]))
                skeleton.get_limb(parent[0]).set_slave(skeleton.get_bone(name), parent[1])


        #?anchor bones to others
        # iterate through all the segments
        for segment in json_model["segments"]:

            # if the segment is anchored to some other
            if segment["links"][1]:

                # get the information about which bone and the point its anchored to
                anchor = segment["links"][1].split(".")

                # get the anchor bone
                anchor_bone = skeleton.get_bone(anchor[0])

                # get the point the bone is anchored to
                if anchor[1] == "a":
                    point = anchor_bone.a
                else:
                    point = anchor_bone.b

                # try to anchor a limb, if the limb doesnt exist, then anchor a bone
                bone = skeleton.get_limb(segment["name"])
                if bone is not None:
                    bone.fixate(point)
                    continue

                bone = skeleton.get_bone(segment["name"])
                bone.fixate(point, anchor[2])
                skeleton.skeleton_anchor = anchor_bone


        return skeleton
