from typing import Type
import requests
import os
from status import Status

URL = 'http://127.0.0.1:5000/'


def send_file(path: str) -> str:
    with open(path, 'rb') as file:
        response = requests.post(URL, files={'file': file})

    if response.status_code == 200:
        return response.json()['uid']
    else:
        raise Exception(response.text)


def send_uid(uid: str) -> Status:
    response = requests.get(URL + uid)
    my_status = Status(response.json())
    if response.status_code == 200 and my_status.is_done():
        return my_status
    elif response.status_code == 404 and my_status.is_not_found():
        raise Exception("UID not found")
    else:
        raise Exception("the request failed")


def main():
    print("Welcome to the GTP-Explainer client")

    while True:
        choice = input("Do you want to upload a PowerPoint file or enter a uid? (1/2)\n")
        try:
            match choice:
                case '0':
                    return
                case '1':
                    file_path = input("Enter the PowerPoint file path\n")
                    if not os.path.isfile(file_path):
                        raise Exception("this file not exist")
                    uid = send_file(file_path)
                    print(f"The uid is {uid}")
                case '2':
                    uid = input("Enter the uid\n")
                    response = send_uid(uid)
                    print(response.get_explanation())
        except Exception as e:
            print(f"Error {e}")


if __name__ == '__main__':
    main()
