from logger import L
from parse import Parser
from utils import parse_args
import config
import json
import sys
import gen
import os
import gv
import utils
import update_manifest
import info
import http_server
import network
import android_build


def execute_func(key, args):
    key = key.strip().lower()
    if key in config.key:
        if key == 'info':
            info.main(args)
        if key == 'gen':
            gen.main(args)
        if key == 'cdn':
            update_manifest.main(args)
        if key == 'update-dev':
            gv.cdn_set_package_url(network.update_host(gv.cdn_package_url()))
            gv.save()
        if key == "update-cdn-url":
            gv.cdn_set_package_url(network.update_host(gv.cdn_package_url()))
            gv.save()
        if key == "android-gen":
            android_build.main(args)
        if key == 'cdn-run':
            print(gv.ROOT_DIR)
            path = os.path.join(gv.ROOT_DIR, "http_server.py")
            path = os.path.abspath(path)
            # cmd = "python {0} -port {1} -path {2}".format(path, gv.cdn_port(), utils.abs_path(gv.cdn_path()))
            print(gv.cdn_package_url())
            http_server.run(gv.cdn_port(), "", utils.abs_path(gv.cdn_path()))
            # os.system(cmd)

        if key == 'jslist':
            cmd = 'jslist -f "{0}"'.format(utils.abs_path(utils.join_path(gv.client_path(), "./project.json")))
            print(cmd)
            os.system(cmd)

        if key == 'run':
            cmd = 'cocos run --proj-dir="{0}" -p web -m debug'.format(utils.abs_path(gv.client_path()))
            print(cmd)
            os.system(cmd)

        if key == 'quit' or key == 'exit' or key == 'q':
            L.info(">>Quit!")
            sys.exit(0)
    pass


def main(args):
    L.debug("main commander")
    parser = Parser(prog='commander.py')
    parser.add_argument("key", default=None, help=get_help())
    if len(args) > 0:
        arguments = [args.pop(0)]
        arguments = parser.parse_args(arguments)
        if arguments is None:
            pass
        else:
            key_found = arguments.key
            if key_found is not None:
                L.debug("find key:" + key_found)
                execute_func(key_found, args)
    else:
        parser.print_help()


def parse(str_line):
    arguments = parse_args(str_line)
    main(arguments)


def get_help():
    return json.dumps(config.key, indent=4, sort_keys=True)
