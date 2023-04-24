import json
import os


def writeDictToJson(name: str, temp: dict):
    filePath = os.path.join(name) + ".json"
    os.makedirs(os.path.dirname(filePath), exist_ok=True)
    with open(filePath, "w") as file:
        json.dump(temp, file, indent=2)
