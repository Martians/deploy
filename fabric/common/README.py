# coding=utf-8

''' 环境准备：
    1. IDE下调试路径与执行路径不同，导致找不到module
        sudo sh -c 'echo /mnt/hgfs/local/deploy/fabric > /home/long/.pyenv/versions/3.6.5/lib/python3.6/site-packages/fabric_test.pth'
'''

''' http://docs.fabfile.org/en/2.0/cli.html
    http://docs.pyinvoke.org/en/latest/invoke.html#inv

    https://github.com/pyinvoke/invoke/issues/471
    
    run:
        warn: true      默认所有错误都不抛出异常；不应该配置此选项
        echo: true      打印执行的所有shell命令内容，相当于 se -x
        hide: false     是否对外输出命令的执行结果
    
    1. 只查看执行的命令：echo = True, hide = True
    2. 输出所有内容：echo = True, hide = False
'''