from typing import Optional, Union

from .Util import writeDictToJson


class Ingredient:
    """
    Class defining what a recipe ingredient is
    """
    itemID: Optional[str]
    itemMeta: int
    ore: Optional[str]

    def __init__(self, /, *, itemID: str = None, itemMeta = 0, ore: str = None):
        """
        :param itemID: Registry key of the item including mod ID
        :param itemMeta: Metadata of the item, not applicable for ores
        :param ore: A Forge dictionary key
        """
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


RecipePattern = list[str]
"""
3 strings each representing 3 slots using a letter or space for air
"""


class Result:
    """
    A class defining a recipe output
    """
    itemID: str
    count: int
    metaData: int
    hasSubtypes: bool

    def __init__(self, itemID: str, count = 1, metaData = 0, hasSubtypes = False):
        """
        :param itemID: Registry key of an item including mod ID
        :param count: The output stack size
        :param metaData: The metadata of the item result
        :param hasSubtypes: If this result needs the metadata attribute
        """
        self.itemID = itemID
        if count < 1:
            raise ValueError("Count can't be less than 1")

        self.count = count
        self.metaData = metaData
        self.hasSubtypes = hasSubtypes

    def build(self) -> dict[str, Union[str, int]]:
        recipeResult = {"item": self.itemID}

        if self.count > 1:
            recipeResult["count"] = self.count

        if self.metaData > 0 or self.hasSubtypes:
            recipeResult["data"] = self.metaData

        return recipeResult


def recipeAdvanced(name: str, recipeType: str, pattern: RecipePattern, ingredients: dict[str, Ingredient],
                   result: Result):
    recipe: dict = {"type": recipeType}

    if pattern:
        recipe["pattern"] = pattern

    recipe["key"] = {}

    for key, ingredient in ingredients.items():
        recipe["key"][key] = ingredient.build()

    recipe["result"] = result.build()

    writeDictToJson(f"recipes/{name}", recipe)


def createShaped(name: str, pattern: RecipePattern, ingredients: dict[str, Ingredient], result: Result):
    recipeAdvanced(name, "minecraft:crafting_shaped", pattern, ingredients, result)


def shapelessRecipe(name: str, ingredients: list[Ingredient], result: Result):
    recipe = {"type": "minecraft:crafting_shapeless"}

    for ingredient in ingredients:
        recipe["ingredients"] = ingredient.build()

    recipe["result"] = result.build()
    writeDictToJson(f"recipes/{name}", recipe)


def createSlab(name: str, parentItem: str, slabItem: str):
    createShaped(name, ["XXX"], {"X": Ingredient(itemID=parentItem)}, Result(slabItem, 6, 0, True))


def createStairs(name: str, parentItem: str, stairsItem: str):
    createShaped(name, ["X  ", "XX ", "XXX"], {"X": Ingredient(itemID=parentItem)}, Result(stairsItem, 6, 0))
