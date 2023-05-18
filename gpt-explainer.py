from dotenv import load_dotenv
import os
import openai

load_dotenv()
TOKEN = os.getenv('OPENAI_TOKEN')
TIMEOUT = 15


class GptExplainer:
    def __init__(self) -> None:
        openai.api_key = TOKEN
        self.model = "gpt-3.5-turbo"
        self.gpt_context = [
            {"role": "system",
             "content":
             "You are a lecturer, that take in input the text of a powerpoint presentation slide, and you need "
             "to explain it"},
        ]
        self.explanations_slides = []

    def send_slide_text_to_gpt(self, slide_number: int, text_of_slide: str) -> None:

        self.gpt_context.append({"role": "user", "content": text_of_slide})

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.gpt_context,
            timeout=TIMEOUT
        )

        if 'choices' in response and len(response.choices) > 0:
            self.gpt_context.append({"role": "assistant", "content": response})
            self.explanations_slides += [(slide_number, response.choices[0].message.content.strip())]
        else:
            self.explanations_slides += [(slide_number, "")]


