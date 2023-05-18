from dotenv import load_dotenv
import os
import openai


class GptExplainer:
    def __init__(self):
        load_dotenv()
        openai.api_key = os.getenv('OPENAI_TOKEN')
        self.model = "gpt-3.5-turbo"
        self.gpt_context = [
            {"role": "system",
             "content":
             "You are a lecturer, that take in input the text of a powerpoint presentation slide, and you need "
             "to explain it"},
        ]



