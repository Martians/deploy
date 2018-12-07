# coding=utf-8
import os

from fabric import Connection, SerialGroup as Group, Config

from common.pack import *
from common.disk import *
import common.sed as sed

def compile_redis(c, compile_path, install_path):
    with c.cd(compile_path):
        if not file_exist(c, 'src', 'redis-server'):
            c.run("make MALLOC=libc -j5")
        c.run("mkdir -p {}".format(c.install.path))
        c.run("sudo \\cp src/redis-server src/redis-cli /usr/local/bin".format(""))
        c.run("sudo \\cp src/redis-server src/redis-cli redis.conf {}".format(install_path))


def install_master(c):
    download(c, "redis", c.install.source, c.install.compile)
    compile_redis(c, c.install.compile, c.install.path)


def config_master(c):
    file = c.install.path + "/redis.conf"
    # sed.update(c, "bind", "0.0.0.0", file=file)
    # sed.update(c, "daemonize", "yes", file=file)
    # sed.update(c, "logfile", "server.log", file=file)
    # sed.update(c, "stop-writes-on-bgsave-error", "no", prefix=".*", file=file)

    # sed.enable(c, "cluster-enabled", "yes", file=file)
    # sed.enable(c, "cluster-config-file", "nodes.conf", prefix=".*", file=file)

    sed.update(c, "save", ".*", file=file)

# sudo sed -i "s#\(^bind \).*#\10.0.0.0#g" redis.conf
# sudo sed -i "s#\(^daemonize \).*#\1yes#g" redis.conf
# sudo sed -i "s#\(^logfile \).*#\1server.log#g" redis.conf
# sudo sed -i "s#.*\(cluster-enabled \).*#\1yes#g" redis.conf
# sudo sed -i "s#.*\(cluster-config-file \).*#\1nodes.conf#g"  redis.conf
# sudo sed -i "s#.*\(stop-writes-on-bgsave-error \).*#\1no#g" redis.conf
# sudo sed -i "s#\(^save .* \)#\#\1#g" redis.conf

from common.common import *
from common.hosts import *
# install_master(conn(0))
config_master(conn(0))