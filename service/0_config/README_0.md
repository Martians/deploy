
##########################################################
# Enviroment 
## config
    1. script/config.sh: set current work TYPE, set macro config
    2. macro in each server script: sshd.sh(NAME REPO PORT MORE) and so on

##########################################################
# Template
## 0_centos: centos:base
    1. use centos:7.4.1708, 7.1.1503 can't work with systemd
    2. child：0_server
    
## 0_ubuntu: ubuntu template

## 0_server: server template <- centos:base
    1. this is a templete for other server
    use initialize.sh if not based on 0_centos(centos:base)
    2. use repo.sh, we can use file and local repo and proxy

## 0_proxy: only for proxy <- ubuntu:xenial, now

## 0_test: use for test

## Dockerfile: nothing



##########################################################
# Server conifg
## server script usage
example: server/http [param]
    1. when given any param, will recreate image and docker, will execute the given script for build
    2. when given 0 or 1, will just recreate image and docker, no need do any script

## config new server(see 0_server template)
    1. setup server: script for create server, in script/server/, as http.sh, for setup image and start docker
    2. start server: script for start server, in script/server/, as start_http.sh

## common server
    1. proxy： yum and apt repository proxy
    2. http；  http server, also used as yum server
    3. dns：   dns server
    4. ntp：   ntp server
    4. sshd:   sshd, assign public ip; sshd.sh, set REPO as "public local proxy". Can't used for systemd
    5. more:   same as sshd
    5. test:   base on 0_test(centos:test), do some script, assign test ip

## advance server
    1. systemd: enable systemd, assign test ip; 
        1. init scipt already used by /bin/bash/init, init work for server can only invoke manually; or systemd will failed
        2. see service\server\postgres.sh for example, after started, invoke script/hadoop/postgres.sh to start postgres server
    2. generate: generate data, like systemd, after start docker, execute start script use docker exec

##########################################################
# Command
    1. create.sh:   create 0_centos images and network, if not exist
    2. clean.sh：   remove all docker and images
    3. dangling.sh: remove danling images
    4. prepare.sh:  proxy.sh and http.sh

##########################################################
# Usage
## Step
    1. prepare proxy and http images, command/prepare.sh  
    2. start other server, sh server/sshd.sh and so on

## Comment
    1. unused: script/hadoop/*.sh: postgres.sh generate.sh