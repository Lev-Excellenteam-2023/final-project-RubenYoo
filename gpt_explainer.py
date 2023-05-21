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

        print(f"Slide {slide_number} processing...")

        # Setting the slide text as the user input
        self.gpt_context.append({"role": "user", "content": text_of_slide})

        # Generate a response from the model

        try:
            response = await asyncio.to_thread(openai.ChatCompletion.create,
                                               model=self.model,
                                               messages=self.gpt_context,
                                               timeout=TIMEOUT
                                               )
        except openai.error.Timeout | openai.error.APIError | openai.error.APIConnectionError\
                | openai.error.InvalidRequestError | openai.error.AuthenticationError \
                | openai.error.PermissionError | openai.error.RateLimitError as e:
            print(f"Slide: {slide_number} was not processed because of the following error: {e}")
            exit()

        print(f"Slide {slide_number} processed!")

        # If the response is not empty, save it in the explanations_slides list
        if 'choices' in response and len(response.choices) > 0:
            self.explanations_slides += [(slide_number, response.choices[0].message.content.strip())]
        else:
            self.explanations_slides += [(slide_number, "")]

    def get_explanations_slides(self) -> list:
        """
        This method returns the explanations_slides list
        :return: the explanations_slides list
        """
        return self.explanations_slides


async def main():
    # Initialize the class
    gpt_explainer = GptExplainer()

    # Send the text of the slides to the gpt-3.5-turbo model
    await asyncio.gather(gpt_explainer.send_slide_text_to_gpt(1, "Asyncio"),
                         gpt_explainer.send_slide_text_to_gpt(2, "Concurrency"),
                         gpt_explainer.send_slide_text_to_gpt(3, "Multiprocessing"))

    # Print the explanations of the slides
    print(gpt_explainer.get_explanations_slides())


if __name__ == '__main__':
    asyncio.run(main())
