import json
import os
from typing import Union


class Model:
    parent: str
    textures: dict[str, str]

    def __init__(self, name: str, textures: dict[str, str], parent: str):
        self.textures = textures
        self.parent = parent
        self.write(name)

    def write(self, name: str):
        file = os.path.join("models", name) + ".json"
        os.makedirs(os.path.dirname(file), exist_ok=True)
        with open(file, "w") as file:
            json.dump({
                "parent": self.parent,
                "textures": self.textures},
                file, indent=2)


class Item(Model):
    def __init__(self, name: str, *textures: Union[list[str], tuple[str, ...], str]):
        texturesDict: dict[str, str] = {}
        for index, texture in enumerate(textures):
            texturesDict[f"layer{index}"] = texture
        super().__init__(f"item/{name}", texturesDict, "item/generated")


class Block(Model):

    def __init__(self, name: str, textures: Union[dict[str, str], str], parent: str = "block/cube_all"):
        if type(textures) is str:
            textures = {"all": textures}
        super().__init__(f"block/{name}", textures, parent)
