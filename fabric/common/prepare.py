# coding=utf-8

import sys, os


def search_path():
    file = 'project.pth'
    pwd = os.path.dirname(os.path.abspath(__file__))
    root = os.path.abspath(os.path.join(pwd, '..'))

    for path in sys.path:
        if path.endswith('site-packages'):
            dest = '{path}/{file}'.format(path=path, file=file)
            os.system("echo '{root}' > {dest}".format(root=root, dest=dest))
            print("add path [{}], locate: {}".format(root, dest))


search_path()