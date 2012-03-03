#!/bin/sh
LIBPATH=$(dirname $SCRIPT_FILENAME)/lib
INCLUDE_HTTPLIB=1
. $LIBPATH/httplib.sh

p_file=/tmp/utk-pl.m3u
p_url="http://infoklass-news.narod.ru/progs/IPTV-ukrtel.m3u"
url="http://i-tools.org/charset/exec?dest=utf-8&src=utf-16le&download=1&data[url]=$p_url"
u_url="http://$(echo $port | cut -f1 -d:):4022/"

header Content-Type "audio/x-mpegurl"
header Content-Disposition "attachment; filename=playlist.m3u"
header Date $(date -R)
if [ ! -r $p_file ] || [ $(($(date +%s) - $(stat -c %Y $p_file))) -gt 86400 ]; then
	wget -O - "$p_url" -o /dev/null | tr -d "\r" | sed -re "/^udp/ { s#://@#/#; s@^@$u_url@ }" > $p_file || echo > $p_file
fi
header Last-Modified $(date -r $p_file -R)
header Status "200 OK"
echo -e "\r"
cat $p_file
