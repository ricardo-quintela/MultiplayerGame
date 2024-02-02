import logging
from typing import List
from pygame import Surface
from pygame.sprite import Group

from blocks import Collider

from .json_types import JSONMap, MapFormatError


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
    def from_json(cls, name: str, json_room: JSONMap):
        logging.info("Loading map from '%s'", name)


        room = cls(name)

        json_colliders = None
        for layer in json_room["layers"]:
            if layer["type"] == "objectgroup" and layer["name"] == "collider":
                json_colliders = layer["objects"]
                break
        else:
            logging.error("Map file '%s' is in the wrong format", name)
            raise MapFormatError(f"Map file '{name}' is in the wrong format")


        for json_collider in json_colliders:
            room.colliders.append(
                Collider(
                    (json_collider["x"], json_collider["y"]),
                    (json_collider["width"], json_collider["height"]),
                    json_collider["properties"][0]["value"]
                )
            )

        logging.info("Map loaded successfully")

        return room
