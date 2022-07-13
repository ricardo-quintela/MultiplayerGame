from pygame import Surface

from .bone import Bone
from .limb import Limb

class Skeleton:

    def __init__(self) -> None:
        """Constructor of the class skeleton\n\n

        A skeleton is a set of bones that can be customized and controlled all at once
        """
        
        self.bones = list()
        self._names = dict()

        self.limbs = list()
        self._limbs_names = dict()


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


    def newLimb(self, name: str = ""):
        """Adds a new limb to the skeleton

        Args:
            name (str, optional): the name of the limb. Defaults to "".
        """


        if name == "":
            self._limbs_names[str(len(self.limbs))] = len(self.limbs)
        else:
            self._limbs_names[name] = len(self.limbs)

        self.limbs.append(Limb(name))


    def getBone(self, name: str) -> Bone:
        """Returns a bone on the skeleton by the given name

        Args:
            name (str): the name of the bone

        Raises:
            KeyError: if the bone doenst exist in the skeleton

        Returns:
            Bone: the bone on the skeleton
        """

        return self.bones[self._names[name]]


    def getLimb(self, name: str) -> Limb:
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