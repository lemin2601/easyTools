import shlex
import os
from gv import num_version
import signal
import sys


def get_args(agrv):
    if len(agrv) > 1:
        args = agrv[1:]
    else:
        args = []
    return args


def parse_args(str_line):
    args = shlex.split(str_line)
    return args


def abs_path(path):
    return normalize_path(os.path.abspath(path))


def normalize_path(path):
    return path.replace('\\\\', "/")


def join_path(path, *paths):
    return normalize_path(os.path.join(path, *paths))


def json_stringify(json_content, indent=4):
    if num_version == 2 and isinstance(json_content, basestring):
        return json_content
    if num_version == 3 and isinstance(json_content, str):
        return json_content
    else:
        space = indent * ' '
        end_line = ''
        content = '{'
        if indent > 0:
            end_line = '\n'
        for key in json_content:
            value = json_stringify(json_content[key], indent + 1)
            content += end_line + space + key + ": " + '"' + value + '",'
        content = content[:-1]
        content += end_line
        content += "}"
        return content


def signal_handler(sig, frame):
    print('\n\nYou pressed Ctrl+C! => exit')
    sys.exit(0)


def register_exit():
    signal.signal(signal.SIGINT, signal_handler)
    # print('Press Ctrl+C')
    # signal.pause()
