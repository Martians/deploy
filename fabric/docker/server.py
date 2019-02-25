
from common import *
from optparse import OptionParser
from docker.image import *

""" 用于根据传入的 server 函数地址，进行server的安装
    1. 本地模式：python3 server.py --server {name} --source {source}
            1. 此时set_invoke(True)，使用的c是Context
            2. 此时 getcwd="/"，因为是在根目录下执行本文件;
            3. 没有复制network.yaml到image中；同时也没有配置 config/network.yaml 的绝对路径
            
    2. 远程模式：先构建c，在执行函数 install_server
            此时使用的c是Connection
            
"""


def parse_options():
    parser = OptionParser(usage='%prog --server server --http --proxy')
    parser.add_option('--server', dest='server', help='server type')
    parser.add_option('--source', dest='source', help='use local yum http、proxy、file source')
    parser.add_option('--address',  dest='address',  help='local host ip')

    (options, args) = parser.parse_args()
    return options


class Entry:
    def __init__(self, path, work, param='', start=''):
        self.path = path
        self.work = work
        self.param = param
        self.start = start


def regist_entries():
    redirect = Dict({'http': Entry('service.source.server', 'http', local.http_path[1]),
                     'proxy': Entry('service.source.server', 'proxy', local.proxy_path[1]),
                     'sshd': Entry('service.source.client', 'use_sshd', '{},{}'.format(local.sshd_user, local.sshd_paww))})

    redirect.update({'use_http': Entry('service.source.client', 'use_http', '{}/{}'.format(net.config.local, local.http_url)),
                     'use_proxy': Entry('service.source.client', 'use_proxy', net.config.local),
                     'use_file': Entry('service.source.client', 'use_file', os.path.join(local.http_path[1], local.http_url))})

    redirect.update({'mariadb': Entry('service.database.mariadb', 'install', start='systemctl start mariadb'),
                     'postgres': Entry('service.database.postgres', 'install', start='systemctl start postgresql-9.5.service')})
    return redirect


def get_entry(server):
    return redirect.get(server)


def install_sources(c, source, address):
    if address:
        """ 本地模式执行时，本地没有network.yaml配置文件，使用外部传入的配置参数
        """
        redirect.get('use_http').param = '{}/{}'.format(address, local.http_url)
        redirect.get('use_proxy').param = '{}'.format(address)

    if str_enum_exist(local.senums, source, 'http'):
        do_install(c, 'use_http')

    if str_enum_exist(local.senums, source, 'proxy'):
        do_install(c, 'use_proxy')

    if str_enum_exist(local.senums, source, 'file'):
        print(redirect.get('use_file').param)
        do_install(c, 'use_file')


def start_server(c, name, errexit=True):
    entry = get_entry(name)
    if entry:
        if entry.start:
            c.run('{}'.format(entry.start))
        else:
            print('no retart code, ignore')
    else:
        color('restart server [{}], not find entry, ignore'.format(name))
        if errexit: exit(0)


def install_server(c='', server='', source='', errexit=True):
    """ 指定了server，表明是以函数方式调用此函数
    """
    address = net.config.local
    if server:
        color('prepare install server [{}], source [{}]'.format(server, source))
    else:
        set_invoke(True)
        options = parse_options()
        server = options.server
        source = options.source
        address = options.address

    install_sources(c, source, address)

    do_install(c, server, errexit=errexit)


def do_install(c, name, errexit):
    entry = get_entry(name)

    """ 方式1：通过shell方式，调用fab进行安装
        os.system('cd {path}; {work}'.format(path=os.path.join(globing.path, entry.path), work=entry.work))
        
        方式2：直接调用函数来执行; 使用此方式来执行
    """
    if entry:
        from invoke import Context
        handle = __import__(entry.path, fromlist=[entry.path.split('.')[-1]])

        param = ''
        if entry.param:
            for p in entry.param.split(','):
                param += " , '{}'".format(p)
        eval('handle.{work}({c}{param})'.format(work=entry.work, c='c' if c else 'Context()', param=param))

    else:
        color('do install [{}], not find entry, ignore'.format(name))
        if errexit: exit(0)


redirect = regist_entries()

if __name__ == '__main__':
    install_server()
    # install_server(hosts.adhoc('192.168.0.85', 'root', '111111'), 'http', 'http,proxy')