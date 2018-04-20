#!/bin/bash

<<'COMMENT'
COMMENT

########################################################################################
# 创建基于模板的镜像
create_origin() {
	####################################################

	local OPTIND
	var=$*
	set -- $var 

	local EXEC
	#echo "get $*"
	while getopts :t:i:p:e: opt; do
		case "$opt" in
		t)	TYPE=$OPTARG;;
		i)  BASE_IMAGE=$OPTARG;;
		p)  BASE_TMPLT=$OPTARG;;
		e)  EXEC=$OPTARG;;
		*) 	echo "Unknown option: $OPT";;
		esac
	done
	# echo "type:  " $TYPE
	# echo "image: " $IMAGE
	# echo "tmplt: " $BASE_TMPLT
	# echo "exec:  " $EXEC
	# exit 1

	if [[ $BASE_TMPLT == "" ]]; then
		BASE_TMPLT=0_centos
	fi

	if [[ $BASE_IMAGE == "" ]]; then
		BASE_IMAGE=centos:base
	fi

	if [[ $TYPE == 1 ]]; then
		step_output "clean image: $BASE_IMAGE"
		docker rmi -f $BASE_IMAGE
	fi

	####################################################
	# echo "base template: " $BASE_TMPLT
	# echo "base image: " $BASE_IMAGE

	# 配置了，要使用基础模板; 或者是 ubuntu 相关容器
	if [[ $USING_BASE == 1 ]]; then

		if [ ! `docker images $BASE_IMAGE -q` ]; then
			work_output "create base image"
			
			# 仅用于 ubuntu 搭建
			if [[ $EXEC ]]; then
				EXEC_PARAM=$(exist $EXEC "--build-arg EXEC=$EXEC")
				sudo \cp $CONFIG_PATH $CONFIG_PATH_2
			fi

			set -x
			docker build -t $BASE_IMAGE -f $IMAGE_PATH/$BASE_TMPLT \
				$EXEC_PARAM .
			set +x
			val=$?

			docker history $IMAGE

			# 仅用于 ubuntu 搭建
			if [[ $EXEC ]]; then
				sudo rm $CONFIG_PATH_2 -rf
			fi
			return $val
			# docker tag centos:base centos
		else
			work_output "base image $IMAGE already exist"			
		fi
	fi
}

# 创建基于其他镜像的镜像
create_image() {
	success create_origin

	local PORT TYPE REPO NAME EXEC

	local OPTIND
	var=$*
	set -- $var 
	#echo "get $*"

	while getopts :n:r:p:e:t: opt
	do
		case "$opt" in
		t)	TYPE=$OPTARG;;
		r)	REPO=$(decode "$OPTARG");;
		n) 	NAME=$OPTARG;;
		p)	PORT=$OPTARG;;
		e)  EXEC=$OPTARG;;
		*) 	echo "Unknown option: $OPT";;
		esac
	done
	# echo "repo: " $REPO
	# echo "name: " $NAME
	# echo "port: " $PORT
	# echo "type: " $TYPE
	# exit 1

	if [[ $IMAGE == "" ]]; then
		IMAGE=centos:$NAME
	fi

	# type == 1, remove image
	if [[ $TYPE == 1 ]]; then
		step_output "clean image: $IMAGE"
		docker rm  -f $NAME
		docker rmi -f $IMAGE
		#sleep 1
	fi

	if [ ! `docker images $IMAGE -q` ]; then
		step_output "create image for $IMAGE"
		EXEC_PARAM=$(exist $EXEC "--build-arg EXEC=$EXEC")

		# 将文件复制到临时路径，因为/docker复制到docker中的，因此docker中可以访问到
		#	1. docker只是在image中存在这个文件
		#	2. 实际docker运行时，为了访问最新文件，挂载了脚本目录到docker中，覆盖了/docker目录
		#	3. 因此在实际docker中，是看不到CONFIG_PATH_2这个文件的
		sudo \cp $CONFIG_PATH $CONFIG_PATH_2
		set -x
		docker build -t $IMAGE -f $IMAGE_PATH/0_server \
			--build-arg REPO=$(encode $REPO)	\
			--build-arg SERVICE=$NAME 	\
			--build-arg LISTEN="$PORT" 	\
			$EXEC_PARAM .
		# EXEC no used in o_server now
		set +x
		# 将临时文件清除
		sudo rm $CONFIG_PATH_2 -rf
	fi
}

create_docker() {
	local PORT TYPE NAME ARGS

	local OPTIND
	var=$*
	set -- $var 
	#echo "get $*"
	while getopts :n:p:t:a:i:e: opt; do
		case "$opt" in
			n) 	NAME=$OPTARG;;
			p)	PORT=$OPTARG;;
			t)	TYPE=$OPTARG;;
			e)	EXEC=$OPTARG;;
			i)	IMAGE=$OPTARG;;
			a) 	ARGS=$(decode "$OPTARG");;
			*) 	echo "Unknown option: $OPT";;
		esac
	done
	if [[ $IMAGE == "" ]]; then
		IMAGE=centos:$NAME
	fi
	# echo "name: " $NAME
	# echo "port: " $PORT
	# echo "type: " $TYPE
	# echo "args: " $ARGS
	# echo "exec: " $EXEC
	# echo "image: "$IMAGE
	# exit 1

	# type == 0 || type == 1, remove docker
	if [[ $TYPE == 0 || $TYPE == 1 ]]; then
		step_output "remove container: $NAME"
		docker rm -f $NAME
	fi

	if [ ! `docker images $IMAGE -q` ]; then
		color_output "docker $IMAGE not exist!"
		exit 1
	fi

	# check if docker ps output end with $NAME
	if [[ `docker ps -a | grep "$NAME$"` == "" ]]; then
		color_output "create docker $NAME"
		PORT_PARAM=$(exist $PORT -p $PORT:$PORT)

		set -x
		docker run -itd --name $NAME -h $NAME \
			$PORT_PARAM			\
			$GLOBAL_MACRO $ARGS \
			$IMAGE $EXEC
		# docker run -itd --name $NAME -h $NAME -v $HOST_PATH_REPO:/html -P $IMAGE
		set +x

	elif [[ `docker ps | grep "$NAME$"` == "" ]]; then
		color_output "starting docker $NAME ..."
		docker start $NAME

	else
		color_output "already started"
	fi
}

# 在创建其他的容器之前，检查是否要先创建依赖容器
create_prepare() {

	################################################################
	if [[ "$REPO" =~ "proxy" && "$REPO_MASK" =~ "proxy" ]]; then

		if [[ `docker ps | grep "proxy$"` == "" ]]; then
			color_output "prepare: proxy"
			sh $BASE_SERVE_PATH/proxy.sh $*
			done=1
		fi
	fi

	if [[ "$REPO" =~ "local" && "$REPO_MASK" =~ "local" ]]; then
		if [[ `docker ps | grep "http$"` == "" ]]; then
			color_output "prepare: http"
			sh $BASE_SERVE_PATH/http.sh
			done=1
		fi
	fi

	################################################################
	for var in $*; do
		# 如果其依赖的docker不存在(base docker)，就创建出来
		if [[ `docker ps | grep "$var$"` == "" ]]; then
			color_output "prepare: $var"
			sh $BASE_SERVE_PATH/$var.sh
			done=1
		fi
	done

	if [[ $done == 1 ]]; then
		color_output "create prepre completed, wait to continue ... "
		read -t 3 done
	fi
}

########################################################################################
create_network() {

	NETWORK=$HOST_LOCAL/$SUBNET 	          

	if [[ `ip address show | grep $BRIDGE` ]]; then
		echo "network exist"
	
	else
		color_output "create network"
		sudo ip addr del $NETWORK dev $DEVICE; \
				sudo ip link add link $DEVICE dev $BRIDGE type macvlan mode bridge; \
				sudo ip link set $BRIDGE up; \
				sudo ip addr add $NETWORK dev $BRIDGE; \
				sudo route add default gw $GATEWAY	

		color_output "clear dangling images"
		docker rmi -f $(docker images -aq -f dangling=true)
	fi
}

alloc_network() {
	local HOST=$1
	if [[ "$HOST" ]]; then
		create_network
	fi

	# 可以根据需要，指定不同的名字
	#	这里，没指定$2，name就是全局变量；指定了，name就是本地变量
	if [[ "$2" ]]; then
		local NAME=$2
	fi

	echo "set host address: $HOST, name: $NAME"
	set -x
	sudo pipework $DEVICE $NAME $HOST/$SUBNET@$GATEWAY
	set +x
}

# 举例：
	# 1) 检查zookeeper-1
	# 2) 检查H1
	# 3) 检查 HOST_1
alloc_cluster_host() {
	local NAME=$1
	local idx=$2

	# 分配IP地址,
	#	外部已经定义了变量 $NAME_$idx, 则优先使用
	if [[ $(dyn_var "${NAME}_${idx}") != "" ]]; then
		# $NAME_$idx 中可能只定义了ip的最后一位
		SUFFIX=$(dyn_var ${NAME}_${idx})

	elif [[ $(dyn_var H${idx}) != "" ]]; then
		# $NAME_$idx 中可能只定义了ip的最后一位
		SUFFIX=$(dyn_var H${idx})
	# 自动解析默认的index，转换为IP
	else
		SUFFIX=$idx
	fi

	echo $(alloc_host $SUFFIX)
}

########################################################################################
display_brower() {
sudo netstat -antp | grep :$PORT[\t\ ] --color
	
echo "brower:
    docker exec -it $NAME /bin/bash
    http://$HOST_LOCAL:$PORT
"
}

display_host() {
if [[ $1 != "" ]]; then
	color_output "ssh clean cache [client side]:"
	echo "    rm ~/.ssh/known_hosts -f
or,
    echo "StrictHostKeyChecking=no" > ~/.ssh/config
    echo "UserKnownHostsFile=/dev/null" >> ~/.ssh/config
"
	# docker 内部，网卡名称是 eth1
	echo "show host address:"
	docker exec $NAME ip addr show eth1 | grep inet | grep [0-9.].*/ --color
	echo
fi

echo "enter host:
    docker exec -it $NAME /bin/bash
    ssh root@$HOST
"
}

display_cluster() {
	local NAME=$1
	local COUNT=$2
	# docker 内部，网卡名称是 eth1
	echo "try start with last param [systemd]"
	echo "show host address:"
	for ((idx = 1; idx <= $COUNT; idx++)); do
		docker exec $NAME-$idx ip addr show eth1 | grep inet | grep [0-9.].*/ --color
	done

	echo "    docker exec $NAME-1 ping $NAME-2"
	echo "enter host:"
	for ((idx = 1; idx <= $COUNT; idx++)); do
		HOSTS=$(alloc_cluster_host $NAME $idx)	
		echo "    ssh root@$HOSTS"
	done
}

########################################################################################
# 整个dns添加过程的，测试方式：
# 	dns_add work 192.168.3.5
# 	dns_reload

# 	dig +short @127.0.0.1 work.data.com 
# 	dig +short @127.0.0.1 -x 192.168.3.5

# 往dns中添加PTR记录时
host_reverse() {
    echo $(alloc_host $1) | awk -F"." '{ print $4".："$3 }'
}

# 为docker配置dnsserver的地址
dns_server() {
	echo 
}

# 添加一个dns解析地址，到dns server的docker中去
dns_add() {
	docker exec dns $DOCK_INNER_PATH/dns_add.sh "$1" "$2"
}

# 检查是否发生了配置改变，需要重启dns server
dns_reload() {
	# 检查是否发生了dns的更新，在 /tmp/dns_reload 文件中检查标志，并重置
	result=$(docker exec dns $DOCK_INNER_PATH/dns_reload.sh)

	if [ $(string_exist "$result" 1) -eq 0 ]; then
		color_output "restart dns"
		docker restart dns
	fi
}

# 在docker中配置dns服务器地址
dns_config() {
	docker exec $1 $DOCK_INNER_PATH/dns_config.sh
}

ntp_config() {
	docker exec $1 $DOCK_INNER_PATH/ntp_config.sh	
}