#!/bin/bash

<<'COMMENT'
COMMENT



# docker_sshd() {

# }

# docker_network() {
# 	NETWORK=$LOCAL/$SUBNET 	          

# 	if ifconfig | grep $BRIDGE > /dev/null; then
# 		echo "network exist"
# 	else
# 		echo "create network"
# 		sudo ip addr del $NETWORK dev $DEVICE; \
# 				sudo ip link add link $DEVICE dev $BRIDGE type macvlan mode bridge; \
# 				sudo ip link set $BRIDGE up; \
# 				sudo ip addr add $NETWORK dev $BRIDGE; \
# 				sudo route add default gw $GATEWAY	

# 		echo "clear dangling images"
# 		docker rmi -f $(docker images -aq -f dangling=true)
# 	fi
# }

# 创建依赖的BASE image
create_base() {

	# 配置了，要使用基础模板
	if [[ $USING_BASE == 1 ]]; then

		echo "create base image"
		IMAGE_NAME=centos:base

		if [ ! `docker images $IMAGE_NAME -q` ]; then
			docker build -t $IMAGE_NAME -f $IMAGE_PATH/0_centos .
			val=$?

			docker history $IMAGE_NAME
			return $val
			# docker tag centos:base centos
		fi
	fi
}

# 1. IMAGE
create_image() {
	create_base
	if [[ $? != 0 ]]; then
		return $?
	fi

	NAME=$1
	IMAGE_NAME=centos:$NAME
	if [ ! `docker images $IMAGE_NAME -q` ]; then
		echo "create image for $NAME"

		set -x
		docker build -t $IMAGE_NAME -f IMAGE_PATH/0_server \
			--build-arg REPO="$REPO"	\
			--build-arg SERVICE=$NAME 	\
			--build-arg LISTEN="$PORT" .
		set +x
	fi
}

# create_docker() {
# 	    docker rm -f $NAME
#     docker rmi -f $IMAGE
# fi


# # check if docker ps output end with $NAME
# if [ "`docker ps -a | grep $NAME$`" == "" ]; then
# 	echo -e  "${GREEN_COLOR}-- create docker -- ${RES}"
# 	set -x
# 	docker run -itd --name $NAME -h $NAME $GLOBAL_MACRO -v $REPO_SRC:$REPO_DST -p $PORT:$PORT $IMAGE
# 	# docker run -itd --name $NAME -h $NAME -v $REPO_SRC:/html -P $IMAGE
# 	set +x
	
# 	elif [ "`docker ps | grep $NAME$`" == "" ]; then
# 		echo -e  "${GREEN_COLOR}-- starting docker ... --${RES}"
# 		docker start $NAME
# 	else
# 		echo -e  "${GREEN_COLOR}-- already started --${RES}"
# 	fi
# }

# alloc_network() {

# }