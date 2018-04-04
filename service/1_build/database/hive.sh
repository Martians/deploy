#!/bin/bash
HIVE_HOME=/apache-hive-2.3.2-bin
POSTGRES_HOST=localhost
METASTOR_HOST=localhost

SOURCE=/source

#######################################################################
BASE_PATH=$(cd "$(dirname "$0")"; cd ../..; pwd)
cd $BASE_PATH

. 0_config/config.sh

#rm /etc/httpd/conf.d/local.conf -rf
if [ $(set_file_flag /installed) -eq 1 ]; then
  echo "already install, just start"
  systemctl start postgresql-9.5.service
  
  echo "start metastore"
  nohup $HIVE_HOME/bin/hive --service metastore &

  sleep 5
  echo "start hiveserver2"
  nohup $HIVE_HOME/bin/hive --service hiveserver2 &

  sleep 5
  jps
  exit
fi

###########################################################################################
BASE_PATH=$(cd "$(dirname "$0")"; cd ../..; pwd)
cd $BASE_PATH

. 0_config/config.sh

#<<'COMMENT'
###########################################################################################
sh $BASE_PATH/1_build/database/postgres.sh

sudo -u postgres psql <<EOF
CREATE DATABASE hive;
CREATE USER hive WITH PASSWORD 'hive';
GRANT ALL PRIVILEGES ON DATABASE hive TO hive;
\c hive
CREATE SCHEMA hive AUTHORIZATION hive;
ALTER SCHEMA hive OWNER TO hive;
ALTER ROLE hive SET search_path to 'hive', 'public';
\q
EOF
#COMMENT

#<<'COMMENT'
###########################################################################################
#create dir on hdfs
sh $BASE_PATH/1_build/database/hive_hadoop_client.sh

echo "prepare hadoop"
hdfs dfs -mkdir -p \
	/user/hive/root \
	/user/hive/tmp \
	/user/hive/log
hdfs dfs -chown -R hadoop /user/hive
hdfs dfs -chmod -R u+w,g+w,o+w /user/hive

hdfs dfs -ls /user/hive

###########################################################################################
rm $HIVE_HOME -rf
tar zxvf $SOURCE/component/hive/apache-hive-2.3.2-bin.tar.gz -C /

echo "
export HIVE_HOME=$HIVE_HOME
export PATH=\$PATH:\$HIVE_HOME/bin" >> ~/.bashrc
source ~/.bashrc

rm /opt/hive -rf
mkdir -p /opt/hive
sudo ln -s $HIVE_HOME /opt/hive
#COMMENT

echo "install jdbc driver"
yum install postgresql-jdbc -y
ln -s /usr/share/java/postgresql-jdbc.jar $HIVE_HOME/lib/postgresql-jdbc.jar

###########################################################################################
echo "copy config template"
\cp $HIVE_HOME/conf/hive-env.sh.template  $HIVE_HOME/conf/hive-env.sh
\cp $HIVE_HOME/conf/hive-log4j2.properties.template $HIVE_HOME/conf/hive-log4j2.properties
\cp $HIVE_HOME/conf/hive-default.xml.template $HIVE_HOME/conf/hive-site.xml  

echo "HADOOP_HOME=$HADOOP_HOME"  >> $HIVE_HOME/conf/hive-env.sh
echo "HIVE_CONF_DIR=$HIVE_HOME/conf"  >> $HIVE_HOME/conf/hive-env.sh

sed -i "s|\(property.hive.log.dir =\).*|\1$HIVE_HOME\/log|g" $HIVE_HOME/conf/hive-log4j2.properties

cat << EOF > $HIVE_HOME/conf/hive-site.xml
<configuration>
<property>
  <name>javax.jdo.option.ConnectionURL</name>
  <value>jdbc:postgresql://$POSTGRES_HOST:5432/hive?createDatabaseIfNotExist=true</value>
</property>

<property>
  <name>javax.jdo.option.ConnectionDriverName</name>
  <value>org.postgresql.Driver</value>
</property>

<property>
  <name>javax.jdo.option.ConnectionUserName</name>
  <value>hive</value>
</property>

<property>
  <name>javax.jdo.option.ConnectionPassword</name>
  <value>hive</value>
</property>

<property>
 <name>hive.metastore.warehouse.dir</name>
 <value>/user/hive/root</value>
</property>

<property>
  <name>hive.exec.scratchdir</name>
  <value>/user/hive/tmp</value>
</property>

<property>
  <name>hive.querylog.location</name>
  <value>/user/hive/log</value>
</property>

<property>
  <name>hive.metastore.uris</name>
  <value>thrift://$METASTOR_HOST:9083</value>
</property>

<property>
  <name>hive.server2.enable.doAs</name>
  <value>false</value>
</property>

</configuration>
EOF
cat $HIVE_HOME/conf/hive-site.xml

###########################################################################################

#chmod
#sudo chown -R hadoop:hadoop /home/hadoop/hive-2.2.0
#sudo chmod -R u+w,g+w /home/hadoop/hive-2.2.0
schematool --dbType postgres --initSchema

echo "start metastore"
nohup hive --service metastore &

sleep 5
echo "start hiveserver2"
nohup hive --service hiveserver2 &

jps

#######################################################################
set_file_flag /installed 1
