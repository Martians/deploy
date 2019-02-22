# coding=utf-8

from common import *


class LocalConfig:
    def __init__(self):
        # self.hide = 'out'
        self.hide = None


local = LocalConfig()


def package(type='', single='', centos=True):
    list = {'source': 'epel-release',
            'common': 'psmisc',
            'compile': 'gcc make',
            'java': 'java-1.8.0-openjdk-devel',
    }
    if list.get(type):
        batch = list.get(type)
    else:
        batch = type

    if centos:
        return 'yum install -y {}{}'.format(batch + ' ' if batch else '', single)
    else:
        return ''


def install(c, type='', single='', hide=local.hide, centos=True):
    """ system.install(c, 'group_name', 'single1 single2')
        system.install(c, 'single1 single2')
    """
    command = package(type=type, single=single, centos=centos)
    if c:
        c.run(command, hide=hide, pty=True)
    else:
        hosts.execute(command, hide=hide, pty=True)

# install(hosts.conn(0), "java")