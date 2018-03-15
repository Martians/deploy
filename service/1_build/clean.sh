#!/bin/bash

#################################################################
file_output "clean.sh"

yum clean all
#rm -rf /var/log/*
rm -rf /var/cache/yum/*
