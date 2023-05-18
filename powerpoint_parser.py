import pptx
import os


class PowerpointParser:
    def __int__(self, file_path: str) -> None:
        if os.path.isfile(file_path):
            self.pptx_file = file_path
        else:
            raise FileNotFoundError("The powerpoint file was not found")
