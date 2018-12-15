import socket
import re


def get_host():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    host = s.getsockname()[0]
    s.close()
    return host


def update_host(old_path):
    new_path = old_path
    p = '(?P<method>http.*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*)/?(?P<path>[\W\S]*)'
    m = re.search(p, old_path)
    method = (m.group('method'))  # 'http://'
    host = (m.group('host'))  # 'www.abc.com'
    port = (m.group('port'))  # '123'
    path = (m.group('path'))  # 'test/abc'
    if port == "":
        port = 80
    if path != '':
        path = "/" + path
    new_path = method + get_host() + ":" + port + path
    return new_path


def main():
    print(update_host('http://www.abc.com:123'))

    pass


if __name__ == "__main__":
    main()
