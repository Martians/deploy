# coding=utf-8
from common import *


class LocalConfig(LocalBase):
    def __init__(self):
        LocalBase.__init__(self, 'docker')
        self.centos = ('centos:centos', '0_centos')
        self.fabric = ('centos:fabric', '0_fabric')
        self.server = '0_server'
        self.system = "--privileged=true -v /sys/fs/cgroup:/sys/fs/cgroup"
        self.volume = '{base}:/fabric'.format(base=globing.path)

        self.use_proxy = True   # 局域网 代理
        self.use_http = True    # 局域网 http

        # 如果修改 dest 位置，需要一同修改 service.source.server 中的 http_path
        self.http_port = 80
        self.http_path = ('/mnt/hgfs/repo/', '/home/repo')

        self.proxy_path = ('/mnt/hgfs/proxy', '/home/proxy')


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
        c.run('''cd {base}/docker; 
        docker build -t {image} -f template/{dockerfile}{build}{param} {context}'''.
                format(base=globing.path, image=image, dockerfile=dockerfile, context=globing.path,
                       build=args(build, ' --build-arg '), param=args(param, ' --build-arg EXEC=')))


def prepare_images(c, proxy=local.use_proxy, http=local.use_http):
    """ 1. centos：最原始镜像，安装了 vim 等必要工具
        2. fabric：1）基础上，安装了fabric相关；执行 - fabric.sh
        3. server：2）基础上，执行不同server；  执行 - server.sh
    """
    build_images(c, 0, local.centos[0], local.centos[1])
    build_images(c, 0, local.fabric[0], local.fabric[1])

    """ 创建 proxy、http
    """


def build_docker(c, type, name, image='', exec='', volume='', port='', **kwargs):
    image = image if image else name

    if type == 0 or type == 1:
        c.run('docker rm -f {name}'.format(name=name), warn=True)

    if not stdouted(c, 'docker ps -a | grep {name}$'.format(name=name)):
        """ volume: 传入逗号分隔的多个: /abc:/efg,/a:/b ==> -v /abc:/efg -v /a:/b
        """
        vlist = ''
        volume = sep(volume, local.volume)
        for v in volume.split(','):
            vlist = sep(vlist, '-v {}'.format(v), ' ')

        """ port: 传入逗号分隔的多个：80,100,10:90 ===> -p 80:80 -p 100:100 -p 10:90
        """
        plist = ''
        for p in str(port).split(','):
            if p.find(':') != -1:
                plist = sep(plist, '-p {port}'.format(port=p), ' ')
            else:
                plist = sep(plist, '-p {port}:{port}'.format(port=p), ' ')

        c.run('docker run -itd --name {name} -h {name}{port}{volume} {image} {exec}'.
              format(image=image, name=name, port=args(plist, ' '), volume=args(vlist, ' '), exec=exec))

    elif not stdouted(c, 'docker ps | grep {name}$'.format(name=name)):
        color('docker [{name}] stopped, restart'.format(name=name))
        c.run('docker start http '.format(name=name), warn=True)

    else:
        color('docker [{name}] already start'.format(name=name))

def prepare_docker(c):
    pass


########################################################################################################################
def start_http(c, type, **kwargs):
    start_images(c, type, 'http', port=local.http_port, http=False, proxy=False)

    kwargs['path'] = args_def(kwargs['path'], local.http_path[0])
    kwargs['port'] = args_def(kwargs['port'], local.http_port)
    print('http: port [{port}], path [{path}]'.format(port=kwargs['port'], path=kwargs['path']))

    volume = '{}:{}'.format(kwargs['path'], local.http_path[1])
    kwargs['port'] = '{out}:{ins}'.format(out=kwargs['port'], ins=local.http_port)

    build_docker(c, type, name='http', volume=volume, http=False, proxy=False, **kwargs)


def start_proxy(c, type, **kwargs):
    start_images(c, type, 'proxy', http=False, proxy=False)

    kwargs['path'] = args_def(kwargs['path'], local.proxy_path[0])
    print('proxy: path [{path}]'.format(path=kwargs['path']))

    volume = '{}:{}'.format(kwargs['path'], local.proxy_path[1])
    build_docker(c, type, name='proxy', volume=volume, http=False, proxy=False, **kwargs)


########################################################################################################################
def start_images(c, type, name, port=0, http=local.use_http, proxy=local.use_proxy, **kwargs):
    prepare_images(c)

    """ 将所有参数用引号封装 -> dockerfile run shell -> 传递给 server.py 解析出来
    """
    param = ''
    param = sep(param, args(name, '--server '), ' ')
    param = sep(param, args(http, '--http', ignore=True), ' ')
    param = sep(param, args(proxy, '--proxy', ignore=True), ' ')

    build_images(c, type, image=name, dockerfile=local.server, build=args(port, 'LISTEN='), param=args(param, '"', '"'))


def start_docker(c, type, name, enter=False, **kwargs):
    start_images(c, type, name, **kwargs)

    build_docker(c, type, name=name, **kwargs)

    """ 当前进入新创建的 docker
    """
    command = 'docker exec -it {name} /bin/bash'.format(name=name)
    if enter:
        c.run('{command}'.format(command=command), echo=False, pty=True)
    else:
        c.run('echo "{command}"'.format(command=command), echo=False)