#!/bin/bash

##############################################################################
echo "use local repo"
echo"
Acquire::http::proxy "http://$HOST_PROXY:3142/";
Acquire::ftp::proxy "ftp://$HOST_PROXY:3142/";
Acquire::https::proxy "https://$HOST_PROXY:3142/";
" >> /etc/apt/apt.conf
