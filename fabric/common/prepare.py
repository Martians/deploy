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


def auto_complete():
    """ 没法做成自动的：
            1. 这里必须执行 fab 命令才能获取脚本；
            2. fab 程序的位置不好判断（特别是安装了 vypenv 这种，需要正常登陆才会加载）；只能通过执行fab时获取其位置
    """
    # home = os.path.expanduser('~')
    #
    # import sys
    # c = Connection("127.0.0.1")
    # c.local('''echo '{fab} --print-completion-script bash > {home}/.fabric-completion.sh' > /tmp/auto;'''.format(fab=sys.argv[0], home=home))
    #
    # import common.sed as sed
    # sed.append(c, 'source ~/.fabric-completion.sh', file='~/.bashrc')

    print('''
auto complete：
    fab --print-completion-script bash > ~/.fabric-completion.sh
    echo "source ~/.fabric-completion.sh" >> ~/.bashrc
    source ~/.bashrc ''')


search_path()
auto_complete()

