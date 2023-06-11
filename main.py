import Parser.powerpoint_parser as powerpoint_parser
import Gpt_explainer.gpt_explainer as gpt_explainer
import Utils.gather_explanations_to_json as gather_explanations_to_json
import asyncio
import argparse


async def main():

    # Parse the command line arguments
    parser = argparse.ArgumentParser(description="Process slides and generate explanations for each slide.")
    parser.add_argument("input", help="Path to the input PowerPoint file")
    args = parser.parse_args()
    file_path = args.input

    try:
        pptx_object = powerpoint_parser.PowerpointParser(file_path)
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
    gather_explanations_to_json.save_to_json(gpt_object.get_explanations_slides(), file_path)


if __name__ == '__main__':
    asyncio.run(main())
