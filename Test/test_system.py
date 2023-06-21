import subprocess

import unittest


class MyTestCase(unittest.TestCase):
    def test_system(self):
        self.scripts = ['../Web_api/app.py', '../Gpt_explainer/main.py', '../Client/python_client.py']
        script_args = [
            '../Web_api/app.py',
            '../Gpt_explainer/main.py',
            ('../Client/python_client.py', 'arg5', 'arg6')
        ]
        self.processes = []

        for script, *args in script_args:
            command = ['python', script] + list(args)
            process = subprocess.Popen(command)
            self.processes.append(process)

        for process in self.processes:
            process.wait()


def main():
    pass


if __name__ == '__main__':
    unittest.main()
