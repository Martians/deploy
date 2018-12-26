# coding=utf-8

import sys, os
sys.path.append(os.path.join(os.getcwd(), "../../.."))

from invoke import task
from common.init import *
from common.pack import *

import common.hosts as hosts
import common.sed as sed
import system

class LocalConfig:
    def __init__(self):
        self.source = 'https://github.com/Martians/hadoop.git'
        self.work = '/home/long/work'

        """ name: 从git地址提取的名字
            base：git 根目录
            home：子工程目录
        """
        self.name = os.path.basename(self.source).split('.')[0]
        self.base = os.path.join(self.work, self.name)
        self.home = os.path.join(self.base, 'client')


local = LocalConfig()

print("connect to [{}]".format(hosts.one(True)['host']))

@task
def install(c):
    c = hosts.one()

    c.run("mkdir -p {}".format(os.path.dirname(local.work)))
    if file_exist(c, local.base, dir=True):
        print("project [{}] already cloned".format(local.name))
    else:
        c.run("git clone {} {}".format(local.source, local.base), pty=True)

    # hosts.execute('sudo rm -rf /opt/*kafka*')

@task
def configure(c):
    c = hosts.one()

    sed.append(c, '''
    <mirror>
        <id>alimaven</id>
        <name>aliyun maven</name>
        <url>http://maven.aliyun.com/nexus/content/groups/public/</url>;
        <mirrorOf>central</mirrorOf>
    </mirror>''', '</mirrors>', '/usr/share/maven/conf/settings.xml', -1)

# configure(hosts.conn(0))

@task
def prepare(c):
    system.install(hosts.one(), 'java', 'unzip git')

@task
def package(c):
    c = hosts.one()
    with c.cd(local.home):
        c.run('mvn source')

@task
def clean(c):
    c = hosts.one()
    c.run("rm -rf {}".format(local.base))

# source(c)
