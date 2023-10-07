from typing import Union

from .Util import writeDictToJson


class Ingredient:
    """
    Class defining what a recipe ingredient is
    """
    itemID: str | None
    itemMeta: int | None
    ore: str | None

    def __init__(self, /, *, itemID: str = None, itemMeta: int = None, ore: str = None):
        """
        :param itemID: Registry key of the item.
        :param itemMeta: Metadata of the item, not applicable for ores.
        :param ore: A Forge dictionary key.
        """
        self.itemID = itemID
        self.itemMeta = itemMeta
        self.ore = ore

    def build(self) -> dict:
        if self.ore:
            return {"type": "forge:ore_dict",
                    "ore": self.ore}

        itemIngredient = {"item": self.itemID}

        if self.itemMeta:
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
    metaData: int | None

    def __init__(self, itemRegistryKey: str, count=1, metaData: int = None):
        """
        :param itemRegistryKey: Registry key of an item
        :param count: The output stack size
        :param metaData: The metadata of the item result
        """
        self.itemID = itemRegistryKey
        if count < 1:
            raise ValueError("Count can't be less than 1")

        self.count = count
        self.metaData = metaData

    def build(self) -> dict[str, Union[str, int]]:
        recipeResult = {"item": self.itemID}

        if self.count > 1:
            recipeResult["count"] = self.count

        if self.metaData:
            recipeResult["data"] = self.metaData

        return recipeResult


def createRecipeAdvanced(name: str, recipeType: str, pattern: RecipePattern, ingredients: dict[str, Ingredient],
                         result: Result) -> None:
    """
    :param name: Name of the recipe.
    :param recipeType: The recipe type.
    :param pattern: Recipe pattern.
    :param ingredients: Recipe ingredients, key ingredient pair.
    :param result: The recipe result.
    """
    recipe: dict = {"type": recipeType}

    if pattern:
        recipe["pattern"] = pattern

    recipe["key"] = {}

    for ingredientKey, ingredient in ingredients.items():
        recipe["key"][ingredientKey] = ingredient.build()

    recipe["result"] = result.build()

    writeDictToJson(f"recipes/{name}", recipe)


def createShaped(name: str, pattern: RecipePattern, ingredients: dict[str, Ingredient], result: Result) -> None:
    """
    :param name: Name of the recipe.
    :param pattern: Recipe pattern.
    :param ingredients:  Recipe ingredients, key ingredient pair.
    :param result: The recipe result.
    """
    createRecipeAdvanced(name, "minecraft:crafting_shaped", pattern, ingredients, result)


def createShapelessRecipe(name: str, ingredients: list[Ingredient], result: Result) -> None:
    """
    :param name: Name of the recipe.
    :param ingredients: List of ingredients, can have a single entry.
    :param result: Result of the recipe.
    """
    recipe = {"type": "minecraft:crafting_shapeless", "ingredients": []}
    for ingredient in ingredients:
        recipe["ingredients"].append(ingredient.build())

    recipe["result"] = result.build()
    writeDictToJson(f"recipes/{name}", recipe)
