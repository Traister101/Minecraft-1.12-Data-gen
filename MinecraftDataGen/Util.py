import json
import os


def writeDictToJson(path: str, jsonData: dict) -> None:
    """
    Writes a dictionary to a json file.
    :param path: Path of the file, not including extension.
    :param jsonData: The dictionary to write as json
    """
    filePath = os.path.join(path) + ".json"
    os.makedirs(os.path.dirname(filePath), exist_ok=True)
    with open(filePath, "w") as file:
        json.dump(jsonData, file, indent=2)
