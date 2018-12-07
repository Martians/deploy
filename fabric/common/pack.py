# coding=utf-8

from common.disk import *


def download(c, pack_name, http_source, install_path, temp_path="/tmp"):
    # 目标位置已经安装   /opt/redis
    if file_exist(c, install_path, dir=True):
        print("install path [{}] already exist".format(install_path))
        # c.run("mkdir -p {}".format(install))
        return 1

    # 下载：到临时目录下 /tmp/redis-5.0.0.tar.gz
    package = os.path.basename(http_source)
    if not file_exist(c, temp_path, package):
        c.run("wget {} -P {}".format(http_source, temp_path))

    # 解压：到目标目录的父目录下 /opt/redis-5.0.0
    base_path = os.path.dirname(install_path)
    if not file_search(c, base_path, pack_name, dir=True):
        c.run("tar zxvf {}/{} -C {} ".format(temp_path, package, base_path))

    # move：将解压出来的文件move，/opt/redis
    actual = file_search(c, base_path, pack_name, dir=True)
    c.run("mv {}/{} {}".format(base_path, actual, install_path))
    return 0
