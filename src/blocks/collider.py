from pygame import Rect, Surface
from pygame.draw import rect

from config import DEBUG


class Collider:
    def __init__(self, pos: tuple, size: tuple, friction: int = 0) -> None:
        """Constructor of the class Collider

        Args:
            pos (tuple): the position of the collider
            size (tuple): the size of the collider
            friction (tuple): the ammount of friction that the surface has
        """

        self.bounding_box = Rect(pos, size)

        self.friction = friction

    def show_bounding_box(self, canvas: Surface):
        """Draws a rectangle on the given canvas representing the bounding_box of the collider

        Args:
            canvas (Surface): the canvas where to draw the rectangle on
        """

        rect(
            canvas,
            DEBUG["collider_bbox_color"],
            (
                self.bounding_box.x,
                self.bounding_box.y,
                self.bounding_box.width,
                self.bounding_box.height,
            ),
            2,
        )

    def __repr__(self) -> str:
        return f"Collider({self.bounding_box.x, self.bounding_box.y, self.bounding_box.width, self.bounding_box.height})"
