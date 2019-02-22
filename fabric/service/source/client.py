# coding=utf-8

from service.source.server import *
import system


def use_repo(c, file, name, path):
    c.run('''cat << EOF > /etc/yum.repos.d/{file}
[{name}]
name=local file repo
baseurl={type}://{path}

gpgcheck=0
enabled=1
priority=1
proxy=_none_
EOF'''.format(file=file, name=name, type='file' if path.startswith('/') else 'http', path=path))

    test = '''yum --disablerepo="*" --enablerepo="{name}" list available'''.format(name=name)
    c.run(test)

    system.help(c, '''
    {test}\n'''.format(test=test), 'test')

@task
def use_sshd(c, user='root', paww='111111'):
    set_invoke(True)
    c = conn(c)

    system.install(c, 'bash-completion tar sudo')
    system.install(c, 'passwd openssh-server openssh-clients')

    """ 方法1：此方法显示 chpasswd 无法找到
    """
    c.run("echo '{user}:{paww}' | /usr/sbin/chpasswd".format(user=user, paww=paww))

    # c.run("echo '{paww}' | password {user} --stdin".format(user=user, paww=paww))
    c.run('''
sed -i 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config
sed -i 's/#UsePAM no/UsePAM no/g' /etc/ssh/sshd_config
sed -i 's/#PermitRootLogin yes/PermitRootLogin yes/' /etc/ssh/sshd_config
sed -i 's/^#UseDNS yes/UseDNS no/g' /etc/ssh/sshd_config
sed -i 's/^GSSAPIAuthentication yes/GSSAPIAuthentication no/g' /etc/ssh/sshd_config

ssh-keygen -t rsa -f /etc/ssh/ssh_host_rsa_key -N ''
ssh-keygen -t dsa -f /etc/ssh/ssh_host_dsa_key -N ''
ssh-keygen -t ecdsa -f /etc/ssh/ssh_host_ecdsa_key -N ''
ssh-keygen -t ed25519 -f /etc/ssh/ssh_host_ed25519_key -N ''

mkdir -p /root/.ssh/
cd /root/.ssh
echo '' | ssh-keygen -t rsa -N ''

echo "StrictHostKeyChecking=no" > /root/.ssh/config
echo "UserKnownHostsFile=/dev/null" >> /root/.ssh/config
''')
    if globing.invoke:
        c.run('''cat << EOF > /start.sh
#!/bin/bash

echo "start sshd"
/usr/sbin/sshd -D
EOF''')


@task
def use_file(c, path=local.http_path):
    """ fab -H 192.168.0.81 source.use_file --path /home/repo
    """
    c = conn(c)
    use_repo(c, 'file.repo', local.file_repo, path)


@task
def use_http(c, url):
    """ fab -H 192.168.0.81 source.use_http --url 192.168.0.81
    """
    c = conn(c)
    use_repo(c, 'http.repo', local.http_repo, url)

@task
def use_help(c):
    """ fab -H 192.168.0.81 source.use_help
    """
    c = conn(c, True)
    system.help(c, '''
        yum --disablerepo="*" --enablerepo="{name}" list available
        yum --disablerepo="*" --enablerepo="{name}" install -y python36u
        '''.format(name=local.http_repo))

@task
def use_epel(c):
    """ add epel and so on

        yum-fastestmirror

        wget -O /etc/yum.repos.d/CentOS-Base-aliyun.repo http://mirrors.aliyun.com/repo/Centos-7.repo
    """
    c = conn(c)
    system.install(c, 'source')

@task
def use_proxy(c, url, add=True):
    """ fab -H 192.168.0.82 source.use_proxy --url 192.168.0.81

        yum makecache 有时要多执行几次
    """
    c = conn(c)
    sed.path('/etc/yum.conf')
    sed.grep(**{'sep': '='})
    sed.append(c, 'proxy=http://{url}:3142'.format(url=url))

    system.help(c, '''
        yum install -y epel-release
        yum install -y apt-cacher-ng''', 'test')

    system.help(c, '''
        yum makecache
    ''')

    # use_proxy(hosts.conn(0), hosts.get_host(0)['host'])