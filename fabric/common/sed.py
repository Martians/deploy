# coding=utf-8

import common.config as work

""" 使用方式：
        1. 测试完成后，使用 vimdiff 查看改动是否成功
"""


def grep(c, key, value=None, prefix='[^#]*', suffix='', sep=' ', file=None):
    return work.grep_data(c, key, value=value, prefix=prefix, suffix=suffix, sep=sep, file=file)


def update(c, key, value=None, prefix='^', suffix='', sep=' ', file=None):
    return work.update(c, key, value=value, prefix=prefix, suffix=suffix, sep=sep, file=file)


def enable(c, key, value=None, prefix='^#.*', suffix='', sep=' ', file=None, grep_prefix="^[^#]*"):
    """ 取消#前缀，并修改
        1. 查找时使用 prefix：^[^#]*
        2. 修改时使用 prefix：^#.*

        构造起来比较麻烦，这里取消update之前、之后的grep检查
    """
    return work.update(c, key, value=value, prefix=prefix, suffix=suffix, sep=sep, file=file, grep_prefix=grep_prefix)


def disable(c, key, value=None, prefix='^', suffix='', sep=' ', file=None, result_prefix='# '):
    """ 增加#前缀
    """
    if work.grep_data(c, key, value=value, prefix=prefix, suffix=suffix, sep=sep, file=file):
        return work.update(c, key, value='\1', prefix=prefix, suffix=suffix, sep=sep, file=file, result_prefix=result_prefix, prepare=False, check=False)
    else:
        return 0


def append(c, key, data=None, file=None, pos=0):
    return work.append(key=key, data=data, file=file, pos=pos)


''' 考虑内容
    1. 更新前查找：grep prefix、suffix
    2. 查找后更改：new  prefix、suffix
    3. 更改后验证：grep prefix、suffix
    
    简化操作：
    1. 只传入^[.*]*key，即可分离出 prefix、key
    2. value中识别 \1
'''

''' 测试用例
    1. 删除前缀#，并修改 key + value
    2. 增加前缀#，并保持 # key + value
'''