import subprocess
import unittest
import time
import Client


class MyTestCase(unittest.TestCase):
    def test_system(self):
        """
        This function tests the system
        """

        self.file_path = "../asyncio-intro.pptx"

        self.scripts = ['../Web_api/app.py', '../Gpt_explainer/main.py']

        self.processes = []

        for script in self.scripts:
            process = subprocess.Popen(['python', script])
            self.processes.append(process)

        time.sleep(5)
        my_client = Client.python_client.PythonClient()
        uid = my_client.send_file(self.file_path)
        time.sleep(10)
        my_status = Client.status.Status(my_client.send_uid(uid))

        print(my_status)

        for process in self.processes:
            process.kill()


def main():
    system_test = MyTestCase()
    system_test.test_system()


if __name__ == '__main__':
    unittest.main()
