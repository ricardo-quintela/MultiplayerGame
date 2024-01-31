from config import DEBUG, MAPS
from .procedural_generation import WaveFuncionCollapse


class Map:
    def __init__(self) -> None:
        self.wfc_generator = WaveFuncionCollapse.from_json(MAPS["room_rules"])


        self.map_rooms = self.wfc_generator.generate_map()
