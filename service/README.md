
##########################################################
# Template
## 0_base: centos_local
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
