from typing import Union

from .Util import writeDictToJson


def create(name: str, textures: dict[str, str], parent: str):
    writeDictToJson(f"models/{name}", {"parent": parent, "textures": textures})


def createItem(name: str, *textures: Union[list[str], tuple[str, ...], str]):
    texturesDict: dict[str, str] = {}
    for index, texture in enumerate(textures):
        texturesDict[f"layer{index}"] = texture
    create(f"item/{name}", texturesDict, "item/generated")


def createBlock(name: str, textures: Union[dict[str, str], str], parent: str = "block/cube_all"):
    if type(textures) is str:
        textures = {"all": textures}
    create(f"block/{name}", textures, parent)
