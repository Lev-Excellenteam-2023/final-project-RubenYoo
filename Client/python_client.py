import argparse
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
    parser = argparse.ArgumentParser(description="Upload a Powerpoint file, or send a UID")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-upload', metavar='<file path>', help='Upload a file')
    group.add_argument('-check', metavar='<uid>', help='Check UID')
    args = parser.parse_args()

    try:
        if args.upload:
            file_path = args.upload
            if not os.path.isfile(file_path):
                raise Exception("this file not exist")
            uid = send_file(file_path)
            print(f"The uid is {uid}")
        elif args.check:
            uid = args.check
            response = send_uid(uid)
            print(response.get_explanation())
        else:
            raise Exception("in the params")
    except Exception as e:
        print(f"Error {e}")


if __name__ == '__main__':
    main()
