#!/bin/sh

BASE=/mnt/disk
WORK=$BASE/apache-hive-2.3.2-bin/

rm $WORK -rf
tar zxvf ~/source/component/hive/apache-hive-2.3.2-bin.tar.gz -C $BASE

echo "export HIVE_HOME=$WORK" >> ~/.bashrc
echo 'export PATH=$PATH:$HIVE_HOME/bin' >> ~/.bashrc
source ~/.bashrc

rm /opt/hive -rf
sudo ln -s $WORK /opt/hive
cd /opt/hive

\cp $HIVE_HOME/conf/hive-log4j2.properties.template $HIVE_HOME/conf/hive-log4j2.properties
\cp $HIVE_HOME/conf/hive-default.xml.template $HIVE_HOME/conf/hive-site.xml  
\cp $HIVE_HOME/conf/hive-env.sh.template  hive-env.sh
