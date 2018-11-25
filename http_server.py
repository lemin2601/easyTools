import argparse

import os
import utils
import sys
from parse import Parser
from logger import L
from gv import num_version
import gv

if num_version == 2:
    import SimpleHTTPServer
    import SocketServer

    pass
else:
    import http.server
    from http.server import CGIHTTPRequestHandler, SimpleHTTPRequestHandler


def run(port=8000, address='', path="./"):
    utils.register_exit()
    L.error("p %s a %s p %s", port, address, path)
    if num_version == 2:
        L.debug(utils.abs_path(path))
        os.chdir(path)
        handler = SimpleHTTPServer.SimpleHTTPRequestHandler
        httpd = SocketServer.TCPServer((address, port), handler)
        httpd.serve_forever()
        pass
    else:
        L.debug(utils.abs_path(path))
        os.chdir(path)
        http.server.test(HandlerClass=SimpleHTTPRequestHandler, port=port, bind=address)


def main(args):
    parser = Parser(prog=utils.abs_path('./http_server.py'))

    parser.add_argument("-port", type=int, default=gv.cdn_port(), help="port will run: default 8000")
    parser.add_argument("-address", default='',
                        help="address bind, default any")
    parser.add_argument("-path", default=gv.cdn_path(),
                        help="path will run http, default :" + utils.abs_path(gv.cdn_path()))

    arguments = parser.parse_args(args)
    run(arguments.port, arguments.address, arguments.path)

    # parser = argparse.ArgumentParser()
    # parser.add_argument('--cgi', action='store_true',
    #                     help='Run as CGI Server')
    # parser.add_argument('--bind', '-b', default='', metavar='ADDRESS',
    #                     help='Specify alternate bind address '
    #                          '[default: all interfaces]')
    # parser.add_argument('port', action='store',
    #                     default=8000, type=int,
    #                     nargs='?',
    #                     help='Specify alternate port [default: 8000]')
    #
    # args = parser.parse_args()
    # if args.cgi:
    #     handler_class = CGIHTTPRequestHandler
    # else:
    #     handler_class = SimpleHTTPRequestHandler
    # http.server.test(HandlerClass=handler_class, port=args.port, bind=args.bind)
    pass


if __name__ == '__main__':
    args = utils.get_args(sys.argv)
    main(args)
