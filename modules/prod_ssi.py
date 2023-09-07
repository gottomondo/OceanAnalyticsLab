import shutil

from modules.module import Module
from tools import utils

MOCK_DIR = "mockups/mock_ssi"


class SSIMockup(Module):

    def _exec_impl(self, input_files: list):
        file_list_formatted = "\n\t\t- ".join(['', *input_files])
        print(f"INFO File downloaded: {file_list_formatted}")

        root_dir = utils.get_root_dir()
        shutil.copy(f"{root_dir}/{MOCK_DIR}/SSI_output.nc", f"{root_dir}/SSI_output.nc")
        shutil.copy(f"{root_dir}/{MOCK_DIR}/SSI_areafassfa_timeseries.png", f"{root_dir}/SSI_area_timeseries.png")
        shutil.copy(f"{root_dir}/{MOCK_DIR}/SSI_maps.png", f"{root_dir}/SSI_maps.png")
