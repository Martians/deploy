# coding=utf-8

"""
在一个 c 内修改的config不生效，不能影响全局？

## 功能
    1. group方式，对多个conn同时执行
    2. 一次执行多条命令
        1）复杂命令：分解开并执行，execute.multi
        2）简单命令：一次传入一次性执行，只看最终结果

## 存在问题：
        1. 模块识别
            common模块中的内容，使用时要加 common.* 前缀；但是如果是调试common内部模块，此前缀导致相关模块找不到

            IDE下调试路径与执行路径不同，导致找不到module
            尝试：sudo sh -c 'echo /mnt/hgfs/local/deploy/fabric > /home/long/.pyenv/versions/3.6.5/lib/python3.6/site-packages/fabric_test.pth'

        2. 配置文件识别
            fabric 不识别本地 fabric.yaml；虽然通过-d选项，能够看到此文件被load过，但是最终的config中没有信息
            invoke 直接使用时可以识别的，https://github.com/pyinvoke/invoke/issues/471

            通过执行 init.copy_config 来确保本地的config文件得到使用

        3. sed解析

## 使用方式：
    1. 必须引入 init 模块，这样会自动初始化 hosts

    2. 重要配置
        run:
            warn: true      默认所有错误都不抛出异常；不应该配置此选项
            echo: true      打印执行的所有shell命令内容，相当于 se -x
            hide: false     是否对外输出命令的执行结果

        1. 只查看执行的命令：echo = True, hide = True
        2. 输出所有内容：echo = True, hide = False
        3. pty=True 需要输入密码的部分


Todo
    将配置文件分离出来

"""