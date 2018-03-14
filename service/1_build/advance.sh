#!/bin/bash
BASE=$(cd "$(dirname "$0")"; cd ..; pwd)
cd $BASE

##############################################################################
echo "install advance ..."
yum install -y bash-completion tar
