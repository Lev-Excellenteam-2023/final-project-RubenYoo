import json
import os


def sort_explanations(list_of_explanations: list) -> list:
    sorted_list = sorted(list_of_explanations, key=lambda x: x[0])
    return [slide_explanation[1] for slide_explanation in sorted_list]


def save_to_json(list_of_explanations: list, path: str) -> None:
    with open(os.path.splitext(os.path.basename(path))[0] + '.json', 'w') as my_file:
        json.dump(sort_explanations(list_of_explanations), my_file)
