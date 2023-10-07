from .Util import writeDictToJson


def createBlockStateBasic(name: str, variants: dict) -> None:
    """
    :param name: Name of the blockstate.
    :param variants: The blockstate variants
    """
    writeDictToJson(f"blockstates/{name}", {"variants": variants})


def createBlockStateSimple(name: str, modelLocation: str | list[str]) -> None:
    """
    A simple blockstate, only has the normal variant
    :param name: Name of the blockstate.
    :param modelLocation: Resource location for the model/s.
    """
    variants: dict = {"normal": None}
    if type(modelLocation) is str:
        variants["normal"] = {"model": modelLocation}
    else:
        variants["normal"] = []
        for model in modelLocation:
            variants["normal"].append({"model": model})
    createBlockStateBasic(name, variants)
