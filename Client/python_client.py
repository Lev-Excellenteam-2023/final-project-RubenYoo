import argparse
import requests
import os
import status


class PythonClient:
    """
    This class represents the python client
    """
    def __init__(self):
        self.url = 'http://127.0.0.1:5000/'

    def send_file(self, path: str) -> str:
        """
        This function sends a file to the server
        :param path: the path of the file
        :return: the uid of the file
        """

        with open(path, 'rb') as file:
            response = requests.post(self.url, files={'file': file})

        if response.status_code == 200:
            return response.json()['uid']
        else:
            raise Exception(response.text)

    def send_uid(self, uid: str) -> status.Status:
        """
        This function sends an uid to the server
        :param uid: the uid of the file
        :return: the status of the file
        """

        response = requests.get(self.url + uid)
        my_status = status.Status(response.json())
        if response.status_code == 200 and my_status.is_done():
            return my_status
        elif response.status_code == 404 and my_status.is_not_found():
            raise Exception("UID not found")
        else:
            raise Exception("the request failed")


def main():
    """
    This function is the main function
    of the python client
    it sends a file or an uid to the server, and prints the response
    """

    parser = argparse.ArgumentParser(description="Upload a Powerpoint file, or send a UID")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-upload', metavar='<file path>', help='Upload a file')
    group.add_argument('-check', metavar='<uid>', help='Check UID')
    args = parser.parse_args()

    try:
        my_client = PythonClient()
        if args.upload:
            file_path = args.upload
            if not os.path.isfile(file_path):
                raise Exception("this file not exist")
            uid = my_client.send_file(file_path)
            print(f"The uid is {uid}")
        elif args.check:
            uid = args.check
            response = my_client.send_uid(uid)
            print(response.get_explanation())
        else:
            raise Exception("in the params")
    except Exception as e:
        print(f"Error {e}")


if __name__ == '__main__':
    main()
