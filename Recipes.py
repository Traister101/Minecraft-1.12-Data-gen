import json
import os
from typing import Optional, Union


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

    def __init__(self, itemID: str, count = 1, metaData = 0):
        """
        :param itemID: Registry key of an item including mod ID
        :param count: The output stack size
        :param metaData: The metadata of the item result
        """
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


class Recipe:
    recipeType: str
    pattern: RecipePattern
    ingredients: dict[str, Ingredient]
    result: Result

    def __init__(self, name: str, recipeType: str, pattern: RecipePattern, ingredients: dict[str, Ingredient],
                 result: Result):
        """
        :param name: Name of this recipe
        :param recipeType: Type of this recipe
        :param pattern: The recipe pattern
        :param ingredients: A <key>:<ingredient> pair
        :param result: The recipe output
        """
        self.recipeType = recipeType
        self.pattern = pattern
        self.ingredients = ingredients
        self.result = result
        self.write(name)

    def build(self) -> dict:
        recipe: dict = {"type": self.recipeType}

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


class ShapedRecipe(Recipe):

    def __init__(self, name: str, pattern: RecipePattern, ingredients: dict[str, Ingredient], result: Result):
        super().__init__(name, "minecraft:crafting_shaped", pattern, ingredients, result)


class ShapelessRecipe:
    ingredients: list[Ingredient]
    result: Result

    def __init__(self, name: str, ingredients: list[Ingredient], result: Result):
        """
        :param name: Name of this recipe
        :param ingredients: A list of the ingredients
        :param result: The recipe output
        """
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


class SlabRecipe(ShapedRecipe):

    def __init__(self, name: str, parentItem: str, slabItem: str):
        """
        :param name: The name of this recipe
        :param parentItem: The parent item which is used for the slab recipe
        :param slabItem: The item used for the resulting slab output
        """
        super().__init__(name, ["XXX"], {"X": Ingredient(itemID=parentItem)}, Result(slabItem, 6, 0))


class StairsRecipe(ShapedRecipe):

    def __init__(self, name: str, parentItem: str, stairsItem: str):
        """
        :param name: The name of this recipe
        :param parentItem: The parent item which is used for the stairs recipe
        :param stairsItem: The item used for the resulting stairs output
        """
        super().__init__(name, ["X  ", "XX ", "XXX"], {"X": Ingredient(itemID=parentItem)}, Result(stairsItem, 6, 0))
