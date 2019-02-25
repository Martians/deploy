# coding=utf-8

from invoke import task
from common import *
import system
from docker.image import *
from docker import helps
from docker import network as net

@task
def install(c):
    build_images(c, local.base[0], local.base[1])


@task
def clean(c, total=False, docker=False, image=False, resource=False):
    """ -di 删除所有docker、大部分image（保留centos、fabric）
    """
    if total:
        docker = True
        image = True
        resource = True

    """ total：清理全部，不保留任何image
        image: 删除image，保留ignore（但必须先清理相关docker）
    """
    if docker:
        clean_docker(c)

    if image:
        clean_image(c, total)

    if resource:
        clean_resource(c)

@task
def help(c):
    c = conn(c, True)
    system.help(c, '''
        docker history centos:base
        docker images centos:test
        '''.format())

@task
def http(c, type=-1, port=local.http_port, path=local.http_path[0]):
    """ 单独启动 http，可以指定更多参数
    """
    start_http(c, type, port=port, path=path)
    helps.result(c, name='http', port=port)

@task
def proxy(c, type=-1, path=local.proxy_path[0]):
    """ 单独启动 proxy，可以指定更多参数
    """
    start_proxy(c, type, path=path)
    helps.result(c, name='proxy', port=3142)
    helps.proxy(c, name='proxy')

@task
def sshd(c, type=-1, name='sshd', systemd=True, addr='sshd', enter=True):
    """ 基于sshd镜像，启动 sshd docker
    """
    start_docker(c, type, name, base='sshd', exec='/bin/bash', systemd=systemd, host=addr, enter=enter)

@task
def cluster(c, name='sshd', systemd=True, count=3):
    for i in range(1, count + 1):
        sshd(c, -1, name='{}-{}'.format(name, i), systemd=systemd, addr='h{}'.format(i), enter=False)

@task
def test(c, type=-1, name='test', base='sshd', port='', exec='/bin/bash', systemd=True, addr='test', enter=True):
    """ 构架测试场景

        1. 指定基础镜像：指定base生成纯净版本，可用于构建测试程序，可选项详见：prepare_images
        2. 内部执行安装：cd /fabric/docker; python3 server.py --server mariadb
    """
    start_docker(c, type, name, base=base, port=port, exec=exec, systemd=systemd, host=addr, enter=enter)

@task
def network(c, force=True):
    net.prepare_network(c, force=force)

@task
def mariadb(c, type=-1, name='mariadb', addr='sshd', enter=False):
    sshd_server(c, type, name, host=addr, enter=enter)


if __name__ == '__main__':
    globing.invoke = True
    c = conn(hosts.one())

    sshd(c, 1)
    # http(c, type=0)
    # mariadb(c, 0)
    # test(c)