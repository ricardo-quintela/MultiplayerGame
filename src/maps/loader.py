import logging
from typing import Dict, Tuple, Union
from json import load
from time import time_ns
from datetime import datetime
from os.path import join

from pygame import Vector2


from config import DEBUG, MAPS
from .procedural_generation import WaveFuncionCollapse, Room


class Map:
    def __init__(self) -> None:

        # create a wfc generator to later generate the map rooms
        with open(MAPS["room_rules"], "r", encoding="utf-8") as room_rules_file:
            json_rooms = load(room_rules_file)

        self.wfc_generator = WaveFuncionCollapse.from_json(json_rooms)

        # the map layout, will handle the navigation conditions
        self.map_rooms = self.wfc_generator.generate_map(
            seed=DEBUG["map_seed"], size=MAPS["map_size"]  # TODO: set seed as time_ns()
        )

        self.map_size = len(self.map_rooms)

        # contains all the room objects that the wfc chose to load
        self.rooms: Dict[Tuple[int, int], Room] = dict()

        self.load_rooms()

    def load_rooms(self):
        """Loads the assets for each room that the wfc algorithm has chosen"""
        logging.info("Loading map")
        start_time = datetime.now()

        # iterating through all the room names in the map
        # in order to load the respective rooms from the json files
        # and build the map
        for i in range(self.map_size):
            for j in range(self.map_size):

                # ignore empty spaces
                if self.map_rooms[j][i] is None:
                    continue

                room_name = self.map_rooms[j][i]

                # load the room from a json file with the corresponding name
                with open(
                    join(MAPS["rooms_folder"], f"{room_name}.json"),
                    "r",
                    encoding="utf-8",
                ) as room_file:
                    self.rooms[(j, i)] = Room.from_json(room_name, load(room_file))

        logging.info(
            "Successfully loaded map. Took %s seconds",
            (datetime.now() - start_time).total_seconds(),
        )

        map_string = ""
        for line in self.map_rooms:
            map_string += str(line) + "\n"



    def get_room(self, room_coords: Union[Tuple[int, int], Vector2]):
        """Returns a specific room if it exists

        Args:
            room_coords (Tuple[int, int]): the room coordinates in the map

        Returns:
            Room: the room in the corresponding map coords
        """
        if (room_coords[1], room_coords[0]) not in self.rooms:
            return

        return self.rooms[(room_coords[1], room_coords[0])]
