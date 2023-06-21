import subprocess

import unittest


class MyTestCase(unittest.TestCase):
    def test_system(self):
        self.file_path = "../asyncio-intro.pptx"

        self.script_args = [
            '../Web_api/app.py',
            '../Gpt_explainer/main.py',
            ('../Client/python_client.py', '-upload', f'{self.file_path}'),
            ('../Client/python_client.py', '-check', f'{self.file_path}')
        ]

        self.processes = []

        for script, *args in self.script_args[:2]:
            command = ['python', script] + list(args)
            process = subprocess.Popen(command)
            self.processes.append(process)

        for process in self.processes:
            process.wait()


def main():
    system_test = MyTestCase()
    system_test.test_system()


if __name__ == '__main__':
    unittest.main()
