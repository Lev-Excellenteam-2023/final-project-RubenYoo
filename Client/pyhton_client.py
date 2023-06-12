import requests
import os

URL = 'http://127.0.0.1:5000/'


def send_file(path):
    with open(path, 'rb') as file:
        response = requests.post(URL, files={'file': file})

    if response.status_code == 200:
        return response.json()['uid']
    else:
        raise Exception(response.text)


def main():
    file_path = input("Enter the PowerPoint file path\n")

    if not os.path.exists(file_path):
        print("this file not exist")
        exit()

    try:
        rep = send_file(file_path)
    except Exception as e:
        print(f"Error {e}")


if __name__ == '__main__':
    main()
