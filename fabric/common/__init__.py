# coding=utf-8

"""
## 使用
    1. 安装
        python3
        pip source pyYaml
        pip source fabric

    2. 配置
        1. 基本：
                1. 每个文件夹有自己的fabric.yaml，必须自动或者手动复制到 ~/或者/etc目录下
                    1. 为了方便，配置中设置了task.collection_name，因此如果切换了目录，找不到对应的 collection.py，fab 无法工作
                    2. 切换目录后，比如切换到 kafka 安装脚本中，需要先执行 python kafka.py，将触发更新配置，将工程目录下的配置复制

                2. fabric.yaml 内容
                    1. run：命令执行时的一些默认命令
                    2. task.collection_name: 默认collection，这样就可以访问本地其他名字的 .py直接使用；不需要导入到fabric.py了
                    3. 控制机、宿主机、服务机

                3. python搜索路径
                    1. 外部设置：lib/python3.6/site-packages/*.pth；在任何路径下，执行：python common/prepare.py 即可
                    2. 程序设置：在fabric命令文件中，最头部初添加：sys.path.append(os.path.join(os.getcwd(), "../.."))
                       见 init.py 头部 ‘搜索路径’ 的说明

        2. 策略
                1. 控制机：发起命令的机器（执行fab的），可以与宿主机一样

                2. 宿主机：从该机器发出命令；其他机器从该机器获取安装包
                    1. 通常情况下，宿主机(hosts.one)即是本地虚拟机；这样就不需要到其他机器配置 python、fabric了
                    2. 宿主机无法通过vpn连接：
                            虚拟机内部添加 NAT 网卡
                            sudo route add -net 192.168.80.0 netmask 255.255.255.0 gw 192.168.127.2

                    1. 控制机与宿主机，都是虚拟机
                    2. 控制机是虚拟机，宿主机是服务机
    3. 案例：
            1. grep、sed: common/sed
            2. 完整：component/kafka

## 开发

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

            3. 屏幕回显丢失
                如果远端不是主动关闭的（持续方式输出、或者尚未执行完成），此时 control-c 那么就会丢失回显
                对长时间执行的命令，使用 pty=True

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
    角色划分：安装点、其他机器（master、slave等）
    在一个 c 内修改的config不生效，不能影响全局？
    help complete
    将不同的命令，放到不同的文件
    将不同的阶段，放到不同的文件

    自动生成范围区间的host

"""