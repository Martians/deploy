
# https://hub.docker.com/_/centos/
# https://github.com/CentOS/sig-cloud-instance-images/blob/bc561dfdd671d612dbb9f92e7e17dd8009befc44/docker/Dockerfile
# centos7.1.1503, 7.1.1503

From centos:7.1.1503
MAINTAINER long@126.com

ARG BASE=/docker

EXPOSE 22
COPY . $BASE

RUN $BASE/script/initialize.sh \
	$BASE/script/server/$SERVICE.sh \
	&& $BASE/script/clean.sh \
	&& cp $BASE/script/server/start_$SERVICE.sh /start.sh

CMD ["/bin/bash"]
CMD ["/start.sh"]
