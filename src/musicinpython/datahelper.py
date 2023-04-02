import os
import json

_ROOT = os.path.abspath(os.path.dirname(__file__))


def get_data_folder():
    return os.path.join(_ROOT, "data")


def get_json_file(file_name: str):
    file_path = os.path.join(get_data_folder(), file_name)
    with open(file_path, "r") as file_obj:
        file_contents = json.load(file_obj)
        return file_contents
