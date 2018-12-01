import utils
import sys
import gv
import inout
from update_manifest import project_manifest_name
from logger import L


def main(args):
    show_version_manifest()


pass


def show_version_manifest():
    num_version = gv.cdn_version()
    cdn_path = utils.join_path(gv.cdn_path(), project_manifest_name)
    client_path = utils.join_path(gv.client_path(), project_manifest_name)
    cdn_config = inout.read_json(cdn_path)
    client_config = inout.read_json(client_path)
    L.debug("version manifest:")
    L.debug("dev.json            => %s", num_version)
    L.debug("client/project.json => %s", client_config['version'])
    L.debug("cdn/project.json    => %s", cdn_config['version'])

    pass


if __name__ == "__main__":
    args = utils.get_args(sys.argv)
    main(args)
