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
def use_file(c, path=local.repo):
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
    c = conn(c)
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