
from common import *
from docker.image import *
from optparse import OptionParser


def parse_options():
    parser = OptionParser(usage='%prog --server server --http --proxy')
    parser.add_option('--server', dest='server', help='server type')
    parser.add_option('--http', dest='http', action='store_true', help='use local yum http source')
    parser.add_option('--proxy', dest='proxy', action='store_true', help='use local yum proxy')

    (options, args) = parser.parse_args()
    return options


class Entry:
    def __init__(self, path, work):
        self.path = path
        self.work = work


def regist_entries(server):
    set_invoke(True)

    redirect = Dict({'http': Entry('service.source.server', 'http'),
                     'proxy': Entry('service.source.server', 'proxy')})
    return redirect.get(server)


def install_server():
    options = parse_options()
    entry = regist_entries(options.server)

    if not entry:
        color('install server, not find entry, ignore')
        exit(0)

    mode = 1
    if mode == 0:
        """ 方式1：通过shell方式，调用fab进行安装
        """
        os.system('cd {path}; {work}'.format(path=os.path.join(glob_conf.path, entry.path), work=entry.work))
    else:
        """ 方式2：通过程序方式，直接调用函数
        """
        from invoke import Context
        server = __import__(entry.path, fromlist=[entry.path.split('.')[-1]])
        eval('server.{work}(Context())'.format(work=entry.work))

install_server()