import subprocess


def test_system():
    subprocess.run(["python", "../Web_api/app.py"])
    subprocess.run(["python", "../Gpt_explainer/main.py"])
