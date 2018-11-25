import sys
import os

num_version = int(sys.version[:1])

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # This is your Project Root

project_config = {
    "client_path": "./",
    "deploy_path": "./../deploy",
    "cdn_deploy_path": "./../deploy/cdn",
    "package_url": "http://localhost:9002",
    "manifest": {
        "folder": [
            "src",
            "res"
        ],
        "version": "1.1.1.1",
        "port": 9002
    },
    "gen": {
        "res": "./res",
        "dst": "./src/Resource.js",
        "ext": [
            "*.*"
        ],
        "folder": [
            "*"
        ],
        "folder_except": []
    }
}


def client_path():
    return project_config['client_path']


def deploy_path():
    return project_config['deploy_path']


def cdn_path():
    return project_config['cdn_deploy_path']


def cdn_package_url():
    return project_config['package_url']


def cdn_manifest_folder_gen():
    return project_config['manifest']['folder']


def cdn_version():
    return project_config['manifest']['version']

def cdn_port():
    return project_config['manifest']['port']

def gen_res_path():
    return project_config['gen']['res']


def gen_dst_path():
    return project_config['gen']['dst']


def gen_ext():
    return project_config['gen']['ext']


def gen_folder():
    return project_config['gen']['folder']


def gen_folder_except():
    return project_config['gen']['folder_except']

#
# client_path = './'
# deploy_path = './../deploy'
# cdn_deploy_path = './../deploy/cdn'
#
# package_port = 9002
# package_url = 'http://localhost'
