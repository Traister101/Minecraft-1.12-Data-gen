from typing import Union, Final


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


STAIR_VARIANTS: Final[dict[str, Variant]] = {
    "normal": Variant("stairs"),
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
"""
All the stair variants
"""

SLAB_VARIANTS: Final[dict[str, Variant]] = {
    "normal": Variant("half_slab"),
    "half=bottom": Variant("half_slab"),
    "half=top": Variant("upper_slab")
}
"""
All the slab variants
"""

DOOR_VARIANTS: Final[dict[str, Variant]] = {
    "facing=east,half=lower,hinge=left,open=false": Variant("door_bottom"),
    "facing=south,half=lower,hinge=left,open=false": Variant("door_bottom", (0, 90, 0)),
    "facing=west,half=lower,hinge=left,open=false": Variant("door_bottom", (0, 180, 0)),
    "facing=north,half=lower,hinge=left,open=false": Variant("door_bottom", (0, 270, 0)),
    "facing=east,half=lower,hinge=right,open=false": {"model": "acacia_door_bottom_rh"},
    "facing=south,half=lower,hinge=right,open=false": {"model": "acacia_door_bottom_rh", "y": 90},
    "facing=west,half=lower,hinge=right,open=false": {"model": "acacia_door_bottom_rh", "y": 180},
    "facing=north,half=lower,hinge=right,open=false": {"model": "acacia_door_bottom_rh", "y": 270},
    "facing=east,half=lower,hinge=left,open=true": {"model": "acacia_door_bottom_rh", "y": 90},
    "facing=south,half=lower,hinge=left,open=true": {"model": "acacia_door_bottom_rh", "y": 180},
    "facing=west,half=lower,hinge=left,open=true": {"model": "acacia_door_bottom_rh", "y": 270},
    "facing=north,half=lower,hinge=left,open=true": {"model": "acacia_door_bottom_rh"},
    "facing=east,half=lower,hinge=right,open=true": {"model": "acacia_door_bottom", "y": 270},
    "facing=south,half=lower,hinge=right,open=true": {"model": "acacia_door_bottom"},
    "facing=west,half=lower,hinge=right,open=true": {"model": "acacia_door_bottom", "y": 90},
    "facing=north,half=lower,hinge=right,open=true": {"model": "acacia_door_bottom", "y": 180},
    "facing=east,half=upper,hinge=left,open=false": {"model": "acacia_door_top"},
    "facing=south,half=upper,hinge=left,open=false": {"model": "acacia_door_top", "y": 90},
    "facing=west,half=upper,hinge=left,open=false": {"model": "acacia_door_top", "y": 180},
    "facing=north,half=upper,hinge=left,open=false": {"model": "acacia_door_top", "y": 270},
    "facing=east,half=upper,hinge=right,open=false": {"model": "acacia_door_top_rh"},
    "facing=south,half=upper,hinge=right,open=false": {"model": "acacia_door_top_rh", "y": 90},
    "facing=west,half=upper,hinge=right,open=false": {"model": "acacia_door_top_rh", "y": 180},
    "facing=north,half=upper,hinge=right,open=false": {"model": "acacia_door_top_rh", "y": 270},
    "facing=east,half=upper,hinge=left,open=true": {"model": "acacia_door_top_rh", "y": 90},
    "facing=south,half=upper,hinge=left,open=true": {"model": "acacia_door_top_rh", "y": 180},
    "facing=west,half=upper,hinge=left,open=true": {"model": "acacia_door_top_rh", "y": 270},
    "facing=north,half=upper,hinge=left,open=true": {"model": "acacia_door_top_rh"},
    "facing=east,half=upper,hinge=right,open=true": {"model": "acacia_door_top", "y": 270},
    "facing=south,half=upper,hinge=right,open=true": {"model": "acacia_door_top"},
    "facing=west,half=upper,hinge=right,open=true": {"model": "acacia_door_top", "y": 90},
    "facing=north,half=upper,hinge=right,open=true": {"model": "acacia_door_top", "y": 180}
}
"""
All the door variants
"""
