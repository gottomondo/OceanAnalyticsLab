import shutil

from modules.module import Module
from tools import utils


class OceanClimateMockup(Module):

    def _exec_impl(self, input_files: list):
        file_list_formatted = "\n\t\t- ".join(['', *input_files])
        print(f"INFO File downloaded: {file_list_formatted}")

        root_dir = utils.get_root_dir()

        file_to_copy = input_files[0]   # return the first found element in input dir
        print(f"INFO Copying {file_to_copy} as output.nc")
        output_file = root_dir + "/output.nc"
        shutil.copy(file_to_copy, output_file)
