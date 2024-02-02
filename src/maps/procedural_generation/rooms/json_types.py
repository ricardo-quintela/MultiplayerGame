from typing import List, Optional, TypedDict, Union, Literal


class MapFormat(Exception):
    """Raised when a map JSON file is not on the correct format
    """

class MissingProperty(Exception):
    """Raised when a JSONProperty is missing in an object
    """



class JSONPoint(TypedDict):
    x: int
    y: int

JSONGrid = JSONPoint
JSONTileOffset = JSONPoint


class JSONProperty(TypedDict):
    name: str
    type: Literal["string", "int", "float", "bool", "color"]
    propertytype: str
    value: Union[str, int, float, bool]


class JSONText(TypedDict):
    bold: bool
    color: str
    fontfamily: str
    halign: Literal["center", "right", "justify", "left"]
    italic: bool
    kerning: bool
    pixelsize: int
    strikeout: bool
    text: str
    underline: bool
    valign: Literal["center", "bottom", "top"]
    wrap: bool


class JSONTransformations(TypedDict):
    hflip: bool
    vflip: bool
    rotate: bool
    preferuntransformed: bool



class JSONTerrain(TypedDict):
    name: str
    properties: List[JSONProperty]
    tile: int


class JSONFrame(TypedDict):
    duration: int
    tileid: int



class JSONMapObject(TypedDict):
    ellipse: bool
    gid: int
    height: float
    id: int
    name: str
    point: bool
    polygon: List[JSONPoint]
    polyline: List[JSONPoint]
    properties: List[JSONProperty]
    rotation: float
    template: str
    text: JSONText
    type: str
    visible: bool
    width: int
    x: int
    y: int


class JSONLayer(TypedDict):
    compression: Literal["zlib", "gzip", "zstd"]
    data: Optional[List[int]]
    draworder: Literal["topdown", "index"]
    encoding: Literal["csv", "base64"]
    height: int
    id: int
    name: str
    objects: Optional[List[JSONMapObject]]
    offsetx: int
    offsety: int
    opacity: float
    parallaxx: float
    parallaxy: float
    properties: List[JSONProperty]
    tintcolor: str
    type: Literal["tilelayer", "objectgroup"]
    visible: bool
    width: int
    x: int
    y: int


class JSONWangTiles(TypedDict):
    tileid: int
    wangid: List[int]



class JSONWangColor(TypedDict):
    color: str
    name: str
    probability: float
    properties: List[JSONProperty]
    tile: int



class JSONWangSet(TypedDict):
    colors: List[JSONWangColor]
    name: str
    properties: List[JSONProperty]
    tile: int
    type: Literal["corner", "edge", "mixed"]
    wangtiles: List[JSONWangTiles]



class JSONTile(TypedDict):
    animation: List[JSONFrame]
    id: int
    image: str
    imageheight: int
    imagewidth: int
    x: int
    y: int
    width: int
    height: int
    objectgroup: JSONLayer
    probability: float
    properties: List[JSONProperty]
    type: str



class JSONTileset(TypedDict):
    backgroundcolor: Optional[str]
    columns: int
    fillmode: Literal["stretch", "preserve-aspect-fit"]
    firstgid: int
    grid: JSONGrid
    image: str
    imageheight: int
    imagewidth: int
    margin: int
    name: str
    objectalignment: Literal["unspecified", "topleft", "top", "topright", "left", "center", "right", "bottomleft", "bottom", "bottomright"]
    properties: List[JSONProperty]
    source: str
    spacing: int
    terrains: Optional[List[JSONTerrain]]
    tilecount: int
    tiledversion: str
    tileheight: int
    tileoffset: Optional[JSONTileOffset]
    tilerendersize: Literal["tile", "grid"]
    tiles: Optional[List[JSONTile]]
    tilewidth: int
    transformations: Optional[JSONTransformations]
    transparentcolor: Optional[str]
    type: Literal["tileset"]
    version: str
    wangsets: List[JSONWangSet]




class JSONMap(TypedDict):
    backgroundcolor: Optional[str]
    compressionlevel: int
    height: int
    infinite: bool
    layers: List[JSONLayer]
    nextlayerid: int
    nextobjectid: int
    orientation: Literal["orthogonal", "isometric", "staggered", "hexagonal"]
    properties: List[JSONProperty]
    renderorder: Literal["right-down", "right-up", "left-down", "left-up"]
    tiledversion: str
    tileheight: int
    tilesets: List[JSONTileset]
    tilewidth: int
    type: Literal["map"]
    version: str
    width: int
