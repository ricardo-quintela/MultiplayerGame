import logging
from typing import Dict, List
from json import load
from os.path import join

from pygame import Surface
from pygame.image import load as pgload

from blocks import Collider
from config import MAPS

from .json_types import JSONMap, MapFormat, MissingProperty, JSONTileset


LAYER_NAMES = [
    "background",
    "paralax",
    "detail1",
    "block",
    "detail2",
    "collider",
    "poi",
]


class Room:
    def __init__(self, name: str) -> None:
        self.name = name

        self.colliders: List[Collider] = list()

        # layers
        self.block_layer: Surface = Surface(MAPS["room_size"])
        self.block_layer.set_colorkey((0,0,0))

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

        # check amount of layers
        if len(json_room["layers"]) != len(LAYER_NAMES):
            logging.error(
                "Map file '%s' is in the wrong format. %s layers",
                name,
                len(json_room["layers"]) - len(LAYER_NAMES),
            )
            raise MapFormat(
                f"Map file '{name}' is in the wrong format. {len(json_room['layers']) - len(LAYER_NAMES)} layers"
            )

        # check if a layer name is different or out of order
        for i, layer in enumerate(json_room["layers"]):
            if layer["name"] != LAYER_NAMES[i]:
                logging.error(
                    "Map file '%s' is in the wrong format. Layer '%s'",
                    name,
                    layer["name"],
                )
                raise MapFormat(
                    f"Map file '{name}' is in the wrong format. Layer {layer['name']}"
                )

        # load tilesets
        # load the block tileset
        with open(join(MAPS["rooms_folder"], json_room["tilesets"][0]["source"]), "r", encoding="utf-8") as tileset_file:
            json_block_tileset: JSONTileset = load(tileset_file)

        # load the spritesheet
        block_spritesheet = pgload(
            join(MAPS["rooms_folder"], json_block_tileset["image"])
        ).convert_alpha()

        # load block layer
        tile_size = json_block_tileset["tileheight"]
        loaded_tiles: Dict[int, Surface] = dict()
        for i, tile_id in enumerate(json_room["layers"][3]["data"]):

            tile_index = tile_id - json_room["tilesets"][0]["firstgid"]
            if tile_index == -1:
                continue

            if tile_index not in loaded_tiles:
                tile_line = tile_index // json_block_tileset["columns"]
                tile_col = tile_index / json_block_tileset["columns"] - tile_line
                tile_coords = (tile_col * json_block_tileset["imagewidth"], tile_line * tile_size)

                sprite = Surface((json_block_tileset["tilewidth"], json_block_tileset["tileheight"]))
                sprite.blit(block_spritesheet, (0,0), (tile_coords[0], tile_coords[1], tile_size, tile_size))
                loaded_tiles[tile_index] = sprite

            room.block_layer.blit(
                loaded_tiles[tile_index],
                (
                    (i % json_room["width"]) * tile_size,
                    i // json_room["width"] * tile_size
                )
            )
        print(loaded_tiles)


        # create colliders and guarantee that they have the friction attribute
        for json_collider in json_room["layers"][5]["objects"]:

            if json_collider["properties"][0]["name"] != "friction":
                logging.error("Property at collider missing: 'friction'")
                raise MissingProperty("Property at collider missing: 'friction'")

            room.colliders.append(
                Collider(
                    (json_collider["x"], json_collider["y"]),
                    (json_collider["width"], json_collider["height"]),
                    json_collider["properties"][0]["value"],
                )
            )

        logging.info("Map loaded successfully")
        return room
