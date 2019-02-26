
from invoke import task, Collection, Config

from common.init import *
from common.show import *

@task
def config(c, fabric=False, size=-1):
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
        sed.update(c, '    - size:', str(size), file=dst)

    else:
        """ 显示各种配置
        """
        print('hosts config  ----- [{}]'.format(search_config(globing.config.hosts)))

        lists, config = config_server()
        if len(lists):
            print('server config ----- [{}]\n'.format(lists[0]))
        else:
            print('')

        if fabric:
            print('fabric config: ')
            print(Config())
        else:
            print('hosts config: ')
            hosts.print()

@task
def kill(c, name):
    import system
    system.process.kills(name)

config(hosts.one(), size=3)