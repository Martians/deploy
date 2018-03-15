#!/bin/bash

<<'COMMENT'
COMMENT

########################################################################################
# 创建依赖的BASE image
create_base() {

	if [[ $BASE_TMPLT == "" ]]; then
		BASE_TMPLT=0_centos
	fi

	if [[ $BASE_IMAGE == "" ]]; then
		BASE_IMAGE=centos:base
	fi
	# echo "base template: " $BASE_TMPLT
	# echo "base image: " $BASE_IMAGE

	# 配置了，要使用基础模板; 或者是 ubuntu 相关容器
	if [[ $USING_BASE == 1 ]]; then

		if [ ! `docker images $BASE_IMAGE -q` ]; then
			work_output "create base image"

			set -x
			docker build -t $BASE_IMAGE -f $IMAGE_PATH/$BASE_TMPLT .
			set +x
			val=$?

			docker history $IMAGE
			return $val
			# docker tag centos:base centos
		else
			work_output "base image $IMAGE already exist"			
		fi
	fi
}

create_image() {
	success create_base
	local PORT TYPE REPO NAME

	local OPTIND
	var=$*
	set -- $var 
	#echo "get $*"

	while getopts :n:r:p:t: opt
	do
		case "$opt" in
		t)	TYPE=$OPTARG;;
		r)	REPO=$(decode "$OPTARG");;
		n) 	NAME=$OPTARG;;
		p)	PORT=$OPTARG;;
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
		step_output "clean image: $NAME"
		docker rm  -f $NAME
		docker rmi -f $IMAGE
		#sleep 1
	fi

	if [ ! `docker images $IMAGE -q` ]; then
		step_output "create image for $NAME"

		set -x
		docker build -t $IMAGE -f $IMAGE_PATH/0_server \
			--build-arg REPO=$(encode $REPO)	\
			--build-arg SERVICE=$NAME 	\
			--build-arg LISTEN="$PORT" .
		set +x
	fi
}

create_docker() {
	local PORT TYPE NAME ARGS

	local OPTIND
	var=$*
	set -- $var 
	#echo "get $*"
	while getopts :n:p:t:a: opt; do
		case "$opt" in
			n) 	NAME=$OPTARG;;
			p)	PORT=$OPTARG;;
			t)	TYPE=$OPTARG;;
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
	# echo "image: "$IMAGE
	# exit 1

	# type == 0 || type == 1, remove docker
	if [[ $TYPE == 0 || $TYPE == 1 ]]; then
		step_output "remove container: $NAME"
		docker rm -f $NAME
	fi

	# check if docker ps output end with $NAME
	if [[ `docker ps -a | grep "$NAME$"` == "" ]]; then
		color_output "create docker"
		PORT=$(exist $PORT -p $PORT:$PORT)

		set -x
		docker run -itd --name $NAME -h $NAME \
			$PORT	\
			$GLOBAL_MACRO $ARGS \
			$IMAGE
		# docker run -itd --name $NAME -h $NAME -v $HOST_PATH_REPO:/html -P $IMAGE
		set +x

	elif [[ `docker ps | grep "$NAME$"` == "" ]]; then
		color_output "starting docker ..."
		docker start $NAME

	else
		color_output "already started"
	fi
}

create_proxy() {
	BASE_TMPLT=0_proxy
	BASE_IMAGE=ubuntu:proxy

	## 用于后续在 create_docker 使用
	IMAGE=$BASE_IMAGE

	local OPTIND
	var=$*
	set -- $var 

	#echo "get $*"
	while getopts :t: opt
	do
		case "$opt" in
		t)	TYPE=$OPTARG;;
		*) 	echo "Unknown option: $OPT";;
		esac
	done

	if [[ $TYPE == 1 ]]; then
		step_output "clean image: $BASE_IMAGE"
		docker rmi -f $BASE_IMAGE
	fi

	success create_base
}

# 在创建其他的容器之前，检查是否要先创建依赖容器
create_prepare() {

	################################################################
	if [[ "$REPO" =~ "proxy" && "$REPO_MASK" =~ "proxy" ]]; then

		if [[ `docker ps | grep "proxy$"` == "" ]]; then
			color_output "create prepare: proxy"
			sh $BASE_SERVE_PATH/proxy.sh $*
		fi
	fi

	if [[ "$REPO" =~ "local" && "$REPO_MASK" =~ "local" ]]; then
		if [[ `docker ps | grep "http$"` == "" ]]; then
			color_output "create prepare: http"
			sh $BASE_SERVE_PATH/http.sh
		fi
	fi
}

########################################################################################
create_network() {

	NETWORK=$LOCAL/$SUBNET 	          

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

	echo "set  host address:"
	set -x
	sudo pipework $DEVICE $NAME $HOST/$SUBNET@$GATEWAY
	set +x
}

########################################################################################
display_state() {
	sudo netstat -antp | grep :$PORT[\t\ ] --color
	
echo "brower:
    docker exec -it $NAME /bin/bash
    http://$LOCAL:$PORT
"
}