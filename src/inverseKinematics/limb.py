from math import acos, atan2, degrees, pi, cos, sin

from pygame import Surface, Vector2

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

        self.size = 0


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

        if len(self.bones) > 2:
            raise Exception("Can't add more bones to " + self.name)

        # add the bone to the list
        self.bones.append(bone)

        self.size += bone.length


    def fixate(self, anchor):
        """Anchors the limb to a given point\n\n

        If the given point is a mutable object, then the limb will follow it as it changes

        Args:
            anchor (list, Vector2): the point to anchor the limb
        """
        self.anchor = anchor


    
    def follow(self, target: tuple, direction: int = 1):
        if len(self.bones) > 2:
            raise Exception("Too many bones on " + self.name)
        elif len(self.bones) < 2:
            raise Exception("Not enough bones on " + self.name)

        # precisamos de um end effector -> target
        end_effector = Vector2(target)


        # temos que calcular o vetor do end effector
        end_effector_vector = end_effector - self.bones[0].a

        

        # precisamos do angulo do vetor do end effector
        end_effector_vector_angle = atan2(end_effector_vector.y, end_effector_vector.x)

        # precisamos da distancia maxima que o membro pode esticar
        d = max(abs(self.bones[0].length - self.bones[1].length), min(self.bones[0].length + self.bones[1].length, end_effector_vector.length()))

        # precisamos da distancia do ombro ao end effector
        distance = Vector2(cos(end_effector_vector_angle) * d, sin(end_effector_vector_angle) * d)



        temp1 = ((self.bones[0].length**2 - self.bones[1].length**2 + distance.length_squared()) / 
            (2 * self.bones[0].length * distance.length()))

        if temp1 < -1:
            temp1 = -1
        elif temp1 > 1:
            temp1 = 1

        theta1 = -direction * acos(temp1) + end_effector_vector_angle



        temp2 = ((self.bones[0].length**2 + self.bones[1].length**2 - distance.length_squared()) / 
            (2 * self.bones[0].length * self.bones[1].length))

        if temp2 < -1:
            temp2 = -1
        elif temp2 > 1:
            temp2 = 1

        theta2 = acos(temp2) * -direction

        
        self.bones[0].setRotation(degrees(theta1))
        self.bones[0].calculate_b()

        self.bones[1].set_pos(self.bones[0].b)
        self.bones[1].setRotation(degrees(pi - (2 * pi - theta2 - theta1)))
        self.bones[1].calculate_b()





    def update(self):
        """Updates all the bones in the skeleton
        """

        for bone in self.bones:
            bone.update()

        if self.anchor and self.bones:
            self.bones[0].a.update(self.anchor)


    def blit(self, canvas: Surface):
        """Draws the limb on the given surface

        Args:
            canvas (Surface): the surface where to draw the limb on
        """

        for bone in self.bones:
            bone.blit(canvas)