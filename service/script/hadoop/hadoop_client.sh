#!/bin/sh

SOURCE=/source
HADOOP_HOME=/hadoop-2.7.3
HADOOP_HOST=192.168.36.10

echo "install java"
yum install java-1.8.0-openjdk-devel -y
echo "
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.151-5.b12.el7_4.x86_64/
export CLASSPATH=.:\$CLASSPATH:\$JAVA_HOME/lib:\$JRE_HOME/lib
export PATH=\$PATH:\$JAVA_HOME/bin " >> ~/.bashrc
source ~/.bashrc

#<<'COMMENT'
echo "setup hadoop client"
rm $HADOOP_HOME -rf
tar zxvf $SOURCE/hadoop/hadoop-2.7.3.tar.gz -C /

echo "
export HADOOP_HOME=$HADOOP_HOME
export PATH=\$HADOOP_HOME/bin:\$PATH" >> ~/.bashrc
source ~/.bashrc

###########################################################################################
echo "config hadoop"
cd $HADOOP_HOME
echo "export JAVA_HOME=$JAVA_HOME" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh

# core-site.xml
FILE=etc/hadoop/core-site.xml
echo "
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://$HADOOP_HOST:9000</value>
    </property> 
</configuration>
" > $FILE
cat $HADOOP_HOME/etc/hadoop/core-site.xml

# hdfs-site.xml
# mapred-site.xml
\cp etc/hadoop/mapred-site.xml.template etc/hadoop/mapred-site.xml
FILE=etc/hadoop/mapred-site.xml
echo "
<configuration>
    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>
</configuration>
" > $FILE
cat $HADOOP_HOME/etc/hadoop/mapred-site.xml