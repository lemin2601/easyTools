import utils
import gv
import config
import sys
import os
from utils import abs_path, join_path
from logger import L
import hashlib
import json
import shutil
import errno
from distutils.dir_util import copy_tree
import inout
from parse import Parser

"""
{
   "packageUrl":"http://49.213.81.43/static/mobile/p13/",
   "remoteManifestUrl":"http://49.213.81.43/static/mobile/p13/project.manifest",
   "remoteVersionUrl":"http://49.213.81.43/static/mobile/p13/version.manifest",
   "version":"7",
   "assets":{
      "src/app.js":{
         "size":2584,
         "md5":"2c1c0aee0b2cb2af5ad972e057d595b4"
      },
      "src/config/LoadResource.js":{
         "size":74,
         "md5":"19a4d9538287531e8c4e262284e4748f"
      },
      "src/config/Resource.js":{
         "size":4979,
         "md5":"af1a910027d3b7b8e717925b666fda96"
      },
    }
}
"""
packageUrl = "packageUrl"
remoteManifestUrl = 'remoteManifestUrl'
remoteVersionUrl = 'remoteVersionUrl'
version = 'version'
assets = 'assets'
size = 'size'
md5 = 'md5'

project_manifest_name = 'project.manifest'
version_manifest_name = 'version.manifest'


def main(args):
    # load default
    num_version = gv.cdn_version()
    client_path = gv.client_path()
    package_url = gv.cdn_package_url()
    cdn_deploy_path = gv.cdn_path()
    dst_project_manifest = gv.client_path()
    folder_will_gen = gv.cdn_manifest_folder_gen()

    if len(args) > 0:
        parser = Parser(prog=utils.abs_path('./update_manifest.py'))
        parser.add_argument("-ver", "--version", default=num_version, help="version manifest")
        parser.add_argument("-cli", "--client_path", default=client_path, help="version manifest")
        parser.add_argument("-pak", "--package_url", default=package_url, help="version manifest")
        parser.add_argument("-cdn", "--cdn_path", default=cdn_deploy_path, help="version manifest")
        parser.add_argument("-dst", "--dst_project_manifest", default=dst_project_manifest, help="version manifest")
        parser.add_argument("-fol", "--folder_gen", default=folder_will_gen, help="version manifest")
        arguments = parser.parse_args(args)
        num_version = arguments.version
        client_path = arguments.client_path
        package_url = arguments.package_url
        cdn_deploy_path = arguments.cdn_path
        dst_project_manifest = arguments.dst_project_manifest
        folder_will_gen = arguments.folder_gen

    gen_manifest(num_version, client_path, package_url, cdn_deploy_path, dst_project_manifest, folder_will_gen)


def gen_manifest(num_version, client_path, package_url,
                 dest_path, dest_project_manifest, folder_will_gen):
    """

    :param client_path:
    :param folder_will_gen:
    :param num_version:
    :param package_url:
    :param dest_path:
    :param dest_project_manifest:
    :return:
    """

    json_manifest = {
        packageUrl: package_url,
        remoteManifestUrl: join_path(package_url, project_manifest_name),
        remoteVersionUrl: join_path(package_url, version_manifest_name),
        version: num_version
    }
    L.error(utils.abs_path(dest_path))
    # json_assets = gen_folders({}, client_path, '')
    json_assets = {}
    for folder in folder_will_gen:
        json_assets = gen_folders(json_assets, join_path(client_path, folder), folder)
        copy_tree(join_path(client_path, folder), join_path(dest_path, folder))
    save(json_manifest, json_assets, dest_path, dest_project_manifest)
    # L.debug(json.dumps(json_assets, indent=4))
    pass


def copy(src, dest):
    try:
        shutil.copy(src, dest)
    except IOError as e:
        # ENOENT(2): file does not exist, raised also on missing dest parent dir
        if e.errno != errno.ENOENT:
            raise
        # try creating parent directories
        os.makedirs(os.path.dirname(dest))
        shutil.copy(src, dest)


def save(json_manifest, json_assets, dest_path, dest_project_manifest):
    L.debug("save-ing ...")
    L.debug(json.dumps(json_manifest, indent=4))
    path_version = abs_path(join_path(dest_path, version_manifest_name))
    L.debug("%s", path_version)

    inout.write_json(path_version, json_manifest)
    json_manifest[assets] = json_assets

    path_project = abs_path(join_path(dest_path, project_manifest_name))
    inout.write_json(path_project, json_manifest)
    L.debug("%s", path_project)

    path_project = abs_path(join_path(dest_project_manifest, project_manifest_name))
    inout.write_json(path_project, json_manifest)
    L.debug("project.manifest => %s", path_project)
    L.debug("save success !!!")


def gen_folders(json_result, path, parent):
    path = abs_path(path)
    files = os.listdir(path)
    # L.info("+ dir: %s", path)
    for name in files:
        full_path = join_path(path, name)
        if os.path.isdir(full_path):
            json_result = gen_folders(json_result, full_path, join_path(parent, name))
        elif os.path.isfile(full_path):
            json_result = gen_files(json_result, parent, name, full_path)

    return json_result


def gen_files(json_result, parent, name, full_path):
    key_file = join_path(parent, name)
    size_file = os.path.getsize(full_path)
    md5_file = hashlib.md5(file_as_bytes(open(full_path, 'rb'))).hexdigest()
    json_result[key_file] = {
        size: size_file,
        md5: md5_file
    }
    return json_result


def file_as_bytes(file):
    with file:
        return file.read()


if __name__ == "__main__":
    args = utils.get_args(sys.argv)
    main(args)
