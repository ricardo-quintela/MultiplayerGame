from typing import List, TypedDict, Union

class Segment(TypedDict):
    name: str
    a: List[float]
    b: List[float]
    angle: float
    length: float
    links: List[Union[str, None]]
    isAnchor: bool


class JSONSkeleton(TypedDict):
    name: str
    origin: List[int]
    segments: List[Segment]
