
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

## 0_proxy: only for proxy <- ubuntu:xenial

## 0_test: use for test

## Dockerfile: nothing



##########################################################
# Server
## comment
example: server/http [param]
    1. when given any param, will recreate image, and execute the script
    2. when given 0 or 1, will just recreate, no need do any script

## config server(see 0_server template)
    1. setup server in script/server/http.sh and so on
    2. start server in script/server/start_http.sh and so on

## create server
    1. proxy： yum and apt proxy
    2. http；  http server and yum server
    3. dns：   dns server
    4. ntp：   ntp server
    4. sshd:   sshd, assign public ip; sshd.sh, set REPO as "public local proxy"
    5. more:   same as sshd
    5. test:   base on 0_test(centos:test), do some script, assign test ip

## advance
    1. systemd: enable systemd, assign test ip; should do init work for docker, manually; or systemd will failed
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