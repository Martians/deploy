# coding=utf-8
from common import *


class LocalConfig(LocalBase):
    def __init__(self):
        LocalBase.__init__(self, 'docker')
        self.centos = ('centos:centos', '0_centos')
        self.fabric = ('centos:fabric', '0_fabric')
        self.server = '0_server'
        self.system = "--privileged=true -v /sys/fs/cgroup:/sys/fs/cgroup"
        self.volume = '-v {base}:/fabric'.format(base=glob_conf.path)

        self.proxy = True   # 局域网 代理
        self.http  = True   # 局域网 http


local = LocalConfig()


def build_images(c, type, image, dockerfile, build='', param=''):
    """ 生成的image中，将整个fabric文件夹都复制过去了
    """
    if type == 1:
        c.run('docker rmi -f {image}'.format(image=image), warn=True)

    if stdouted(c, 'docker images {image} -q'.format(image=image)):
        color('image [{image}] already exist'.format(image=image))
    else:
        color('create image [{image}]'.format(image=image))
        c.run('docker build -t {image} -f template/{dockerfile}{build}{param} {context}'.
                format(image=image, dockerfile=dockerfile, context=glob_conf.path,
                       build=args(build, ' --build-arg '), param=args(param, ' --build-arg EXEC=')))


def prepare_images(c, proxy=local.proxy, http=local.http):
    """ 创建 base、init
    """
    build_images(c, 0, local.base[0], local.base[1])
    build_images(c, 0, local.fabric[0], local.fabric[1])

    """ 创建 proxy、http
    """


def build_docker(c, type, image, name, exec='/bin/bash', volume=local.volume, **kwargs):
    if type == 0 or type == 1:
        c.run('docker rm -f {name}'.format(name=name), warn=True)

    if stdouted(c, 'docker ps -a | grep {name}$'.format(name=name)):
        color('docker [{name}] already exist'.format(name=name))
    else:
        c.run('docker run -itd --name {name} -h {name} {volume} {image} {exec}'.
              format(image=image, name=name, volume=volume, exec=exec))


def prepare_docker(c):
    pass


########################################################################################################################
def start_images(c, type, name, port=0, http=local.http, proxy=local.proxy, **kwargs):
    prepare_images(c)

    """ 将所有参数用引号封装 -> dockerfile run shell -> 通过 server.py 解析出来
    """
    param = ''
    param = sep(param, args(name, '--server '), ' ')
    param = sep(param, args(http, '--http', ignore=True), ' ')
    param = sep(param, args(proxy, '--proxy', ignore=True), ' ')

    build_images(c, type, image=name, dockerfile=local.server, build=args(port, 'LISTEN='), param=args(param, '"', '"'))


def start_docker(c, type, name, enter=False, **kwargs):
    """ 创建基础 images：centos、fabric
    """
    start_images(c, type, name, **kwargs)

    build_docker(c, type, image=name, name=name, **kwargs)

    command = 'docker exec -it {name} /bin/bash'.format(name=name)
    if enter:
        c.run('{command}'.format(command=command), echo=False, pty=True)
    else:
        c.run('echo "{command}"'.format(command=command), echo=False)