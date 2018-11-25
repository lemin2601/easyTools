from logger import L
from utils import get_args, abs_path, join_path, json_stringify
import sys
import json
from parse import Parser
from inout import write
import os
import ntpath
import re
import gv

default_src = './res'
default_dst = './src/Resource.js'
default_ext = ['*.*']
default_folder = ['*']
default_folder_except = []

pattern_save = "var res=@content;"


def main(args):
    # load default config
    global default_folder_except
    global default_folder
    global default_ext
    global default_dst
    global default_src
    default_src = join_path(gv.client_path(), gv.gen_res_path())
    default_dst = join_path(gv.client_path(), gv.gen_dst_path())
    default_ext = gv.gen_ext()
    default_folder = gv.gen_folder()
    default_folder_except = gv.gen_folder_except()

    parser = Parser(prog='gen.py')
    parser.add_argument("-src", "--source", default=default_src, help="folder res will gen, default=" + default_src)
    parser.add_argument("-dst", "--destination", default=default_dst,
                        help="destination file will save, default=" + default_dst)
    parser.add_argument("-ext", "--extension", nargs='+', default=default_ext,
                        help="list extension file will gen to res, default=" + json.dumps(default_ext))
    parser.add_argument("-folder", "--folder_gen", nargs='+', default=default_folder,
                        help="list folder will gen, default=" + json.dumps(default_folder))
    parser.add_argument("-_folder", "--folder_except", nargs='+', default=default_folder_except,
                        help="list folder will not gen, default=" + json.dumps(default_folder_except))
    arguments = parser.parse_args(args)
    execute(arguments.source, arguments.destination, arguments.extension, arguments.folder_gen, arguments.folder_except)
    # L.debug(arguments)


def valid_folder(path):
    return True


def valid_ext(file_extension):
    return True


def execute(src, dst, ext, folder, folder_except):
    global default_ext
    global default_folder
    global default_folder_except
    default_ext = ext
    default_folder = folder
    default_folder_except = folder_except

    json_result = gen_folders({}, src, ntpath.basename(src))
    save(json_result, dst)


def gen_folders(json_result, path, parent):
    path = abs_path(path)
    if valid_folder(path):
        files = os.listdir(path)
        L.info("+ dir: %s", path)
        for name in files:
            full_path = join_path(path, name)
            if os.path.isdir(full_path):
                json_result = gen_folders(json_result, full_path, join_path(parent, name))
            elif os.path.isfile(full_path):
                json_result = gen_files(json_result, parent, name)
    else:
        L.warning("- dir: %s", path)
    return json_result


def normal_key(file_name):
    return re.sub("[!@#$%^&*()[\]{};:,./<>?\|`~\-=_+\s]", "_", file_name.lower())
    # result = re.sub("[!@#$%^&*()[\]{};:,./<>?\|`~\-=_+\s]", "_", file_name.lower())
    # L.debug("normal file %s %s", file_name, result)
    # return result


def gen_files(json_result, parent, name):
    file_name, file_extension = os.path.splitext(name)
    value = join_path(parent, name)
    key = normal_key(file_name)
    if valid_ext(file_extension):
        json_result[key] = value
        # L.info("+ %s = %s", key, value)
    else:
        L.warning("- %s = %s", key, value)
    return json_result


def save(json_content, path):
    path = abs_path(path)
    # json_content = {}
    # for key, value in json_content.iteritems():
    #     print("key: {} | value: {}".format(key, value))
    # content = pattern_save.replace("@content", json.dumps(json_content, indent=4))

    content = pattern_save.replace("@content", json_stringify(json_content))
    write(path, content)
    L.debug("success => save to file:" + path)


if __name__ == "__main__":
    # result = gen_folders({}, "./res", "res")
    # print(json.dumps(result, indent=4))
    args = get_args(sys.argv)
    main(sys.argv)
