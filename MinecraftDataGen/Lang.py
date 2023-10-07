import os
from typing import TextIO


class Lang:
    """
    Helper class to wrap fileIO with a lang file
    """
    file: TextIO

    def __init__(self, local: str) -> None:
        """
        :param local: The lang local to write
        """
        os.makedirs(os.path.dirname(f"lang/{local}.lang"), exist_ok=True)
        self.file = open(f"lang/{local}.lang", "w")

    def writeHeader(self, header: str) -> None:
        """
        Writes the header string as <## header> with a newline
        :param header: Header string to write to the lang
        """
        self.file.write(f"## {header}\n")

    def writeComment(self, comment: str) -> None:
        """
        Writes a comment string as <# comment> with a newline
        :param comment: Comment string to write to the lang
        """
        self.file.write(f"# {comment}\n")

    def write(self, key: str, localization: str) -> None:
        """
        Writes a lang key, and it's localization for this local. Writes a newline
        :param key: A string lang key
        :param localization: The string localization for this entry
        """
        self.file.write(f"{key}={localization}\n")

    def writeTile(self, registryName: str, localization: str) -> None:
        """
        Shorthand for a key being tile.<registryName>.name
        :param registryName: A string registry key for a tile
        :param localization: The string localization for this entry
        """
        self.write(f"tile.{registryName}.name", localization)

    def writeItem(self, registryName: str, localization: str) -> None:
        """
        Shorthand for a key being item.<registryName>.name
        :param registryName: A string registry key for a tile
        :param localization: The string localization for this entry
        """
        self.write(f"item.{registryName}.name", localization)

    def writeEntity(self, registeryName: str, localization: str) -> None:
        """
        Shorthand for a key being entity.<registryName>.name
        :param registeryName: A string registry key for an entity
        :param localization: The string localization for this entry
        """
        self.write(f"entity.{registeryName}.name", localization)

    def newLine(self) -> None:
        """
        Writes a single new line
        """
        self.file.write("\n")
