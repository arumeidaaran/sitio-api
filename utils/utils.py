from json import load
from pathlib import Path


def read_json_file(json_file_path: Path | str) -> object:
    with open(json_file_path, 'r', encoding='utf8') as json_file:
        return load(json_file)
