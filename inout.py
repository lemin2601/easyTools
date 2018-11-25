from json import load, dumps
import os
from logger import L
import utils
import ntpath


def write_json(path, json):
    # context = dumps(json, indent=4, sort_keys=True)
    context = dumps(json, indent=4)
    write(path, context)


def write(path, content):
    f = open(path, "w+")
    f.write(content)
    f.close()
    # L.debug("write" + os.path.abspath(path))
    pass


def read_text(path):
    L.debug("read_text" + os.path.abspath(path))
    f = open(path, "r")
    if f.mode == 'r':
        contents = f.read()
        f.close()
        return contents
    f.close()
    return ''


def read_json(path):
    L.debug("red_json" + os.path.abspath(path))
    f = open(path, "r")
    result = load(f)
    f.close()
    return result




if __name__ == "__main__":
    name = ntpath.basename("./c")
    file_name, file_extension = os.path.splitext("/a/abc")
    print(file_extension)
    print(file_name)
    print(name)
    # path = os.path.abspath("./")
    # files = os.listdir(path)
    # for name in files:
    #     full_path = os.path.join(path, name)
    #     print(name)
    #     if os.path.isdir(full_path):
    #         print('    dir')
    #     elif os.path.isfile(full_path):
    #         fileName, fileExtension = os.path.splitext(full_path)
    #         print('    file' + fileName)


    pass

    # save = {
    #     "path":"D:/abc/xyz"
    # }
    # save["path"] = os.path.abspath(save["path"])
    # write_json("./abc.json", save)
    #
    # print(utils.normalize_path(read_json('./abc.json')["path"]))
    # L.debug(read_json('./abc.json'))
