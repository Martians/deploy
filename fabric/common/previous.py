
from invoke import task, Collection, Config

from common.init import *
from common.show import *

@task
def xconf(c, fabric=False, size=-1):
    host = globing.config.hosts

    if size != -1:
        """ 设置host个数
                如果配置~/hosts.yaml不存在，就复制过去
        """
        src = os.path.join(globing.path, host)
        dst = os.path.join(globing.user, host)
        if not file_exist(c, dst, echo=False):
            print('copy {} to [{}]'.format(src, dst))
            c.run("\cp {} {}".format(src, dst))
        if size > hosts.total:
            color('can not set size [{}], larger than host count [{}]'.format(size, hosts.total))
            exit(-1)

        import common.sed as sed
        sed.mute(True)
        sed.update(c, '    - size:', str(size), file=dst)

        config_hosts()


    else:
        """ 显示各种配置
            1. 当前 fab 执行所在目录下所有的配置
        """
        dst = search_config(globing.config.hosts)
        # print('hosts config  ----- [{}]'.format(dst))

        lists, config = config_server()
        if len(lists):
            print('server config ----- [{}]\n'.format(lists[0]))
        else:
            print('')

        """ 2. fabric 自身的配置
        """
        if fabric:
            print('fabric config: ')
            print(Config())
            print()

    print('hosts config: [{}]'.format(dst))
    hosts.print()

@task
def xkill(c, name):
    import system
    system.process.kills(name)


@task
def xdata(c, key, value=None, file=globing.user + '/.local.yaml'):
    if not os.path.exists(file):
        print(file)
        os.mknod(file)

    if value:
        return set_yaml(file, key, value)
    else:
        return get_yaml(file, key)


if __name__ == '__main__':
    c = conn(invoke=True)
    xdata(c, 'a.d', 'b')
    xdata(c, 'a.d')