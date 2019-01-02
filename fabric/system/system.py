# coding=utf-8

from common import *


def kill(name, string=False, pkill=True, conns=None):
    if pkill:
        command = 'pkill -9 {name}'.format(name=name)
    else:
        command = "ps aux | grep {name} | grep -v grep | awk '{{print $2}}' | xargs kill -9".format(name=name)

    if string:
        return command
    else:
        return hosts.execute(command, err=False, conns=conns)


def help(c, display, name='help'):
    display = display.replace('\n        ', '\n    ')
    c.run('''echo; echo '{name}: {display}' '''.format(name=name, display=display), echo=False)
