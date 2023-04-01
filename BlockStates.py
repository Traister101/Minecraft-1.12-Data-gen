from typing import Union, Optional

from BlockstateVariants import STAIR_VARIANTS, SLAB_VARIANTS, Variant


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
        filePath = os.path.join("blockstates", name) + ".json"
        os.makedirs(os.path.dirname(filePath), exist_ok=True)
        with open(filePath, "w") as file:
            json.dump(self.dict_build(), file, indent=2)


class CubeAll(Blockstate):

    def __init__(self, name: str, texture: str):
        super().__init__(name, {"all": texture}, {"normal": Variant("cube_all")})


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

    def __init__(self, name: str, texture: str):
        """
        Creates Blockstates for Half slab and a full Block slab.
        Expects only the "half=bottom" and "half=top" variants, may need a custom state mapping on Java end

        :param name: For the file including relative path from /blockstates/<slab | double_slab>/
        :param texture: Either a dict of <key>:<texture> pairs or a single string which is applied to the top, bottom and side
        """
        Blockstate(f"double_slab/{name}", {"all": texture}, {"normal": Variant("cube_all")})
        texture = {"top": texture, "bottom": texture, "side": texture}
        super().__init__(f"slab/{name}", texture, SLAB_VARIANTS)
