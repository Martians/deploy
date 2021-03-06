# coding=utf-8
import os

from common.util import *

""" 默认配置内容
"""
globing = Dict({
    # 全局路径
    'path': os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")),
    'user': os.path.expanduser('~'),

    # 当前在docker中，执行本地任务
    'invoke': False,

    'config': {
        'hosts': 'hosts.yaml'
    },
    'source': {
        'parent': '/opt',
        'source': '/home/long/source'
    }
})


def load_yaml(file):
    import yaml
    with open(file, 'r') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        return Dict(data) if data else Dict()


def write_yaml(file, data):
    import yaml
    with open(file, 'w') as f:
        yaml.dump(data.dict(), f, default_flow_style=False)


def set_yaml(file, key, value):
    """ 先将数据都load出来，更新后再dump

        方式1）：从外到内
            c = data; while(loop k) { c.k = Dict(); c = c.k }
            失败：无法递归修改 dict 的值，放在dickt中value已经是值了，无法再进行修改
            考虑转成字符串，然后在eval回来？eval('data.{k} = Dict()'.format(k=k))

        方式2）：从内到外
    """
    data = load_yaml(file)

    range = key.split('.')
    range.reverse()
    d = value
    for k in range:
        d = Dict({k : d})

    data.update(d)
    write_yaml(file, data)


def get_yaml(file, key):
    c = load_yaml(file)
    for k in key.split('.'):
        c = c.get(k)
        if not c: return None
    return c


def default_config_path(name, type):
    entries = {'curr': lambda: os.path.join(os.getcwd(), name),
               'user': lambda: '{}/{}'.format(globing.user, name),
               'glob': lambda: '/etc/{}'.format(name),
               'module': lambda: os.path.join(os.path.abspath(globing.path), name)}

    path = entries.get(type)()
    if os.path.exists(path):
        return path
    else:
        return None


def search_config(name, merge=False, high='', low=''):
    """ 在多个位置查找配置文件

        优先级：high、当前目录、用户目录、全局目录、顶层目录、low
    """
    lists = []
    for type in ['curr', 'user', 'glob', 'module']:
        path = default_config_path(name, type)
        if path:
            if merge:
                lists.append(path)
            else:
                return path
    if merge:
        if high:
            for path in high.split(','):
                path = os.path.join(path, name)
                if os.path.exists(path):
                    lists.insert(0, path)
        if low:
            for path in low.split(','):
                path = os.path.join(path, name)
                if os.path.exists(path):
                    lists.append(path)
        lists.reverse()
        return lists
    else:
        print('not find {}!'.format(name))
        exit(-1)


def parse_config_list(path, withdraw=True):
    """ 将传入的 list，依次进行merge
        注意：这里是递归 merge（如不是递归方式，只能进行第一册的替换）
    """
    config = Dict()

    if isinstance(path, str):
        config = load_yaml(path)
    else:
        for file in path:
            file = load_yaml(file)
            """ config.update(file) 无法进行递归的 update
            """
            config.updating(file)

    if withdraw:
        config.withdraw()
    return config


def parse_config(name, merge=False, withdraw=True, high='', low=''):
    path = search_config(name, merge, high=high, low=low)
    return parse_config_list(path, withdraw=withdraw)


def parse_traverse(search, withdraw=True):
    """ 使用单独的路径，进行递归查找
    """
    collect = []

    def traverse(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.find('yaml') != -1 or file.find('yml') != -1:
                    collect.append(os.path.join(root, file))

            for dir in dirs:
                if not dir.startswith('_'):
                    traverse(os.path.join(root, dir))
            break
    traverse(search)

    return collect, parse_config_list(collect, withdraw=withdraw)


def str_enum(valid):
    import re
    result = re.split('[|,]', valid)

    enums = []
    for item in result:
        enums.append(item)
    return enums


def str_enum_exist(enums, strs, exist):
    if not strs:
        return
    """ 全集合为：enums
        当前配置：strs
        当前检测：exist
    """
    import re
    result = re.split('[|,]', strs)

    for item in result:
        if item not in enums:
            print('enum [{}] not in {}'.format(strs, enums))
            exit(-1)
    return exist in result