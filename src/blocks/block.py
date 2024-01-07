

from pygame import Rect, Surface
from pygame.draw import rect


class Block:
    def __init__(self, pos: tuple, size: tuple, friction:int = 0) -> None:
        """Constructor of the class Block

        Args:
            pos (tuple): the position of the block
            size (tuple): the size of the block
            friction (tuple): the ammount of friction that the surface has
        """
        
        self.bounding_box = Rect(pos, size)

        self.friction = friction


    
    def show_hitbox(self, canvas: Surface):
        """Draws a rectangle on the given canvas representing the bounding_box of the block

        Args:
            canvas (Surface): the canvas where to draw the rectangle on
        """

        rect(canvas, "red", (self.bounding_box.x, self.bounding_box.y, self.bounding_box.width, self.bounding_box.height), 2)