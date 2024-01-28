import logging
from typing import List, Tuple, Union, Dict, TypedDict, Deque
from random import Random
from collections import deque

RoomName = str

RoomsList = List[RoomName]


class RoomRules(TypedDict):
    up: RoomsList
    down: RoomsList
    left: RoomsList
    right: RoomsList


class JSONRooms(TypedDict):
    mainRoom: str
    rules: Dict[RoomName, RoomRules]


class WaveFuncionCollapse:
    def __init__(
        self, rules: Dict[RoomName, RoomRules], start_room: RoomName = ""
    ) -> None:
        self.rules = rules
        self.start_room = start_room

        self.num_rooms = len(rules)
        self.generator = Random()

    def generate_map(
        self, seed: Union[int, float, str, bytes, bytearray] = None, size: int = 1
    ) -> List[List[RoomName]]:
        """Generates a map using a variation of the WFC algorithm

        Args:
            seed (Union[int, float, str, bytes, bytearray], Optional): the rng seed.
            Defaults to None

        Returns:
            List[List[RoomName]]: the map
        """
        logging.info("Generating %sx%s map, random_seed=%s", size, size, seed)

        collapse_table: List[List[List[RoomName]]] = [
            [list(self.rules.keys()) for _ in range(size)] for _ in range(size)
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
                entropy_queue.append([self.num_rooms, (i,j)])


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

        # collapse the room
        room = self.generator.choice(collapse_table[y][x])
        collapse_table[y][x].clear()
        generated_map[y][x] = room

        # update the collapsed room entropy
        current_entropy = entropy_queue.popleft()
        current_entropy[0] = 999
        entropy_queue.append(current_entropy)


        self.update_nighbors_rules(x-1,y, self.rules[room]["left"], size, collapse_table, entropy_queue)
        self.update_nighbors_rules(x+1,y, self.rules[room]["right"], size, collapse_table, entropy_queue)
        self.update_nighbors_rules(x,y+1, self.rules[room]["down"], size, collapse_table, entropy_queue)
        self.update_nighbors_rules(x,y-1, self.rules[room]["up"], size, collapse_table, entropy_queue)

        return True


    def update_nighbors_rules(
        self,
        x: int,
        y: int,
        room_rules: RoomsList,
        size: int,
        collapse_table: List[List[List[RoomName]]],
        entropy_queue: Deque[List[Union[int, Tuple[int, int]]]]
    ):
        if not (-1 < x < size and -1 < y < size):
            return

        # update the choices of the cell
        collapse_table[y][x] = list(set(collapse_table[y][x]) & set(room_rules))
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
        while entropy_queue[queue_index][0] <= current_entropy[0]:
            queue_index += 1
        entropy_queue.insert(queue_index, current_entropy)



    def __repr__(self) -> str:
        return f"WaveFunctionCollapse(num_rooms={self.num_rooms})"


# debugging
if __name__ == "__main__":
    rooms: Dict[str, RoomRules] = {
        "main": {
            "up": ["lootRoom"],
            "down": ["lootRoom"],
            "left": ["quoridor", "lootRoom"],
            "right": ["quoridor", "lootRoom"],
        },
        "lootRoom": {
            "up": ["lootRoom"],
            "down": ["lootRoom"],
            "left": ["quoridor", "lootRoom"],
            "right": ["quoridor", "lootRoom"],
        },
        "quoridor": {
            "up": [],
            "down": [],
            "left": ["quoridor", "lootRoom"],
            "right": ["quoridor", "lootRoom"],
        },
    }

    wfc_generator = WaveFuncionCollapse(rooms, "main")
    print(wfc_generator)

    gen_map = wfc_generator.generate_map(seed=2, size=10)

    for line in gen_map:
        for column in line:
            print(column, end=" ")
        print("")
