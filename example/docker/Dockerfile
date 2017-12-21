
From ubuntu

RUN echo 0 > /etc/stop
CMD ["/bin/bash"]

HEALTHCHECK --interval=5s --timeout=3s --retries=2 \
	echo `more /etc/stop` || exit 1
