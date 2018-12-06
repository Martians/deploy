# coding=utf-8
import os

from fabric import Connection, SerialGroup as Group, Config


def enable(c, f):
    c.config.run.warn = False if f else True


def download(c, pack_name, http_source, install_path, tar_path="/tmp"):
    if c.run("[ -d {} ]".format(install_path)).ok:
        print("install path [{}] already exist".format(install_path))
        # c.run("mkdir -p {}".format(install))
        return 1

    # 下载 package
    package = os.path.basename(http_source)
    if c.run("[ -f {}/*{} ]".format(tar_path, package)).failed:
        c.run("wget {} -P {}".format(http_source, tar_path))

    temp_path = os.path.dirname(install_path)
    c.run("tar zxvf {}/{} -C {} ".format(tar_path, package, temp_path))
    c.run("mv {}/*{}* {}".format(temp_path, pack_name, install_path))
    return 0


def compile_redis(c, compile_path, install_path):
    with c.cd(compile_path):
        if c.run("[ -f src/redis-server ]").failed:
            c.run("make MALLOC=libc -j5")
            c.run("\cp src/redis-server src/redis-cli /usr/local/bin".format(""))
            c.run("\cp src/redis-server src/redis-cli redis.conf {}".format(compile_path, install_path))


def install_master(c):
    download(c, "redis", c.install.source, c.install.compile)
    compile_redis(c, c.install.compile, c.install.path)
    print("=========")