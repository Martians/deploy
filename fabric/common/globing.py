# coding=utf-8
import os

from common.util import *

""" 默认配置内容
"""
globing = Dict({
    # 全局路径
    'path': os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")),

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