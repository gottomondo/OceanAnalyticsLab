import socket

from tools import utils


class OtherInfo:
    def __init__(self):
        self.poutkey = None
        self.root_dir = utils.get_root_dir()
        self.hostname = socket.gethostname()

    def set_poutkey(self, poutkey):
        self.poutkey = poutkey
