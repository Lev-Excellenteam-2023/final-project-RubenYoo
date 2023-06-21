import Parser.powerpoint_parser as powerpoint_parser
import Explainer.gpt_explainer as gpt_explainer
import Utils.gather_explanations_to_json as gather_explanations_to_json
import asyncio
import glob
import os
import time


async def main():
    pattern = '../Web_api/uploads/*.pptx'
    pattern2 = '../Web_api/outputs/*.json'
    my_pptx = set()

    [my_pptx.add(os.path.splitext(os.path.basename(file_path))[0]) for file_path in glob.glob(pattern2) if
     not os.path.isdir(file_path)]
    print(my_pptx)

    while True:
        time.sleep(5)
        files = [file_path for file_path in glob.glob(pattern) if not os.path.isdir(file_path)]

        for file in files:
            file_name = os.path.splitext(os.path.basename(file))[0]

            if file_name not in my_pptx:
                print(f'processing {file_name}...')

                pptx_object = powerpoint_parser.PowerpointParser(file)

                gpt_object = gpt_explainer.GptExplainer()

                coroutines = [gpt_object.send_slide_text_to_gpt(slide_number, slide_text) for slide_number, slide_text
                              in
                              enumerate(pptx_object.extract_text_from_slide())]

                await asyncio.gather(*coroutines)

                gather_explanations_to_json.save_to_json(gpt_object.get_explanations_slides(), file)

                my_pptx.add(file_name)

                print(f'{file_name} was processed successfully')
                print(my_pptx)


if __name__ == '__main__':
    asyncio.run(main())
