import powerpoint_parser
import gpt_explainer
import asyncio


async def main():
    # Get the path to the PowerPoint file
    path = input("Enter your powerpoint file path\n")

    try:
        pptx_object = powerpoint_parser.PowerpointParser(path)
    except FileNotFoundError as e:
        print(e)
        exit()

    gpt_object = gpt_explainer.GptExplainer()

    # Iterate through each slide and extract the slide text
    coroutines = [gpt_object.send_slide_text_to_gpt(slide_number, slide_text) for slide_number, slide_text in
                  enumerate(pptx_object.extract_text_from_slide())]

    # explain each slide
    await asyncio.gather(*coroutines)

    # Print the results
    print(gpt_object.get_explanations_slides())


if __name__ == '__main__':
    asyncio.run(main())
