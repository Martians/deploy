# coding=utf-8
import os

from fabric import Connection, SerialGroup as Group, Config, task

from common.init import *
from common.pack import *

import common.hosts as hosts
import common.sed as sed
from componet.ignite import ignite

""" 1. slave节点，与simplebench中，配置的节点个数保持一致
    2. 
"""

@task
def coding(c):
    c.run("mkdir -p {}".format(os.path.dirname(c.install.work)))
    if not file_exist(c, c.install.work, "", dir=True):
        git_url = 'http://gitlab.internal.nimblex.cn/guijichaxun/SimpleBenchmark'
        c.run("git clone {} {}".format(git_url, c.install.work), pty=True)

    master_copy(c, c.install.work + "/scripts", '/opt/ignite/', other=False)

@task()
def update(c):
    """ update java package
    """
    with c.cd(c.install.work):
        c.run("mvn package")
        master_copy(c, "target/*.jar", '/opt/ignite/libs', other=False)

@task
def install(c):
    ignite.prepare(c)
    ignite.install(c)

    coding(c)
    update(c)

@task
def clean(c):
    ignite.clean(c)
    # hosts.execute("rm -rf {}".format(c.install.work))

c = hosts.conn(0)
# install_total()
# hosts.conn(1).run("echo $IGNITE_HOME", replace_env=False)
# sed.append(hosts.conn(0), 'IGNITE_HOME', '/opt/ignite', '/etc/profile')

