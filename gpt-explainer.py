from dotenv import load_dotenv
import os
import openai
import asyncio

# Load the environment variables
load_dotenv()
TOKEN = os.getenv('OPENAI_TOKEN')

# Set the timeout for the gpt-3.5-turbo model
TIMEOUT = 15


class GptExplainer:
    """
    This class is used to explain the slides of a PowerPoint presentation based on the gpt-3.5-turbo model.
    """
    def __init__(self) -> None:
        """
        Initialize the class
        """
        self.model: str
        self.gpt_context: list
        self.explanations_slides: list

        # Setting the context of the gpt-3.5-turbo model
        openai.api_key = TOKEN
        self.model = "gpt-3.5-turbo"
        self.gpt_context = [
            {"role": "system",
             "content":
             "You are a lecturer, that take in input the text of a powerpoint presentation slide, and you need "
             "to explain it"},
        ]

        # Saving the explanations of the slides
        self.explanations_slides = []

    async def send_slide_text_to_gpt(self, slide_number: int, text_of_slide: str) -> None:
        """
        This method sends the text of a slide to the gpt-3.5-turbo model and saves the response in the
        explanations_slides list.
        :param slide_number: the number of the slide
        :param text_of_slide: the text of the slide
        :return: None
        """

        # Setting the slide text as the user input
        self.gpt_context.append({"role": "user", "content": text_of_slide})

        # Generate a response from the model
        response = await asyncio.to_thread(openai.ChatCompletion.create(
            model=self.model,
            messages=self.gpt_context,
            timeout=TIMEOUT
        ))

        # If the response is not empty, save it in the explanations_slides list
        # and append it to the gpt_context for more context for the other slides
        if 'choices' in response and len(response.choices) > 0:
            self.gpt_context.append({"role": "assistant", "content": response})
            self.explanations_slides += [(slide_number, response.choices[0].message.content.strip())]
        else:
            self.explanations_slides += [(slide_number, "")]

    def get_explanations_slides(self) -> list:
        """
        This method returns the explanations_slides list
        :return: the explanations_slides list
        """
        return self.explanations_slides
