# coding=utf-8
from common import *
from docker import helps
from docker import network as net


class LocalConfig(LocalBase):
    def __init__(self):
        LocalBase.__init__(self, 'docker')
        ################################################################################################################
        """ 基础镜像配置
        """
        self.centos = ('centos:centos', '0_centos')
        self.fabric = ('centos:fabric', '0_fabric')
        self.server = '0_server'

        ################################################################################################################
        """ sshd 相关配置
        """
        self.sshd_port = 22
        self.systemd = " --privileged=true -v /sys/fs/cgroup:/sys/fs/cgroup"
        self.initial = '/usr/sbin/init'
        self.volume = '{base}:/fabric'.format(base=globing.path)

        ################################################################################################################
        """ 是否使用 http、proxy 设置yum源
                1. 如果修改 dest 位置，需要一同修改 service.source.server 中的 http_path
        """
        self.use_http = True
        self.use_proxy = True

        self.http_port = 80
        self.http_path = ('/mnt/hgfs/repo/', '/home/repo')

        self.proxy_port = 3142
        self.proxy_path = ('/mnt/hgfs/proxy', '/home/proxy')

        ################################################################################################################
        self.flag = Dict()
        self.images_count = 0
        self.docker_count = 0


local = LocalConfig()

""" 1. server image
        1. 基于新 image，image中包含了server的服务内容：base的选择：fabric、sshd
        2. 基于sshd的：然后在新创建的 docker 中，安装服务
"""


def build_images(c, type, image, dockerfile, build='', param='', noisy=True):
    """ 1. 复制：将整个fabric文件夹都复制过去了
        2. 变量：build传递变量给dockerfile，目前只有 port
        3. 传参：构建server的参数，统一封装在 --build-arg EXE 参数中，交给构建脚本
        4. 构建：fabric.sh 用于构建基础fabrc镜像；server.sh 构建其他 server 镜像
    """
    if type == 1:
        color('clean image: [{image}]'.format(image=image))
        c.run('docker rmi -f {image}'.format(image=image), warn=True)

    if stdouted(c, 'docker images {image} -q'.format(image=image)):
        if noisy:
            color('image [{image}] already exist'.format(image=image))

    else:
        local.images_count += 1
        color('create image: [{image}]'.format(image=image))
        c.run('''cd {base}/docker; 
        docker build -t {image} -f template/{dockerfile}{build}{param} {context}'''.
                format(base=globing.path, image=image, dockerfile=dockerfile, context=globing.path,
                       build=args(build, ' --build-arg '), param=args(param, ' --build-arg EXEC=')))


def basing_images(c):
    if local.flag.basing:
        return
    else:
        local.flag.basing = True

    """ 1. centos：最原始镜像，安装了 vim 等必要工具
        2. fabric：1）基础上，安装了fabric相关；执行 - fabric.sh
        3. server：2）基础上，执行不同server；  执行 - server.sh
    """
    # color('====> create base image')
    build_images(c, 0, image=local.centos[0], dockerfile=local.centos[1], noisy=False)
    build_images(c, 0, image=local.fabric[0], dockerfile=local.fabric[1], noisy=False)


def build_docker(c, type, name, image='', exec='', volume='', port='', systemd=False, host='',
                 output='', noisy=True, **kwargs):
    image = args_def(image, name)
    do_output = True

    if type == 0 or type == 1:
        color('remove docker: [{name}]'.format(name=name))
        c.run('docker rm -f {name}'.format(name=name), warn=True)

    if not stdouted(c, 'docker ps -a | grep {name}$'.format(name=name)):
        """ volume: 传入逗号分隔的多个: /abc:/efg,/a:/b ==> -v /abc:/efg -v /a:/b
        """
        vlist = ''
        volume = sep(volume, local.volume)
        if volume:
            for v in volume.split(','):
                vlist = sep(vlist, '-v {}'.format(v), ' ')

        """ port: 传入逗号分隔的多个：80,100,10:90 ===> -p 80:80 -p 100:100 -p 10:90
        """
        plist = ''
        if port:
            for p in str(port).split(','):
                if p.find(':') != -1:
                    plist = sep(plist, '-p {port}'.format(port=p), ' ')
                else:
                    plist = sep(plist, '-p {port}:{port}'.format(port=p), ' ')

        local.docker_count += 1
        color('create docker: [{name}]{base}...'.format(name=name, base=' base on [{}]'.format(image) if name != image else ''))
        c.run('docker run -itd --name {name} -h {name}{port}{volume}{systemd} {image} {exec}'.
              format(image=image, name=name, port=args(plist, ' '), volume=args(vlist, ' '),
                     systemd=local.systemd if systemd else '', exec=local.initial if local.systemd else exec))

    elif not stdouted(c, 'docker ps | grep {name}$'.format(name=name)):
        color('start docker: [{name}]'.format(name=name))
        c.run('docker start {name}'.format(name=name), warn=True)

    else:
        if noisy:
            color('docker [{name}] already start'.format(name=name))
        do_output = False

    if do_output and output:
        print(output)

    """ 总是重新设置network
    """
    if host:
        net.address(c, name=name, host=host, local=local)


########################################################################################################################
def clean_docker(c):
    if stdouted(c, 'docker ps -aq'):
        color('clean docker')
        c.run('docker rm -f  $(docker ps -aq)')
        # c.run('docker ps -a')
    else:
        color('no docker to clean', False)


def clean_image(c, total=False, ignore='fabric|centos'):
    if stdouted(c, 'docker images -q -f dangling=true'):
        color('clear dangling images!')
        c.run('docker rmi -f $(docker images -q -f dangling=true)')

    """
        docker images：显示所有image，包括dangling
        docker images -a：显示所有image，包括其他image所被依赖的

        1. docker rmi -f $(docker images -aq)  删除所有
        2. docker images | egrep "({ignore})" | awk '{{print $3}}'                  找到无需过滤的那些 image id
        3. docker images | egrep -v "({ignore})" | awk '{{print $3}}' | sed '1d'    找到需要过滤的那些 image id

        用方法2
    """
    list = c.run('''docker images -q''').stdout.replace('\n', ' ')

    if not total:
        keep = c.run('''docker images | egrep "({ignore})" | awk '{{print $3}}' '''
                     .format(ignore=ignore)).stdout.replace('\n', ' ')
        for k in keep.split(' '):
            list = list.replace(k, '')

    list.strip()
    if list:
        color('clean images')
        c.run('echo {list} | xargs docker rmi -f'.format(list=list))
    else:
        color('no image to clean', False)


def clean_resource(c):
    color('clean volume')
    c.run('docker volume prune -f')

    color('clean network')
    c.run('docker network prune -f')
    # c.run('docker network ls')
    # c.run('docker volume ls')


########################################################################################################################
def start_http(c, type, **kwargs):
    kwargs = Dict(kwargs)
    start_images(c, type, 'http', port=local.http_port, http=False, proxy=False, noisy=False)

    kwargs.path = args_def(kwargs.path, local.http_path[0])
    kwargs.port = args_def(kwargs.port, local.http_port)
    output = 'http: port [{port}], path [{path}]'.format(port=kwargs.port, path=kwargs.path)

    volume = '{}:{}'.format(kwargs.path, local.http_path[1])
    kwargs.port = '{out}:{ins}'.format(out=kwargs.port, ins=local.http_port)

    build_docker(c, type, name='http', volume=volume, http=False, proxy=False, noisy=False, output=output, **kwargs)


def start_proxy(c, type, **kwargs):
    kwargs = Dict(kwargs)
    start_images(c, type, 'proxy', http=False, proxy=False, noisy=False)

    kwargs.port = local.proxy_port
    kwargs.path = args_def(kwargs.path, local.proxy_path[0])
    output = 'proxy: path [{path}]'.format(path=kwargs.path)

    volume = '{}:{}'.format(kwargs.path, local.proxy_path[1])
    build_docker(c, type, name='proxy', volume=volume, http=False, proxy=False, noisy=False, output=output, **kwargs)


def sshd_image(c, type, **kwargs):
    start_images(c, type, 'sshd', noisy=False, **kwargs)


########################################################################################################################
def prepare_docker(c, http=local.use_http, proxy=local.use_proxy, **kwargs):
    if http:
        start_http(c, -1)

    if proxy:
        start_proxy(c, -1)

    if local.images_count > 0 or local.docker_count > 0:
        color('create prepre completed, wait to continue ... ')


def prepare_images(c, name):
    valid = ['sshd', local.centos[0], local.fabric[0]]

    if name == 'sshd':
        sshd_image(c, -1)

    elif name in valid:
        pass
    else:
        print('prepare images, but image [{name}] not exist, valid {valid}'.format(name=name, valid=valid))
        exit(-1)


def start_images(c, type, name, base='', port=0, http=local.use_http, proxy=local.use_proxy, **kwargs):
    """ 创建image
            1. dockerfile 默认是 0_server：可用于生成sshd、其他server等
            2. base：为空：新生成的image，并且名字与 name 一致，通常是生成了不同 server 自己的 image
                     非空：基于某个已存在的image，建立docker后，再进行安装

            3. port：只用于设置dockerfile中的 expose，用于声明作用
            4. http：传递给image构建脚本 server.sh，设置镜像的 yum
    """
    basing_images(c)

    if base:
        prepare_images(c, base)

    else:
        """ 将所有参数用引号封装 -> dockerfile run shell -> 传递给 server.py 解析出来
        """
        param = ''
        param = sep(param, args(name, '--server '), ' ')
        param = sep(param, args(http, '--http', ignore=True), ' ')
        param = sep(param, args(proxy, '--proxy', ignore=True), ' ')

        build_images(c, type, image=name, dockerfile=local.server, build=args(port, 'LISTEN='), param=args(param, '"', '"'), **kwargs)


def start_docker(c, type, name, base='', enter=False, **kwargs):
    """ 准备工作
    """
    start_images(c, type, name, base=base, **kwargs)

    prepare_docker(c, **kwargs)

    """ 启动容器
    """
    build_docker(c, type, name=name, image=base, **kwargs)

    """ 当前进入新创建的 docker
    """
    if enter:
        helps.sshd(c, name, host=local.flag.host)
        c.run('docker exec -it {name} /bin/bash'.format(name=name), echo=False, pty=True)
    else:
        helps.result(c, name, **kwargs)
        helps.sshd(c, name, host=local.flag.host)