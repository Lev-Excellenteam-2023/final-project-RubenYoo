import powerpoint_parser
import gpt_explainer
import gather_explanations_to_json
import asyncio


async def main():
    # Get the path to the PowerPoint file
    path = input("Enter your powerpoint file path\n")

    try:
        pptx_object = powerpoint_parser.PowerpointParser(path)
    except FileNotFoundError as error:
        print(error)
        exit()

    gpt_object = gpt_explainer.GptExplainer()

    # Iterate through each slide and extract the slide text
    coroutines = [gpt_object.send_slide_text_to_gpt(slide_number, slide_text) for slide_number, slide_text in
                  enumerate(pptx_object.extract_text_from_slide())]

    # explain each slide
    await asyncio.gather(*coroutines)

    # Save the results into a json file
    gather_explanations_to_json.save_to_json(gpt_object.get_explanations_slides(), path)


if __name__ == '__main__':
    asyncio.run(main())
