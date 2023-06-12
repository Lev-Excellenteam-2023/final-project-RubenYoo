import requests
import os
import json

URL = 'http://127.0.0.1:5000/'


def send_file(path):
    with open(path, 'rb') as file:
        response = requests.post(URL, files={'file': file})

    if response.status_code == 200:
        return response.json()['uid']


def main():
    file_path = input("Enter the PowerPoint file path\n")
    if os.path.exists(file_path):
        send_file(file_path)
    else:
        print("this file not exist")
        exit()


if __name__ == '__main__':
    main()
