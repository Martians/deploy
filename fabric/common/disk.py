# coding=utf-8


def file_exist(c, path, name=None, dir=False):
    return c.run(_file_exist_command(path, name, dir), warn=True).ok


def _file_exist_command(path, name=None, dir=False):
    """ 模糊名字查找
    """
    flag = 'd' if dir else 'f'
    if name:
        path = '{}/*{}*'.format(path, name)
    return "[ -{} {} ]".format(flag, path)


def _file_result(path, name, result):
    file_list = result.stdout.strip().split('\n')

    if len(file_list) == 1:
        return file_list[0]

    elif len(file_list) > 1:
        print("too much similar item [{}] matched in {}:\n\t {}".format(name, path, file_list))
        exit(-1)

    return None


def file_actual(c, path, name, dir=False):
    """ 模糊名字匹配

        更多方式：https://blog.csdn.net/ialexanderi/article/details/79021312
    """
    flag = 'd' if dir else '^d'
    result = c.run("ls -l {} | grep ^[{}] | awk '{{print $9}}' | grep {}".format(path, flag, name), warn=True)
    return _file_result(path, name, result)


def file_search(c, path, name, suffix=None, dir=False):
    """ https://linux.cn/article-1672-1.html
    """
    flag = 'd' if dir else 'f'
    suffix = suffix if suffix else "|"

    for s in suffix.split("|"):
        result = c.run('sudo find {} -follow -type {} -name "*{}*{}"'.format(path, flag, name, s), warn=True)
        item = _file_result(path, name, result)
        if item: return item
    return None


if __name__ == '__main__':
    from fabric import Config, Connection
    from common.init import *
    c = hosts.conn(0)

    file_search(c, "/home/long/source", 'redis')
    file_search(c, "/home/long/source", 'redis', suffix="zip|tar.gz")
    file_search(c, "/home/long/source", 'redis', suffix="tar.gz")
    file_search(c, "/home/long/source", 'ignite', suffix="zip")
