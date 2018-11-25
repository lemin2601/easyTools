import argparse
from logger import L


class Parser(argparse.ArgumentParser):
    def exit(self, status=0, message=None):
        L.debug("exit")
        pass

