import json
from dataclasses import dataclass

ListOrInt = "list[int] | int"


@dataclass
class ParameterInstance:
    continentalness: ListOrInt
    erosion: ListOrInt
    depth: ListOrInt
    weirdness: ListOrInt
    temperature: ListOrInt
    humidity: ListOrInt
    offset: int
