# coding=utf-8

import os

''' search.replace('-', '\-')
'''
class Local:
    grep_update = {'raw': '',       # 传递给grep命令本身
                   'sed': False,    # 使用sed替换grep
                   'prefix': '[^#]*',
                   'suffix': '',
                   'sep': ' ',      # key、data之间的分隔符
                   'more': '',      # grep时，添加到sep后边，这样可以允许多个sep重复
                   'head': '',
                   }
    grep_append = {'sed': True}

    sed_update = {'dump_search': True,  # 最后dump结果时，使用/search/replace/g中的search部分，或者是replace部分
                  'tag': '|',           # sed分隔符
                  'end': 'g',           # sed结尾的选项
                  'loc_data': '.*',     # locate部分，data的占位符
                  'rep_prefix': '',     # replace部分的的prefix
                  }

    """ 内部配置，经常要改动的那些
    """
    _debug_command = False   # 显示更多测试信息
    _debug_output = False

    """ 初始化工作
    """
    def __init__(self):
        """ 提供执行grep、sed时的，command执行模式
        """
        self.multi = 'NNN'
        self.run = {'warn': True, 'hide': True}

        self.test = False
        self.exit_on_err = True
        self.conf_path = ''     # 默认配置文件

        """ 保存中间结果
        """
        self.cache = ''     # 临时测试数据
        self.grep_out = ''  # grep结果
        self.sed_out = ''   # sed结果
        self.result = ''    # 测试结果

        self.init_option()


    def test_mode(self):
        self.test = True
        self.exit_on_err = False

        self.conf_path = os.path.join(os.getcwd(), 'config.properties')

    def debug(self, command=True, output=False):
        self._debug_command = command
        self._debug_output = output

    def initial(self, cache):
        """ 设置test时的数据源
        """
        self.cache = cache.strip('\n')

    def _path(self, file):
        return file if file else self.conf_path

    def debug_output(self, name, output, line=False, force=False, seperate=''):
        """ 有数据才输出
            只有一行，就不使用回车
        """
        if force or self._debug_output and len(output) > 0:
            if output.count('\n') > 1: line = True
            print('[{name}]: {line}{output}{seperate}'.format(name=name, output=output, line='\n' if line else '',
                                                              seperate=seperate))

    def debug_command(self, name, output):
        if self._debug_command:
            print("[{}]: {}".format(name, output))

    ########################################################################################
    def path(self, path):
        """ 设置默认配置文件
        """
        self.conf_path = path

    def init(self, c, file):
        return c, self._path(file)

    def file(self, path):
        """ 显示时方便查看，截短
        """
        return path.split('/')[-1]

    def exit(self, data):
        if data:
            return data
        else:
            return exit(-1) if self.exit_on_err else False
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
        """ 覆盖默认grep选项
        """
        if kwargs.get('for_append'):
            self._grep_append.update(kwargs)
        else:
            self.grep_update.update(kwargs)
        self.init_option()

    def sed(self, **kwargs):
        """ 覆盖默认sed选项
        """
        self._sed_update.update(kwargs)

    def show_option(self, count):
        """ grep时，显示的行数选项
        """
        if count:
            return '-{type} {count} '.format(type='A' if count >= 0 else 'B', count=abs(count))
        else:
            return ''

    ########################################################################################
    def grep_fix(self, command):
        if command:
            return command.replace('-', '\-')
        else:
            return ''

    def sed_fix(self, data, for_key=True):
        if for_key:
            return data.replace('/', '\/').replace('=', '\=')
        else:
            return data.replace('\n', '\\n')

    def check_param(self, file, **kwargs):
        if not file:
            print("update config, but file not set")
            exit(-1)


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


def grep(**kwargs):
    local.grep(**kwargs)


def sed(**kwargs):
    local.sed(**kwargs)


def path(full):
    local.path(full)


if True:
    def test_mode(set):
        if set:
            local.test_mode()

            """ 是否开启更多的日志
            """
            local.debug(True)
            global c    # 在本文件中使用的c，如 check 函数

            from fabric import Connection
            c = Connection('127.0.0.1')
            return c
        else:
            return None

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
