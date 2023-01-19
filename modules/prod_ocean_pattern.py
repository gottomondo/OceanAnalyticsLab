import shutil
import glob
import os

from modules.module import Module
from tools import utils


MOCK_DIR = "mockups/mock_ocean_pattern"


class OceanPatternMockup(Module):

    def _exec_impl(self, input_files: list):
        file_list_formatted = "\n\t\t- ".join(['', *input_files])
        print(f"INFO File downloaded: {file_list_formatted}")

        root_dir = utils.get_root_dir()
        for file in glob.glob(f"{root_dir}/{MOCK_DIR}/*"):
            filename = os.path.basename(file)
            shutil.copy(file, filename)
