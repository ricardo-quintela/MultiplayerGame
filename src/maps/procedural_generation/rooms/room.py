from typing import List
from pygame import Surface
from pygame.sprite import Group

from blocks import Collider


class Room:
    def __init__(self, name: str) -> None:
        self.name = name

        self.colliders: List[Collider] = list()

        # sprite groups
        self.block_sprites = Group()


    def show_bounding_boxes(self, canvas: Surface):
        """Draws the bounding_boxes of all the colliders

        Args:
            canvas (Surface): _description_
        """
        for collider in self.colliders:
            collider.show_bounding_box(canvas)


    @classmethod
    def from_json(cls, json_room):
        raise NotImplementedError
