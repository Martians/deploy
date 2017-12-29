#!/bin/sh
BASE=$(cd "$(dirname "$0")"; cd ..; pwd)
cd $BASE

##############################################################################
echo "install advance ..."
# same as 0_base
yum install -y bash-completion tar
