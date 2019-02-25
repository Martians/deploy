# coding=utf-8

import sys, os
sys.path.append(os.path.join(os.getcwd(), "../../.."))

from invoke import task
from common import *
import system


class LocalConfig:
    def __init__(self):
        self.http_path = '/home/repo'
        self.proxy_path = '/home/proxy'

        self.http_home = '/etc/httpd'
        self.http_conf = os.path.join(self.http_home, 'conf/httpd.conf')
        self.http_host = os.path.join(self.http_home, 'conf.d/local.conf')
        self.http_port = 80

        self.file_repo = 'file_repo'
        self.http_repo = 'http_repo'

        self.proxy_conf = '/etc/apt-cacher-ng/acng.conf'


local = LocalConfig()

@task
def file(c, path=local.http_path):
    """
        fab -H 192.168.0.81 source.file --path /home/repo
    """
    c = conn(c)
    print("make file repo on {}, path [{}]".format(c.host, path))

    system.install(c, 'createrepo')
    c.run('createrepo {}'.format(path))

@task
def http(c, path=local.http_path, port=local.http_port):
    """ fab -H 192.168.0.81 source.http --path /home/repo --port 80
    """
    c = conn(c)
    print("make http repo on {}, path [{}]".format(c.host, path))

    """ 准备
    """
    system.install(c, 'httpd createrepo')
    c.run('mkdir -p {path}'.format(path=path))

    """ 配置
    """
    c.run('''
        cd {home}; mkdir -p save
        cp -f conf/httpd.conf save
        mv conf.d/welcome.conf save
        rm conf.d/local.conf -rf'''.format(home=local.http_home))

    c.run('''cat << EOF > {host}
<VirtualHost *:{port}>
    DocumentRoot "{path}"
    <Directory "{path}">
        Options Indexes FollowSymLinks
        AllowOverride None
        Require all granted
      </Directory>
</VirtualHost>
EOF'''.format(host=local.http_host, path=path, port=port))

    if port != local.http_port:
        sed.append(hosts.conn(2), 'Listen {port}'.format(port=port), 'Listen 80', local.http_conf)
        print("set http port [{}]".format(port))

    """ 配置：
            root path不要配置在 /tmp下，无法识别
            httpd -t 
    """

    if globing.invoke:
        c.run('''cat << EOF > /start.sh
#!/bin/bash
echo "start httpd ... [`date`]"

#mkdir -p /run/httpd
for count in {1..5}  
do  
    echo "start $count"
    httpd -DFOREGROUND
    sleep 1
done
EOF''')
    else:
        c.run('systemctl restart httpd')

@task
def update(c, init=False):
    c = conn(c)

    """ 获取 path 位置
    """
    import re
    result = c.run("grep 'DocumentRoot' {host}".format(host=local.http_host))
    m = re.match('.*"(.*)"', result.stdout)

    if m is not None:
        path = m.group(1)
    else:
        print("not find repo path!")
        exit(-1)

    c.run('createrepo {type}{path}'.format(type='' if init else '-update ', path=path))


@task
def proxy(c, path=local.proxy_path):
    """ fab -H 192.168.0.81 source.proxy --path /home/proxy

        yum remove -y apt-cacher-ng
        systemctl restart apt-cacher-ng.service
        tail -f /var/log/apt-cacher-ng/*

            https://www.pitt-pladdy.com/blog/_20150720-132951_0100_Home_Lab_Project_apt-cacher-ng_with_CentOS/
            https://fabianlee.org/2018/02/11/ubuntu-a-centralized-apt-package-cache-using-apt-cacher-ng/

            docker: https://hub.docker.com/r/minimum2scp/apt-cacher-ng
    """
    c = conn(c)
    c.run('rm {conf} -rf'.format(conf=local.proxy_conf))

    """ 这里需要分开安装：先安装 epel-release 之后，才能安装 其他server
    """
    system.install(c, 'source')
    system.install(c, 'apt-cacher-ng')

    from common.disk import file_exist
    if not file_exist(c, local.proxy_conf):
        print("conf file {} not exist".format(local.proxy_conf))
        exit(-1)

    c.run('mkdir -p {path}; chmod 777 {path}'.format(path=path))
    c.run('''curl https://www.centos.org/download/full-mirrorlist.csv \
        | sed 's/^.*"http:/http:/' | sed 's/".*$//' | grep ^http > /etc/apt-cacher-ng/centos_mirrors''')

    """ 修改配置
    """
    sed.path(local.proxy_conf)
    sed.grep(**{'sep': ': '})
    sed.append(c, '''VfilePatternEx: ^(/\\\\?release=[0-9]+&arch=.*|.*/RPM-GPG-KEY-examplevendor)$''', '# WfilePatternEx:')
    #   sed.append(c, '''VfilePatternEx: ^/\\\\?release=[0-9]+&arch=''', '# WfilePatternEx:')
    sed.append(c, 'Remap-centos: file:centos_mirrors \/centos', 'Remap-debrep', pos=-1)
    sed.append(c, 'PassThroughPattern: (mirrors\\\\.fedoraproject\\\\.org|some\\\\.other\\\\.repo|yet\\\\.another\\\\.repo):443', '# PassThroughPattern: private-ppa', pos=5)
    sed.update(c, 'CacheDir', path)

    """ 启动服务
    """
    if globing.invoke:
        c.run('''cat << EOF > /start.sh
#!/bin/bash

echo "start proxy"

touch /var/log/apt-cacher-ng/a.log
#/etc/init.d/apt-cacher-ng start

/usr/sbin/apt-cacher-ng -c /etc/apt-cacher-ng pidfile=/var/run/apt-cacher-ng/pid SocketPath=/var/run/apt-cacher-ng/socket foreground=0
tail -f /var/log/apt-cacher-ng/*
EOF''')
    else:
        c.run('systemctl restart apt-cacher-ng.service')

    system.help(c, '''
        http://{host}:3142
        http://{host}:3142/acng-report.html
    
        tail -f /var/log/apt-cacher-ng/*'''.format(host=c.host), 'you can visit')

# proxy(hosts.conn(0))