#!/bin/sh
LIBPATH=$(dirname $SCRIPT_FILENAME)/lib
INCLUDE_HTTPLIB=1
. $LIBPATH/httplib.sh

header Content-Type "text/plain; charset=utf-8"
date=$(date -R)
out=""
header Date $date
header Last-Modified $date
header Status "200 OK"
echo -e "\r"
set
fin
