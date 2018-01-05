#!/bin/sh

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