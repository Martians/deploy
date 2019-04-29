# coding=utf-8

from invoke import task
from common import *
import system

"""
    1. 自动编译，结果复制到 include、lib 目录中
"""
class LocalConfig(LocalBase):
    """ 默认配置
    """
    def __init__(self):
        LocalBase.__init__(self, 'kafka')

        self.conf = 'depend.base'
        self.base = xdata(conn(invoke=True), self.conf)

        self.temp = 'builds'
        self.prefix = 'prefix'

        self.name = ['gtest', 'glog', 'gflags', 'gflags']
        self.nmap = {'gtest': 'googletest', 'gprof': 'pprof'}


""" 提供个默认参数
    
    该变量定义在头部，这样在函数的默认参数中，也可以使用了
"""
local = LocalConfig()

@task
def build(c, name):
    if not local.base:
        print('not find conf base path in ~/.local.yaml')
        exit(-1)

    """ fab build [name | all]
    """
    if name == 'all':
        for n in local.name:
            build(c, n)
        return

    c.run('mkdir -p {base}/include; mkdir -p {base}/lib'.format(base=local.base))

    name = local.nmap[name] if name in local.nmap else name
    dest = '{base}/{name}'.format(base=local.base, name=name)

    with c.cd(dest):
        if file_exist(c, 'CMakeLists.txt'):
            build_cmake(c, dest)

        else:
            build_automake(c, dest)


def build_cmake(c, dest):
    c.run('mkdir -p {temp}'.format(temp=local.temp))

    with c.cd(local.temp):
        c.run('cmake -DCMAKE_INSTALL_PREFIX={prefix} ..'.format(prefix=local.prefix))
        c.run('make -j4 && make install')
        copy(c, local.prefix)


def build_automake(c, dest, use_prefix=False):
    if not file_exist(c, 'configure'):
        c.run('PATH=$PATH:/usr/local/bin/ ./autogen.sh')

    c.run('./configure --prefix={dest}/{prefix}'.format(dest=dest, prefix=local.prefix))
    c.run('make -j4 && make install')

    copy(c, local.prefix)


def copy(c, prefix):
    c.run('\cp -rf {prefix}/include {base}'.format(prefix=prefix, base=local.base))

    if file_match(c, '{prefix}/lib/*.a '.format(prefix=prefix)):
        c.run('\cp -rf {prefix}/lib/*.a {base}/lib'.format(prefix=prefix, base=local.base), echo=True, warn=True)

    if file_match(c, '{prefix}/lib/*.so '.format(prefix=prefix)):
        c.run('\cp -rf {prefix}/lib/*.so {base}/lib'.format(prefix=prefix, base=local.base), echo=True, warn=True)

@task
def path(c, path=''):
    """ 设置3rd repo的路径
    """
    if path:
        xdata(c, local.conf, path)
    else:
        print('[using path]: {}'.format(xdata(c, local.conf)))

# @task
# def help(c):
#     system.help(c, '''
#         fab build [name | all]''')

if __name__ == '__main__':
    set_invoke(True)
    c = conn(hosts.conn(0))
    # build(c, 'gflags')
    # build(c, 'glog')
    # build(c, 'gtest')
    # build(c, 'protobuf')
    build(c, 'all')