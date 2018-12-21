# coding=utf-8

import os

''' search.replace('-', '\-')
'''
class Local:
    test = True

    grep_update = {'raw': '',      # 传递给grep命令本身
                   'sed': False,   # 使用sed替换grep
                   'prefix': '[^#]*',
                   'suffix': '',
                   'sep': ' ',
                   'more': '',     # grep时，添加到sep后边，允许多个sep重复
                   'head': '',
                   }
    grep_append = {'sed': True}

    sed_update = {'tag': '|',
                  'end': 'g',
                  'holder': '.*'}


    """ 初始化工作
    """
    def __init__(self):
        # 提供执行grep、sed时的，command执行模式
        self.run = {'warn': True, 'hide': True}
        self.update_check = {'pre': True, 'post': True}

        self.multi = 'NNN'
        self.init_option()

        if self.test:
            self.debug = False  # 显示更多测试信息
            self.cache = ''     # 测试数据
            self.result = ''    # 测试结果
            self.exit_on_err = False

            self._file = 'conf_file'
            self.path = os.path.join(os.getcwd(), self._file)
        else:
            self.exit_on_err = True

    def _path(self, file):
        return file if file else self.path

    def init(self, c, file):
        return c, self._path(file)

    def file(self, path):
        """ 显示时方便查看，截短
        """
        return path.split('/')[-1]

    def initial(self, cache):
        """ 设置test时的数据源
        """
        self.cache = cache.strip('\n')

    ########################################################################################
    def init_option(self):
        temp = self.grep_update.copy()
        temp.update(self.grep_append)
        self._grep_append = temp

        temp = self.grep_update.copy()
        temp.update(self.sed_update)
        self._sed_update = temp

    def grep_option(self, **kwargs):
        """ 提取参数中的grep选项，并提供默认值

                用新传入的配置，覆盖默认配置后返回
                for_append: 用于append时操作
        """
        option = kwargs.get('grep')
        if kwargs.get('for_append'):
            current = self._grep_append.copy()
        else:
            current = self.grep_update.copy()

        if option:
            current.update(option)
        return current

    def sed_option(self, **kwargs):
        """ 默认值中包含了 grep_option 中的选项
        """
        option = kwargs.get('sed')
        current = self._sed_update.copy()

        if option:
            current.update(option)
        return current

    def grep(self, **kwargs):
        if kwargs.get('for_append'):
            self._grep_append.update(kwargs)
        else:
            self.grep_update.update(kwargs)
        self.init_option()

    def sed(self, **kwargs):
        self._sed_update.update(kwargs)

    def show_option(self, count):
        """ grep时，显示的行数选项
        """
        if count:
            return '-{type} {count} '.format(type='A' if count >= 0 else 'B', count=abs(count))
        else:
            return ''

    def check(self, option):
        current = self.update_check.copy()
        if option:
            current.update(option)
        return current


def arg(kwargs, name, blank=False):
    """ 工具函数
            blank：存在而且不为空，添加' '后缀
    """
    if name in kwargs:
        if blank and kwargs[name]:
            return kwargs[name] + ' '
        else:
            return kwargs[name]
    else:
        return ''


if True:
    from fabric import Connection
    c = Connection('127.0.0.1')

    def initial(info, cache):
        local.initial(cache)
        print("\n########################################################################## {}",format(info))

    def output(info):
        print("\n--------------------------------------------------------------------------- {info}:".format(info=info))

    def check(v1, v2):
        """ 数据写入到文件后用diff比较
        """
        if v1 != v2:
            c.run('''echo '{}' > /tmp/v1; echo '{}' > /tmp/v2'''.format(v1, v2), echo=False)
            c.run('diff /tmp/v1 /tmp/v2', warn=True)
            exit(-1)

    def match(v):
        check(v.strip('\n'), local.result.strip('\n'))

local = Local()
