import logging
from typing import List, Tuple, Union, Dict, TypedDict, Deque
from random import Random
from collections import deque

from datetime import datetime

RoomName = str

RoomsList = List[RoomName]


class RoomRules(TypedDict):
    up: RoomsList
    down: RoomsList
    left: RoomsList
    right: RoomsList


class JSONRooms(TypedDict):
    startRoom: str
    rules: Dict[RoomName, RoomRules]


class WaveFuncionCollapse:
    def __init__(
        self, room_rules: Dict[RoomName, RoomRules], start_room: RoomName = ""
    ) -> None:
        self.room_rules = room_rules
        self.start_room = start_room

        self.num_rooms = len(room_rules)
        self.generator = Random()

    def generate_map(
        self, seed: Union[int, float, str, bytes, bytearray] = None, size: int = 1
    ) -> List[List[RoomName]]:

        logging.info("Generating %sx%s map, random_seed=%s", size, size, seed)

        collapse_table: List[List[List[RoomName]]] = [
            [list(self.room_rules.keys()) for _ in range(size)] for _ in range(size)
        ]
        generated_map: List[List[Union[RoomName, None]]] = [
            [None for _ in range(size)] for _ in range(size)
        ]

        # deque containing the entropy of each room
        # the entropy is the number of possible choices to collapse
        entropy_queue: Deque[List[Union[int, Tuple[int, int]]]] = deque()

        # initialize the deque
        for i in range(size):
            for j in range(size):
                entropy_queue.append([999, (i,j)])


        # initialize rng
        self.generator.seed(seed)

        x = size // 2
        y = size // 2

        # initialize with the start room
        collapse_table[y][x] = [self.start_room]

        entropy_queue.rotate(size*size - 1 - (y*size + x))
        start_el = entropy_queue.pop()
        entropy_queue.rotate(-(size*size - 1 - (y*size + x)))
        start_el[0] = 1
        entropy_queue.appendleft(start_el)


        room_count = 0
        while self.collapse_cells(size, collapse_table, generated_map, entropy_queue):
            room_count += 1

        logging.info("Successfully generated a map with %s rooms", room_count)

        return generated_map



    def collapse_cells(
        self,
        size: int,
        collapse_table: List[List[List[RoomName]]],
        generated_map: List[List[Union[RoomName, None]]],
        entropy_queue: Deque[List[Union[int, Tuple[int, int]]]]
    ) -> bool:

        x, y = entropy_queue[0][1]

        if not collapse_table[y][x]:
            return False

        if generated_map[y][x] is not None:
            return False

        if entropy_queue[0][0] == 999:
            return False

        # collapse the room
        room = self.generator.choice(collapse_table[y][x])
        collapse_table[y][x].clear()
        generated_map[y][x] = room

        # update the collapsed room entropy
        current_entropy = entropy_queue.popleft()
        current_entropy[0] = 999
        entropy_queue.append(current_entropy)

        if room is None:
            return True

        self.update_nighbors_rules(x-1,y, self.room_rules[room]["left"], size, collapse_table, entropy_queue)
        self.update_nighbors_rules(x+1,y, self.room_rules[room]["right"], size, collapse_table, entropy_queue)
        self.update_nighbors_rules(x,y+1, self.room_rules[room]["down"], size, collapse_table, entropy_queue)
        self.update_nighbors_rules(x,y-1, self.room_rules[room]["up"], size, collapse_table, entropy_queue)

        return True


    def update_nighbors_rules(
        self,
        x: int,
        y: int,
        available_rooms: RoomsList,
        size: int,
        collapse_table: List[List[List[RoomName]]],
        entropy_queue: Deque[List[Union[int, Tuple[int, int]]]]
    ):
        if not (-1 < x < size and -1 < y < size):
            return

        # update the choices of the cell
        collapse_table[y][x] = list(set(collapse_table[y][x]) & set(available_rooms))
        collapse_table[y][x].sort()

        # update the entropy and sort

        # find the cell on the queue
        queue_offeset = 0
        while entropy_queue[-1][1] != (x,y):
            entropy_queue.rotate(1)
            queue_offeset += 1
        current_entropy = entropy_queue.pop()
        entropy_queue.rotate(-queue_offeset)

        # update the entropy, if the antropy is 0 then the cell can no longer be collapsed and
        # its more optimal to leave it at the end of the queue
        current_entropy[0] = len(collapse_table[y][x]) if len(collapse_table[y][x]) > 0 else 999

        # optimization to the insertion on the end of the queue
        if current_entropy[0] == 999:
            entropy_queue.append(current_entropy)
            return

        # sort the entropy with insertion sort
        queue_index = 0
        while entropy_queue[queue_index][0] < current_entropy[0]:
            queue_index += 1
        entropy_queue.insert(queue_index, current_entropy)



    @classmethod
    def from_json(cls, json_rooms: JSONRooms):
        """Creates an instance of a WaveFunctionCollapse generator
        from a json formated object containing the room rules

        Args:
            json_rooms (JSONRooms): the json rules of each room

        Returns:
            WaveFunctionCollapse: the wfc generator
        """
        return cls(json_rooms["rules"], json_rooms["startRoom"])



    def __repr__(self) -> str:
        return f"WaveFunctionCollapse(num_rooms={self.num_rooms})"




# debugging
if __name__ == "__main__":

    from json import load

    with open("assets/maps/room_rules.json", "r", encoding="utf-8") as file:
        rooms: Dict[str, RoomRules] = load(file)

    wfc_generator = WaveFuncionCollapse.from_json(rooms)
    print(wfc_generator)

    gen_map = wfc_generator.generate_map(seed=18, size=5)

    for line in gen_map:
        for column in line:
            print(column, end=" ")
        print("")
