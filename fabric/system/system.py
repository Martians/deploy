# coding=utf-8

from common import *


def grep_handle(result):
    return result.stdout.count('\n') > 0


def grep_output(result):
    data = result.stdout.strip('\n')
    if data:
        return 'pid: {}'.format(data)
    else:
        return ''


def group(command, **kwargs):
    return hosts.execute(command, **args_def(kwargs, go_on=True))


def grep(name, string=False, output=None, **kwargs):
    command = "ps aux | grep {name} | grep -v grep | awk '{{print $2}}'".format(name=name)
    if string:
        return command
    else:
        return group(command, handle=grep_handle, output=output, **kwargs)


def kill(name, string=False, pkill=True, **kwargs):
    if pkill:
        command = 'pkill -9 {name}'.format(name=name)
    else:
        command = "ps aux | grep {name} | grep -v grep | awk '{{print $2}}' | xargs kill -9".format(name=name)

    if string:
        return command
    else:
        return group(command, **kwargs)


def help(c, display, name='help'):
    display = display.replace('\n        ', '\n    ')
    c.run('''echo; echo '{name}: {display}' '''.format(name=name, display=display), echo=False)


########################################################################################################################
def start(name, command, force=False, **kwargs):
    """ 先检查服务是否已经启动
    """
    if not force:
        conns = hosts.conns_filter(grep(name, string=True), handle=grep_handle, reverse=True, **kwargs)
    else:
        conns = hosts.conns(**kwargs)

    if len(conns):
        return group(command, **kwargs)
    else:
        print("all server already start".format())


def stop(name, exec='', dir='', **kwargs):
    if exec:
        dir = 'cd {}; '.format(dir) if dir else ''
        hosts.execute('{dir}{exec}'.format(dir=dir, exec=exec), **kwargs)
    else:
        kill(name, **kwargs)


def stat(name, **kwargs):
    grep(name, out=True, output=grep_output, **kwargs)


def clean(dirs='', disk=True, **kwargs):
    remove = ''
    for dir in dirs.split(','):
        remove = sep(remove, dir, ' ')

    if remove:
        hosts.execute('sudo rm -rf {}'.format(remove), hide=None, **kwargs)

    if disk:
        for index in hosts.lists(**kwargs):
            c = hosts.conn(index)

            for disk in hosts.item(index, 'disk', ',').split(','):
                c.run("sudo rm -rf {}/*".format(disk), pty=True)
