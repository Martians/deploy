#!/bin/bash

##############################################################################
BASE_PATH=$(cd "$(dirname "$0")"; cd ..; pwd)
cd $BASE_PATH

. 0_config/config.sh

# 将配置文件复制到docker中，方便后续在docker中执行相关脚本时用到
#	注意，因为配置是复制到image中的，如果调整了docker_config的配置，需要重新生成images
cp $CONFIG_PATH_2 /root/.docker_config
##############################################################################
parse_param() {
	local OPTIND
	var=$*
	set -- $var 
	#echo $*

	while getopts :r:s:m: opt
	do
		case "$opt" in
			r) 	REPO=$(decode "$OPTARG");;
			s)	SERVER=$OPTARG;;
			m)	MORE=$OPTARG;;
			*) 	echo "Unknown option: $opt";;
		esac
	done
	# echo "repo: " $REPO
	# echo "more: " $MORE
	# echo "SERVER: " $SERVER
	# exit 1
}
parse_param $*

##############################################################################
## 执行说明
#	1. 任何时候 scripts 执行的脚本出错，就会导致程序退出
#	2. 如果脚本中需要引用函数 1）export函数 2) scripts source *.sh 方式执行

##############################################################################
## Repo
if [ "$REPO" ]; then
	if [[ $REPO == "" ]]; then
		REPO="public"
	fi
	scripts source 1_build/repo.sh $REPO
	cd $BASE_PATH
fi

##############################################################################
## System
scripts $BASE_PATH/1_build/system.sh
scripts $BASE_PATH/1_build/common.sh

##############################################################################
## More Script
# if [ "$MORE" and -e "$MORE" ]; then
# 	echo "use More"
# 	scripts $MORE
# fi

##############################################################################
## Install service
scripts source $BASE_PATH/1_build/server/$SERVER.sh

cp $BASE_PATH/1_build/server/start_$SERVER.sh /start.sh

##############################################################################
## Clean
scripts source $BASE_PATH/1_build/clean.sh

##############################################################################
echo "initialize complete ..."

