import sys
import commander
import shlex
import utils
from logger import L
from gv import num_version, load_config_project
from time import sleep


def main(arguments):
    # My code here
    if len(arguments) > 1:
        commander.main(args)
    else:
        utils.register_exit()
        loop()
    pass


def loop():
    """
    1. read input
    2. pasrse command
    3. continue

    :return:
    """

    load_config_project()

    L.debug("running with version: %s", sys.version)
    is_version_2 = sys.version.startswith("2")
    while True:
        response = ''
        if num_version == 2:
            response = raw_input("Enter command:")
        if num_version == 3:
            response = input("Enter command:")

        if response != '':
            commander.parse(response)
        sleep(0.5)


def get_agrs(str_line):
    args = shlex.split(str_line)
    return args


if __name__ == "__main__":
    args = utils.get_args(sys.argv)
    main(args)
