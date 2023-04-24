from typing import Union, Optional

from .BlockstateVariants import Variant, STAIR_VARIANTS, SLAB_VARIANTS
from .Util import writeDictToJson


def createBlockState(name: str, textures: Optional[dict[str, str]], variants: dict[str, Variant], uvLock = False):
    blockState: dict = {}

    if textures:
        blockState["forge_marker"] = 1
        blockState["defaults"] = {"textures": textures}

    blockState["variants"] = {}

    if uvLock:
        blockState["defaults"]["uvlock"] = uvLock

    for key, entry in variants.items():
        blockState["variants"][key] = entry.unpack()

    writeDictToJson(f"blockstates/{name}", blockState)


def createCubeAll(name: str, texture: str):
    createBlockState(name, {"all": texture}, {"normal": Variant("cube_all")})


def createStairs(name: str, textures: Union[dict[str, str], str]):
    if type(textures) is str:
        textures = {"top": textures, "bottom": textures, "side": textures}
    createBlockState(name, textures, STAIR_VARIANTS, True)


def createSlab(name: str, texture: str):
    createBlockState(f"double_slab/{name}", {"all": texture}, {"normal": Variant("cube_all")})
    texture = {"top": texture, "bottom": texture, "side": texture}
    createBlockState(f"slab/{name}", texture, SLAB_VARIANTS)
