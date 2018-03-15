#!/bin/bash

#################################################################################################
# 动态获取变量内容：将字符串的名字，作为变量名，再获得最终value
dyn_var() {
	echo `eval echo '$'${1}`
}


#################################################################################################
# Wrapper：
#	执行函数，并检查其返回值，进行错误输出；无需在函数外再写返回值检查
#	函数中发现了错误，通过return来返回错误码
success() {
	#echo $@
	func=$1
	shift
	#echo "success handle: " $*
	
	# 这里使用 $@，无法将有空格的参数很好的传递
	$func "$*"

	result=$?
	if [ $result == 0 ]; then
		return 0
	else
		echo "exec [$func] failed, return $result"
		exit $result
	fi
}

# Wrapper：
#	执行脚本，并检查其返回值，进行错误输出；无需在函数外再写返回值检查
#	脚本中发现了错误，通过 exit 来返回错误码
# 普通方式：  script        1_build/repo.sh $REPO
# source方式：script source 1_build/repo.sh $REPO
scripts() {

	# 如果第一个参数是 source, 使用source的方式执行脚本
	if [[ $1 == "source" ]]; then
		SOURCE=1
		shift
	fi
	
	func=$1
	shift
	#echo "success handle: " $*
	
	# 这里使用 $@，无法将有空格的参数很好的传递
	if [[ $SOURCE == 1 ]]; then
		#echo "source mode"
		.  $func "$*"
	else
		#echo "common mode"
		sh $func "$*"
	fi

	result=$?
	if [ $result == 0 ]; then
		return 0
	else
		echo "exec [$func] failed, return $result"
		exit $result
	fi
}

#################################################################################################
# 该函数暂未用上
# base_dir() {
# 	if [ $base_path ]; then
# 		echo $base_path
# 		return 0
# 	fi

# 	cd $(dirname ${BASH_SOURCE[0]});
# 	depth=1

# 	if [ $1 ]; then
# 		depth=$1
# 	fi
# 	for ((x = 0; x < $depth; x++)); do
# 		cd ..
# 	done

# 	base_path=$(pwd)
# 	echo $base_path
# }

# color: http://www.linuxidc.com/Linux/2014-12/110463.htm 
<<'COMMENT'
	RED_COLOR='\E[1;31m'  #红
	GREEN_COLOR='\E[1;32m' #绿
	YELOW_COLOR='\E[1;33m' #黄
	BLUE_COLOR='\E[1;34m'  #蓝
	PINK='\E[1;35m'      #粉红
	RES='\E[0m'

	#需要使用echo -e
	echo -e  "${RED_COLOR}======red color======${RES}"
	echo -e  "${YELOW_COLOR}======yelow color======${RES}"
	echo -e  "${BLUE_COLOR}======green color======${RES}"
	echo -e  "${GREEN_COLOR}======green color======${RES}"
	echo -e  "${PINK}======pink color======${RES}"
	echo "#############################################################"
COMMENT

GREEN_COLOR='\E[1;32m'
RES='\E[0m'

file_output() {
	echo 
	echo "======================================"
	echo "[file:  $@]"
}

step_output() {
	#echo 
	echo "  ==== " $@
}

work_output() {
	#echo 
	echo "  ---- " $@
}

color_output() {
	echo -e  "${GREEN_COLOR}-- $@ -- ${RES}"
}
export -f file_output step_output work_output color_output

#################################################################################################
# 参数传递时进行的特殊字符转换：空格
encode() {
	echo -n $@ | sed -e 's#[ \t]#||#g'
}

decode() {
	echo -n $@ | sed -e 's#||# #g'
}

# 参数传递时进行的特殊字符转换：空格
exist() {
	if [[ $1 == "0" ]]; then
		echo ""
	else
		shift
		echo $*
	fi
}