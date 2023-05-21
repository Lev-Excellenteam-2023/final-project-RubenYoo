import json
import os


def sort_explanations(list_of_explanations: list) -> list:
    return sorted(list_of_explanations, key=lambda x: x[0])


def save_to_json(list_of_explanations: list, path: str) -> None:
    with open(os.path.splitext(os.path.basename(path))[0] + '.json', 'w') as f:
        json.dump(sort_explanations(list_of_explanations[1]), f)
