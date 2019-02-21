from invoke import task
from invoke import Context

from common import *

@task
def maven(c):
    c = conn(c, True)

    sed.append(c, '''
    <mirror>
        <id>alimaven</id>
        <name>aliyun maven</name>
        <url>http://maven.aliyun.com/nexus/content/groups/public/</url>;
        <mirrorOf>central</mirrorOf>
    </mirror>''', '</mirrors>', '/usr/share/maven/conf/settings.xml', -1)

