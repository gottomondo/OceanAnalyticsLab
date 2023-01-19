import os

from modules.module import Module
from tools import fields_mng
from tools import time_utils
from download import daccess
from input import string_template, working_domain as wd


class Download(Module):

    def _exec_impl(self, dl_dir: str = None, get_template: bool = None):
        files_to_process = self.retrieve_file(dl_dir, get_template)

        return files_to_process

    def retrieve_file(self, dl_dir: str, get_template: bool = False):
        """
        Function to retrieve the requested files.
        Args:
            dl_dir: download where store the file
            get_template: If True, daccess return some special string which can be used later to download the files.
                This function is used to know how much files the algorithm needs before to start the execution.

        Returns: A list of downloaded files if get_template is False, otherwise a list of string

        """
        if os.path.isdir(dl_dir):
            print(f"INFO download dir {dl_dir} already exists, nothing to do...")
             #return
        start_time, end_time, month = self._input_parameters.get_start_end_time_and_month()
        working_domain = self._input_parameters.get_working_domain()
        data_source = self._input_parameters.get_data_source()
        id_field = self._input_parameters.get_id_field()

        daccess_wd = wd.init_daccess_working_domain(working_domain)
        fields = fields_mng.get_cf_standard_name(id_field)
        times = time_utils.get_time_range_wd(start_time, end_time, month)

        dcs = daccess.Daccess(data_source, fields, output_dir=dl_dir)
        outfile = list()
        for time in times:
            daccess_wd['time'] = time
            if get_template:
                for file_template in string_template.get_outfile_template(data_source, daccess_wd, fields):
                    outfile.append(file_template)
            else:
                dcs.download(daccess_wd, rm_file=False)
        return outfile
