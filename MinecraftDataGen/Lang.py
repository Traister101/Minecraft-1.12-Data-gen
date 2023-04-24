import os
from typing import TextIO


class Lang:
    """
    Helper class to wrap fileIO with a lang file
    """
    file: TextIO

    def __init__(self, local: str):
        """
        :param local: The lang local to write
        """
        os.makedirs(os.path.dirname(f"lang/{local}.lang"), exist_ok=True)
        self.file = open(f"lang/{local}.lang", "w")

    def writeHeader(self, header: str):
        """
        Writes the header string as <## header> with a newline
        :param header: Header string to write to the lang
        """
        self.file.write(f"## {header}\n")

    def writeComment(self, comment: str):
        """
        Writes a comment string as <# comment> with a newline
        :param comment: Comment string to write to the lang
        """
        self.file.write(f"# {comment}\n")

    def writeLocalization(self, key: str, localization: str):
        """
        Writes a lang key, and it's localization for this local. Writes a newline
        :param key: A string lang key
        :param localization: The string localization for this entry
        """
        self.file.write(f"{key}={localization}\n")

    def writeTile(self, registryName: str, localization: str):
        """
        Shorthand for a key being tile.<registryName>.name
        :param registryName: A string registry key for a tile
        :param localization: The string localization for this entry
        """
        self.writeLocalization(f"tile.{registryName}.name", localization)

    def writeItem(self, registryName: str, localization: str):
        """
        Shorthand for a key being item.<registryName>.name
        :param registryName: A string registry key for a tile
        :param localization: The string localization for this entry
        """
        self.writeLocalization(f"item.{registryName}.name", localization)

    def newLine(self):
        """
        Writes a single new line
        """
        self.file.write("\n")
