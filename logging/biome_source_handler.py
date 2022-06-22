import json
from dataclasses import dataclass

from typing.io import IO

ListOrInt = "list[int] | int"


@dataclass
class BiomeSource:
    parameters: "list[Parameter]"


@dataclass
class Parameter:
    continentalness: ListOrInt
    erosion: ListOrInt
    weirdness: ListOrInt
    temperature: ListOrInt
    humidity: ListOrInt
    depth: ListOrInt
    offset: int
    biome: str


def create_parameter(biome_and_params: dict) -> Parameter:
    params: dict = biome_and_params["parameters"]
    return Parameter(
        continentalness=params["continentalness"],
        erosion=params["erosion"],
        weirdness=params["erosion"],
        temperature=params["temperature"],
        humidity=params["humidity"],
        depth=params["depth"],
        offset=params["offset"],
        biome=biome_and_params["biome"]
    )


def load_json(f: IO) -> BiomeSource:
    preliminary_biome_source: list = json.load(f)["biome_source"]["biomes"]
    return BiomeSource([create_parameter(params) for params in preliminary_biome_source])
