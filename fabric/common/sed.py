# coding=utf-8

import common.config as work


def grep(c, key, value=None, prefix='[^#]*', suffix='', sep=' ', file=None):
    return work.grep_data(c, key, value=value, prefix=prefix, suffix=suffix, sep=sep, file=file)


########################################################################################################################
def update(c, key, value=None, prefix='^', suffix='', sep=' ', file=None):
    return work.update(c, key, value=value, prefix=prefix, suffix=suffix, sep=sep, file=file)


''' 取消#前缀，并修改 
        1. 查找时使用 prefix：^[^#]*
        2. 修改时使用 prefix：^#.*
    
    构造起来比较麻烦，这里取消update之前、之后的grep检查
'''
def enable(c, key, value=None, prefix='^#.*', suffix='', sep=' ', file=None, grep_prefix="^[^#]*"):
    return work.update(c, key, value=value, prefix=prefix, suffix=suffix, sep=sep, file=file, grep_prefix=grep_prefix)


''' 增加#前缀
'''
def disable(c, key, value=None, prefix='^#.*', suffix='', sep=' ', file=None, grep_prefix="^[^#]*", result_prefix='# '):
    return work.update(c, key, value=value, prefix=prefix, suffix=suffix, sep=sep, file=file, grep_prefix=grep_prefix, result_prefix=result_prefix)


########################################################################################################################
def append(c, key, data=None, file=None, pos=0):
    return work.append(key=key, data=data, file=file, pos=pos)