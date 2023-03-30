import json
import os
from typing import Union, Optional


class Variant:
    model: str
    x: int
    y: int
    z: int

    def __init__(self, model: str, rotation: tuple[int, int, int] = (0, 0, 0)):
        self.model = model
        self.x = rotation[0]
        self.y = rotation[1]
        self.z = rotation[2]

    def unpack(self) -> dict[str, Union[str, int, bool]]:
        variantJson: dict[str, Union[str, int, bool]] = {"model": self.model}

        if self.x != 0:
            variantJson["x"] = self.x

        if self.y != 0:
            variantJson["y"] = self.y

        if self.z != 0:
            variantJson["z"] = self.z

        return variantJson


class Blockstate:
    textures: dict[str, str]
    variants: dict[str, Variant]
    uvLock: bool

    def __init__(self, name: str, textures: dict[str, str], variants: dict[str, Variant], uvLock = False):
        self.textures = textures
        self.variants = variants
        self.uvLock = uvLock
        self.write(name)

    def dict_build(self) -> dict[str, Union[str, int, bool]]:
        blockState: dict[str, any] = {
            "forge_marker": 1,
            "defaults": {
                "textures": self.textures
            },
            "variants": {}
        }

        if self.uvLock:
            blockState["defaults"]["uvlock"] = self.uvLock

        for key, entry in self.variants.items():
            blockState["variants"][key] = entry.unpack()

        return blockState

    def write(self, name: str):
        file = os.path.join("blockstates", name) + ".json"
        os.makedirs(os.path.dirname(file), exist_ok=True)
        with open(file, "w") as file:
            json.dump(self.dict_build(), file, indent=2)


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


STAIR_VARIANTS: dict[str, Variant] = {
    # "normal": Variant("stairs"),
    "facing=north,half=bottom,shape=straight": Variant("stairs", (0, 270, 0)),
    "facing=east,half=bottom,shape=straight": Variant("stairs"),
    "facing=west,half=bottom,shape=straight": Variant("stairs", (0, 180, 0)),
    "facing=south,half=bottom,shape=straight": Variant("stairs", (0, 90, 0)),

    "facing=north,half=bottom,shape=outer_right": Variant("outer_stairs", (0, 270, 0)),
    "facing=east,half=bottom,shape=outer_right": Variant("outer_stairs"),
    "facing=south,half=bottom,shape=outer_right": Variant("outer_stairs", (0, 90, 0)),
    "facing=west,half=bottom,shape=outer_right": Variant("outer_stairs", (0, 180, 0)),

    "facing=north,half=bottom,shape=outer_left": Variant("outer_stairs", (0, 270, 0)),
    "facing=east,half=bottom,shape=outer_left": Variant("outer_stairs", (0, 270, 0)),
    "facing=south,half=bottom,shape=outer_left": Variant("outer_stairs"),
    "facing=west,half=bottom,shape=outer_left": Variant("outer_stairs", (0, 90, 0)),

    "facing=north,half=bottom,shape=inner_right": Variant("inner_stairs", (0, 270, 0)),
    "facing=east,half=bottom,shape=inner_right": Variant("inner_stairs"),
    "facing=south,half=bottom,shape=inner_right": Variant("inner_stairs", (0, 90, 0)),
    "facing=west,half=bottom,shape=inner_right": Variant("inner_stairs", (0, 180, 0)),

    "facing=north,half=bottom,shape=inner_left": Variant("inner_stairs", (0, 180, 0)),
    "facing=east,half=bottom,shape=inner_left": Variant("inner_stairs", (0, 270, 0)),
    "facing=south,half=bottom,shape=inner_left": Variant("inner_stairs"),
    "facing=west,half=bottom,shape=inner_left": Variant("inner_stairs", (0, 90, 0)),

    "facing=north,half=top,shape=straight": Variant("stairs", (180, 270, 0)),
    "facing=east,half=top,shape=straight": Variant("stairs", (180, 0, 0)),
    "facing=south,half=top,shape=straight": Variant("stairs", (180, 90, 0)),
    "facing=west,half=top,shape=straight": Variant("stairs", (180, 180, 0)),

    "facing=north,half=top,shape=outer_right": Variant("outer_stairs", (180, 0, 0)),
    "facing=east,half=top,shape=outer_right": Variant("outer_stairs", (180, 90, 0)),
    "facing=south,half=top,shape=outer_right": Variant("outer_stairs", (180, 180, 0)),
    "facing=west,half=top,shape=outer_right": Variant("outer_stairs", (180, 270, 0)),

    "facing=north,half=top,shape=outer_left": Variant("outer_stairs", (180, 270, 0)),
    "facing=east,half=top,shape=outer_left": Variant("outer_stairs", (180, 0, 0)),
    "facing=south,half=top,shape=outer_left": Variant("outer_stairs", (180, 90, 0)),
    "facing=west,half=top,shape=outer_left": Variant("outer_stairs", (180, 180, 0)),

    "facing=north,half=top,shape=inner_right": Variant("outer_stairs", (180, 0, 0)),
    "facing=east,half=top,shape=inner_right": Variant("outer_stairs", (180, 90, 0)),
    "facing=south,half=top,shape=inner_right": Variant("outer_stairs", (180, 180, 0)),
    "facing=west,half=top,shape=inner_right": Variant("outer_stairs", (180, 270, 0)),

    "facing=north,half=top,shape=inner_left": Variant("outer_stairs", (180, 270, 0)),
    "facing=east,half=top,shape=inner_left": Variant("outer_stairs", (180, 0, 0)),
    "facing=south,half=top,shape=inner_left": Variant("outer_stairs", (180, 90, 0)),
    "facing=west,half=top,shape=inner_left": Variant("outer_stairs", (180, 180, 0)),
}


class Stairs(Blockstate):

    def __init__(self, name: str, textures: Union[dict[str, str], str]):
        if type(textures) is str:
            textures = {"top": textures, "bottom": textures, "side": textures}
        super().__init__(name, textures, STAIR_VARIANTS, True)


if __name__ == "__main__":
    os.chdir("test")
    Blockstate("test_blockstate", {"top": "blocks/test",
                                   "bottom": "blocks/test",
                                   "side": "blocks/test"}, STAIR_VARIANTS, True)
    Stairs("test_stairs", "blocks/test")
    Model("test_model", {"test": "blocks/test"}, "block/cube_all")
    Item("test_item", "items/test")
    Block("test_block", "blocks/test")
