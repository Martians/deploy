# coding=utf-8

from invoke import task
from common import *
import system
from docker.image import *


@task
def install(c):
    build_images(c, local.base[0], local.base[1])


@task
def clean(c, total=False, docker=False, image=False, resource=False):
    if total:
        docker = True
        image = True
        resource = True

    """ total：清理全部，不保留任何image
        image: 删除image，保留ignore
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

@task
def proxy(c, type=-1, path=local.proxy_path[0]):
    """ 单独启动 proxy，可以指定更多参数
    """
    start_proxy(c, type, path=path)

@task
def sshd(c, type=-1, port=local.sshd_port):
    """ 基于sshd镜像，启动 sshd docker
    """
    start_sshd(c, type, port=port)

@task
def cluster(c, type=-1, **kwargs):
    start_docker(c, type)


@task
def test(c, type=-1, name='test', base='sshd', port='', exec='/bin/bash', systemd=False):
    """ 根据base生成的纯净版本，可用于构建测试程序，见：prepare_images
    """
    start_docker(c, type, name, base=base, port=port, exec=exec, systemd=systemd, enter=True)


if __name__ == '__main__':
    # sshd(hosts.one(), 0)
    globing.invoke = True
    test(conn(hosts.one()), type=0, port=90)