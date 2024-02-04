import logging
from typing import Dict, List
from json import load
from os.path import join

from pygame import Surface
from pygame.image import load as pgload
from pygame.draw import rect

from blocks import Collider
from config import MAPS
from entities import Enemy

from .json_types import JSONMap, MapFormat, MissingProperty, JSONTileset


LAYER_NAMES = [
    "background",
    "parallax",
    "detail1",
    "block",
    "detail2",
    "collider",
    "poi",
]


DEFAULT_TEXTURE = Surface((32, 32))
DEFAULT_TEXTURE.fill((1, 1, 1))
rect(DEFAULT_TEXTURE, (255, 0, 255), (16, 0, 31, 15))
rect(DEFAULT_TEXTURE, (255, 0, 255), (0, 16, 15, 31))


class Room:
    def __init__(self, name: str) -> None:
        self.name = name

        self.colliders: List[Collider] = list()

        # layers
        self.block_layer: Surface = Surface(MAPS["room_size"])
        self.block_layer.set_colorkey((0, 0, 0))


        self.enemies: List[Enemy] = list()


    def show_bounding_boxes(self, canvas: Surface):
        """Draws the bounding_boxes of all the colliders

        Args:
            canvas (Surface): _description_
        """
        for collider in self.colliders:
            collider.show_bounding_box(canvas)

    @classmethod
    def from_json(cls, name: str, json_room: JSONMap):
        """Loads and renders the assets of a room in different Surface layers

        Args:
            name (str): the room name
            json_room (JSONMap): the room formated json attributes

        Raises:
            MapFormat: In case the room file is not in the correct format
            MissingProperty: If an object doesn't include a required property

        Returns:
            Room: The rendered room
        """
        logging.info("Loading '%s' room", name)

        room = cls(name)

        # check amount of layers
        if len(json_room["layers"]) != len(LAYER_NAMES):
            logging.fatal(
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
                logging.fatal(
                    "Map file '%s' is in the wrong format. Layer '%s'",
                    name,
                    layer["name"],
                )
                raise MapFormat(
                    f"Map file '{name}' is in the wrong format. Layer {layer['name']}"
                )

        # load tilesets
        # load the block tileset
        with open(
            join(MAPS["rooms_folder"], json_room["tilesets"][0]["source"]),
            "r",
            encoding="utf-8",
        ) as tileset_file:
            json_block_tileset: JSONTileset = load(tileset_file)



        try:
            # load the spritesheet
            block_spritesheet = pgload(
                join(MAPS["rooms_folder"], json_block_tileset["image"])
            ).convert_alpha()
        except FileNotFoundError:
            logging.error(
                "Couldn't load texture from '%s'",
                join(MAPS["rooms_folder"], json_block_tileset["image"]),
            )
            block_spritesheet = Surface(
                (json_block_tileset["imagewidth"], json_block_tileset["imageheight"])
            )
            for i in range(json_block_tileset["imagewidth"] // json_block_tileset["tileheight"]):
                for j in range(json_block_tileset["imageheight"] // json_block_tileset["tileheight"]):
                    block_spritesheet.blit(
                        DEFAULT_TEXTURE,
                        (
                            i * json_block_tileset["tilewidth"],
                            j * json_block_tileset["tileheight"],
                        ),
                    )



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
                tile_coords = (
                    tile_col * json_block_tileset["imagewidth"],
                    tile_line * tile_size,
                )

                sprite = Surface(
                    (json_block_tileset["tilewidth"], json_block_tileset["tileheight"])
                )
                sprite.blit(
                    block_spritesheet,
                    (0, 0),
                    (tile_coords[0], tile_coords[1], tile_size, tile_size),
                )
                loaded_tiles[tile_index] = sprite

            room.block_layer.blit(
                loaded_tiles[tile_index],
                (
                    (i % json_room["width"]) * tile_size,
                    i // json_room["width"] * tile_size,
                ),
            )



        # create colliders and guarantee that they have the friction attribute
        for json_collider in json_room["layers"][5]["objects"]:

            if json_collider["properties"][-1]["name"] != "friction":
                logging.fatal("Property at collider missing: 'friction'")
                raise MissingProperty("Property at collider missing: 'friction'")

            # create a collider with the read properties
            collider = Collider(
                    (json_collider["x"], json_collider["y"]),
                    (json_collider["width"], json_collider["height"]),
                    json_collider["properties"][-1]["value"],
                )

            # add the collider to the room
            room.colliders.append(collider)

            # spawn enemies in the room
            if len(json_collider["properties"]) > 1 and json_collider["properties"][-2]["name"] == "enemies_spawnable":
                enemy = Enemy((30,250))
                enemy.set_pos(collider.bounding_box.midtop)
                room.enemies.append(enemy)
                print("spawned enemy")



        logging.info("Room loaded successfully")
        return room
