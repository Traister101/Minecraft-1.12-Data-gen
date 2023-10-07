from .Util import writeDictToJson


def create(name: str, textures: dict[str, str], parent: str) -> None:
    """
    :param name: Name of the model.
    :param textures: Dict of textures, keys must be the same as the parent!
    :param parent: Parent model
    """
    writeDictToJson(f"models/{name}", {"parent": parent, "textures": textures})


def createItem(name: str, *textures: list[str] | str) -> None:
    """
    Creates a basic item
    :param name: Name of the item model.
    :param textures: A single texture or a list of textures. List will require custom model registration code!
    """
    texturesDict: dict[str, str] = {}
    for index, texture in enumerate(textures):
        texturesDict[f"layer{index}"] = texture
    create(f"item/{name}", texturesDict, "item/generated")


def createBlock(name: str, textures: dict[str, str], parent: str) -> None:
    """
    :param name: Name of the block model.
    :param textures: Dict of textures, keys must be the same as the parent!
    :param parent: Parent model
    """
    create(f"block/{name}", textures, parent)


def createCubeAll(name: str, texture: str) -> None:
    """
    Helper to create a six sided single texture cube model.
    :param name: Name of the block model.
    :param texture: Texture the model should use.
    """
    createBlock(name, {"all": texture}, "block/cube_all")
