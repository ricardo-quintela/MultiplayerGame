from pygame import Surface

from utils import load_skeleton


class Player:
    def __init__(self) -> None:
        """Constructor of the class Player
        """
        
        self.model = load_skeleton("skeleton.json")


    def update(self):
        """Makes the necessary computations to update the physics of the player
        """
        self.model.update()


    def blit(self, canvas: Surface):
        """Draws the player model on the given surface

        Args:
            canvas (Surface): the surface where to draw the player on
        """

        self.model.blit(canvas)