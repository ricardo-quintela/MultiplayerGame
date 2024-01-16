from typing import List, Dict

from pygame import Surface, Vector2

from .bone import Bone
from .limb import Limb

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


    def set_origin(self, pos: tuple):
        """Updates the origin of the skeleton

        Args:
            pos (tuple): the position where to move the origin to
        """
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


    def get_limb(self, name: str) -> Limb:
        """Returns a limb on the skeleton by the given name

        Args:
            name (str): the name of the limb

        Raises:
            KeyError: if the limb doenst exist in the skeleton

        Returns:
            Limb: the limb on the skeleton
        """

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
        