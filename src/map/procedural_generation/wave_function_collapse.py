import logging
from typing import List, Tuple, Union, Dict, TypedDict
from random import Random

from pprint import pprint  # TODO: REMOVE

RoomName = str


class RoomRules(TypedDict):
    up: Union[List[Union[str, None]], None]
    down: Union[List[Union[str, None]], None]
    left: Union[List[Union[str, None]], None]
    right: Union[List[Union[str, None]], None]


class WaveFuncionCollapse:
    def __init__(
        self,
        rules: Dict[RoomName, RoomRules],
        seed: Union[int, float, str, bytes, bytearray] = None,
        size: int = 1
    ) -> None:
        self.rules = rules
        self.seed = seed
        self.size = size

        self.num_rooms = len(rules)
        self.generator = Random(seed)

        self.collapse_table = [[[] for _ in range(size)] for _ in range(size)]

        self.generated_map = [[None for _ in range(size)] for _ in range(size)]

    def generate_map(self) -> List[List[int]]:
        logging.info("Generating %sx%s map, random_seed=%s", self.size, self.size, self.seed)

        x = self.size // 2
        y = self.size // 2

        self.generated_map[y][x] = "main"
        if x - 1 >= 0:
            self.collapse_table[y][x-1] = list(set(self.collapse_table[y][x-1]) | set(self.rules["main"]["left"]))
        if x + 1 < self.size:
            self.collapse_table[y][x+1] = list(set(self.collapse_table[y][x+1]) | set(self.rules["main"]["right"]))
        if y - 1 >= 0:
            self.collapse_table[y-1][x] = list(set(self.collapse_table[y-1][x]) | set(self.rules["main"]["down"]))
        if y + 1 < self.size:
            self.collapse_table[y+1][x] = list(set(self.collapse_table[y+1][x]) | set(self.rules["main"]["up"]))

        self._collapse(x-1,y)
        self._collapse(x+1,y)
        self._collapse(x,y-1)
        self._collapse(x,y+1)

        return self.generated_map



    def _collapse(
        self,
        x: int,
        y: int
    ) -> bool:
        """Collapse a specific coordinate

        Args:
            x (int): the x of the room to collapse
            y (int): the y of the room to collapse
        
        Returns:
            bool: True if the wave function collapses; False if it's impossible to do so
        """

        # base cases
        if not (-1 < x < self.size and -1 < y < self.size):
            return False

        if self.generated_map[y][x] is not None:
            return False

        if not self.collapse_table[y][x]:
            return False

        # collapsing
        room = self.generator.choice(self.collapse_table[y][x])
        self.generated_map[y][x] = room

        if x - 1 >= 0:
            self.collapse_table[y][x-1] = list(set(self.collapse_table[y][x-1]) | set(self.rules[room]["left"]))
        if x + 1 < self.size:
            self.collapse_table[y][x+1] = list(set(self.collapse_table[y][x+1]) | set(self.rules[room]["right"]))
        if y - 1 >= 0:
            self.collapse_table[y-1][x] = list(set(self.collapse_table[y-1][x]) | set(self.rules[room]["down"]))
        if y + 1 < self.size:
            self.collapse_table[y+1][x] = list(set(self.collapse_table[y+1][x]) | set(self.rules[room]["up"]))


        return self._collapse(x-1,y) or self._collapse(x+1,y) or self._collapse(x,y-1) or self._collapse(x,y+1)



    def __repr__(self) -> str:
        return f"WaveFunctionCollapse(seed={self.seed},num_rooms={self.num_rooms},size={self.size})"


if __name__ == "__main__":
    room_rules: Dict[str, RoomRules] = {
        "main": {
            "up": ["quoridor", "lootRoom"],
            "down": ["quoridor", "lootRoom"],
            "left": ["quoridor", "lootRoom"],
            "right": ["quoridor", "lootRoom"],
        },
        "lootRoom": {
            "up": ["quoridor", "lootRoom"],
            "down": ["quoridor", "lootRoom"],
            "left": ["quoridor", "lootRoom"],
            "right": ["quoridor", "lootRoom"]
        },
        "quoridor": {
            "up": ["quoridor", "lootRoom"],
            "down": ["quoridor", "lootRoom"],
            "left": ["quoridor", "lootRoom"],
            "right": ["quoridor", "lootRoom"]
        }
    }

    wfc_generator = WaveFuncionCollapse(room_rules, 2, 5)
    print(wfc_generator)

    pprint(wfc_generator.generate_map())
