import powerpoint_parser
import gpt_explainer
import asyncio


async def main():
    # Get the path to the PowerPoint file
    path = input("Enter your powerpoint file path\n")

    # Create a PowerpointParser object
    pptx_object = powerpoint_parser.PowerpointParser(path)

    # Create a GPTExplainer object
    gpt_object = gpt_explainer.GptExplainer()

    # Iterate through each slide and send the slide text to the GPTExplainer object
    for slide, text in enumerate(pptx_object.extract_text_from_slide()):
        await gpt_object.send_slide_text_to_gpt(slide, text)

    # Print the results
    print(gpt_object.get_explanations_slides())


if __name__ == '__main__':
    asyncio.run(main())
