

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
        
        self.hitbox = Rect(pos, size)

        self.friction = friction


    
    def show_hitbox(self, canvas: Surface):
        """Draws a rectangle on the given canvas representing the hitbox of the block

        Args:
            canvas (Surface): the canvas where to draw the rectangle on
        """

        rect(canvas, "red", (self.hitbox.x, self.hitbox.y, self.hitbox.width, self.hitbox.height), 2)