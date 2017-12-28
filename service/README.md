
##########################################################
# Usage
## config
script/config.sh: set TYPE

## usage 
server/http [param], when given any param, will recreate image
server/proxy
server/dns
server/sshd

## 0_ubuntu, not use public centos:base, use centos:7.1.1503
1. in 0_centos:     initialize

## 0_ubuntu, use centos:base <- 0_base
1. in 0_centos: 	repo.sh, we can use local repo and proxy
2. start server/http.sh, server/proxy.sh
3. config server/sshd.sh, set REPO as "public local proxy"
4. test proxy
   in sshd-host1, yum install git -y
   in proxy, docker logs -f proxy

##########################################################
# Template
## 0_base: centos:base, not clean cache, only for service setup
## 0_centos: centos template
## 0_ubuntu: ubuntu template 
## Dockerfile: nothing

##########################################################
# Enviroment Command
## create macro in ~/.bashrc
command/prepare.sh  

## create images and network, if not exist
command/create.sh  

##########################################################
# start server

## sshd:   server/sshd.sh  

## docker: server/host.sh  

## dns:    server/dns.sh
