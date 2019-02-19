# coding=utf-8

from invoke import task
from common import *
import system


class LocalConfig(LocalBase):
    def __init__(self):
        LocalBase.__init__(self, 'docker')
        self.base = ('centos:base', '0_centos')
        self.sshd = ('centos:server','0_server')


local = LocalConfig()


def execute(c, cmd):
    return len(c.run(cmd, echo=False, hide=True).stdout) > 0


def color(string, newline=True):
    print("{newline}\033[1;32;40m{string}\033[0m".format(string=string, newline='\n' if newline else ''))


def build_image(c, name, file, exec=''):
    if execute(c, 'docker images {image} -q'.format(image=name)):
        print('image [{image}] already exist'.format(image=name))
    else:
        c.run('docker build -t {image} -f template/{dockerfile} {exec} .'.
                format(image=name, dockerfile=file, exec=exec))

def build_base(c):
    build_image(c, local.base[0], local.base[1])

@task
def install(c):
    build_image(c, local.base[0], local.base[1])

@task
def clean(c, all=False, docker=False, image=False, resource=False):
    if all:
        docker=True
        image=True
        resource=True

    if execute(c, 'docker images -q -f dangling=true'):
        color('clear dangling images!')
        c.run('docker rmi -f $(docker images -q -f dangling=true)')

    if docker:
        if execute(c, 'docker ps -aq'):
            color('clean docker')
            c.run('docker rm -f  $(docker ps -aq)')
            # c.run('docker ps -a')
        else:
            color('no docker', False)

    if image:
        if execute(c, 'docker images -aq'):
            color('clean images')
            c.run('docker rmi -f $(docker images -aq)')
            # c.run('docker images -a')
        else:
            color('no image', False)

    if resource:
        color('clean volume')
        c.run('docker volume prune -f')

        color('clean network')
        c.run('docker network prune -f')
        # c.run('docker network ls')
        # c.run('docker volume ls')

@task
def proxy(c):


@task
def sshd(c):
    build_base(c)


if __name__ == '__main__':
    sshd(hosts.conn(0))