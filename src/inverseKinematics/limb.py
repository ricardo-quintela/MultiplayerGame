from pygame import Surface

from .bone import Bone


class Limb:

    def __init__(self, name: str = "") -> None:
        """Constructor of the class Limb\n\n

        A limb is a set of bones that are ment to be attached and move together\n
        The limb can be anchored to a fixed point

        Args:
            name (str, optional): the name of the limb. Defaults to "".
        """
        
        self.bones = list()

        self.name = name

        self.anchor = None


    def setName(self, name: str):
        """Sets the name attribute to the given string

        Args:
            name (str): the new name
        """
        self.name = name


    def add(self, bone: Bone):
        """Adds a bone to the limb

        Args:
            bone (Bone): the bone to add
        """

        # add the bone to the list
        self.bones.append(bone)


    def fixate(self, anchor):
        """Anchors the limb to a given point\n\n

        If the given point is a mutable object, then the limb will follow it as it changes

        Args:
            anchor (list, Vector2): the point to anchor the limb
        """
        self.anchor = anchor


    def update(self):
        """Updates all the bones in the skeleton
        """

        self.bones[0].a.update(self.anchor)
        self.bones[0].calculate_b()

        for i in range(1, len(self.bones)):
            self.bones[i].a.update(self.bones[i-1].b)
            self.bones[i].calculate_b()