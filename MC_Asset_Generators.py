import json
import os
from typing import Union, Optional, Any, Dict


class Variant:
    """
    A class containing a model, and any extra transformations applied as a tuple used for easily creating a Blockstate
    """
    model: str
    x: int
    y: int
    z: int

    def __init__(self, model: str, rotation: tuple[int, int, int] = (0, 0, 0)):
        """
        :param model: The model this variant applies
        :param rotation: The model rotations this variant should apply as a tuple (x, y, z)
        """
        self.model = model
        self.x = rotation[0]
        self.y = rotation[1]
        self.z = rotation[2]

    def unpack(self) -> dict[str, Union[str, int, bool]]:
        """
        :return: The dictionary representation of the variant used for Json output
        """
        variantJson: dict[str, Union[str, int, bool]] = {"model": self.model}

        if self.x != 0:
            variantJson["x"] = self.x

        if self.y != 0:
            variantJson["y"] = self.y

        if self.z != 0:
            variantJson["z"] = self.z

        return variantJson


class Blockstate:
    """
    A class defining what a blockstate contains. Automatically writes the file after construction
    """
    textures: dict[str, str]
    variants: dict[str, Variant]
    uvLock: bool

    def __init__(self, name: str, textures: Optional[dict[str, str]], variants: dict[str, Variant], uvLock = False):
        """
        Mommy blockstate, generates a blockstate file with the passed in textures and variants

        :param name: The file name/path from the blockstates folder
        :param textures: A dictionary of textures <key>:<texture> or None (for model applied textures)
        :param variants: A dictionary of the variants, <key>:<Variant> pairs
        """
        self.textures = textures
        self.variants = variants
        self.uvLock = uvLock
        self.write(name)

    def dict_build(self) -> dict[str, Any]:
        """
        Builds the dictionary representation of the Blockstate, used in writing the Json output
        :return: Dictionary representation of the Blockstate
        """

        # Initialize as an empty dict, so we don't force Forge Blockstates
        blockState: dict = {}

        if self.textures:
            blockState["forge_marker"] = 1
            blockState["defaults"] = {"textures": self.textures}

        blockState["variants"] = {}

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

SLAB_VARIANTS: dict[str, Variant] = {
    "half=bottom": Variant("half_slab"),
    "half=top": Variant("upper_slab")
}


class Stairs(Blockstate):
    """
    A class for simple Stair Blockstates
    """

    def __init__(self, name: str, textures: Union[dict[str, str], str]):
        """
        :param name: Name for the file including relative path from /blockstates/
        :param textures: Either a dict of <key>:<texture> pairs or a single string which is applied to the top, bottom and side
        """
        if type(textures) is str:
            textures = {"top": textures, "bottom": textures, "side": textures}
        super().__init__(name, textures, STAIR_VARIANTS, True)


class Slab(Blockstate):
    """
    A class for simple Slab Blockstates
    """

    def __init__(self, name: str, textures: Union[dict[str, str], str], fullBlockModel: str):
        """
        Creates Blockstates for Half slab and a full Block slab.
        Expects only the "half=bottom" and "half=top" variants, may need a custom state mapping on Java end

        :param name: For the file including relative path from /blockstates/<slab | double_slab>/
        :param textures: Either a dict of <key>:<texture> pairs or a single string which is applied to the top, bottom and side
        :param fullBlockModel: Path to the model that should be used for the full block slab
        """
        if type(textures) is str:
            textures = {"top": textures, "bottom": textures, "side": textures}
        super().__init__(f"slab/{name}", textures, SLAB_VARIANTS)
        Blockstate(f"double_slab/{name}", None, {"normal": Variant(fullBlockModel)})


class Ingredient:
    itemID: Optional[str]
    itemMeta: int
    ore: Optional[str]

    def __init__(self, /, *, itemID: str = None, itemMeta = 0, ore: str = None):
        self.itemID = itemID
        self.itemMeta = itemMeta
        self.ore = ore

    def build(self) -> dict:
        if self.ore:
            return {"type": "forge:ore_dict",
                    "ore": self.ore}

        itemIngredient = {"item": self.itemID}

        if self.itemMeta > 0:
            itemIngredient["data"] = self.itemMeta
        return itemIngredient


Pattern = list[str, str, str]
"""
A list of 3 strings which each contain 3 "slots"
"""


class Result:
    itemID: str
    count: int
    metaData: int

    def __init__(self, itemID: str, count = 1, metaData = 0):
        self.itemID = itemID
        if count < 1:
            raise ValueError("Count can't be less than 1")

        self.count = count
        self.metaData = metaData

    def build(self) -> dict[str, Union[str, int]]:
        recipeResult = {"item": self.itemID}

        if self.count > 1:
            recipeResult["count"] = self.count

        if self.metaData > 0:
            recipeResult["data"] = self.metaData

        return recipeResult


class ShapedRecipe:
    pattern: Pattern
    ingredients: dict[str, Ingredient]
    result: Result

    def __init__(self, name: str, pattern: Pattern, ingredients: dict[str, Ingredient], result: Result):
        """
        :param name: Of this recipe
        :param pattern: The recipe pattern
        :param ingredients: A <key>:<ingredient> pair
        :param result: The recipe output
        """
        self.pattern = pattern
        self.ingredients = ingredients
        self.result = result
        self.write(name)

    def build(self) -> dict:
        recipe: dict = {"type": "minecraft:crafting_shaped"}

        if self.pattern:
            recipe["pattern"] = self.pattern

        recipe["key"] = {}

        for key, ingredient in self.ingredients.items():
            recipe["key"][key] = ingredient.build()

        recipe["result"] = self.result.build()

        return recipe

    def write(self, name: str):
        file = os.path.join("recipes", name) + ".json"
        os.makedirs(os.path.dirname(file), exist_ok=True)
        with open(file, "w") as file:
            json.dump(self.build(), file, indent=2)


class ShapelessRecipe:
    ingredients: list[Ingredient]

    def __init__(self, name: str, ingredients: list[Ingredient], result: Result):
        self.ingredients = ingredients
        self.result = result
        self.write(name)

    def build(self) -> dict[str]:
        recipe = {"type": "minecraft:crafting_shapeless"}

        for ingredient in self.ingredients:
            recipe["ingredients"] = ingredient.build()

        recipe["result"] = self.result.build()

        return recipe

    def write(self, name: str):
        file = os.path.join("recipes", name) + ".json"
        os.makedirs(os.path.dirname(file), exist_ok=True)
        with open(file, "w") as file:
            json.dump(self.build(), file, indent=2)


if __name__ == "__main__":
    print("This is meant to be imported, running it as a script will do tests")

    os.chdir("test")
    Blockstate("test_blockstate", {"top": "blocks/test",
                                   "bottom": "blocks/test",
                                   "side": "blocks/test"}, STAIR_VARIANTS, True)
    Stairs("test_stairs", "blocks/test")
    Model("test_model", {"test": "blocks/test"}, "block/cube_all")
    Item("test_item", "items/test")
    Block("test_block", "blocks/test")
    Slab("test", "blocks/test", "test_block")

    ShapedRecipe("test_shaped", [" I ", " I ", " S "],
                 {"I": Ingredient(itemID="iron_ingot"), "S": Ingredient(ore="stick")},
                 Result("id:test"))

    ShapelessRecipe("test_shapeless", [Ingredient(itemID="id:test")], Result("id:test"))
