#!/bin/sh
LIBPATH=$(dirname $SCRIPT_FILENAME)/lib
INCLUDE_HTTPLIB=1
. $LIBPATH/httplib.sh

do_find () {
	find . -maxdepth 1 -mindepth 1 -type $1 | sed -e 's@^./@@' | sort
}

p_file () {
	echo -n "<tr><td><a href='$(urlencode "$1")'>"
	stat -c '%n</a></td><td align='right'>%s</td><td>%y</td></tr>' "$2"
}

p_dir () {
	echo -n "<tr><td><a href='$(urlencode "$1")'>"
	stat -c '%n</a></td><td>%y</td></tr>' "$2"
}

p_stat () {
	b_free=$(stat -f -c "%a" "$home")
	b_size=$(stat -f -c "%S" "$home")
	echo "<p>$((b_free*b_size/1024/1024)) MB free</p>"
}

p_mem () {
	echo '<pre>'
	free
	echo '</pre>'
}

p_load () {
	echo '<pre>'
	cat /proc/loadavg
	echo '</pre>'
}

header Content-Type "text/html; charset=utf-8"
date=$(date -R)
out=""
header Date $date
header Last-Modified $date
	
path=$(realpath "$home/$QUERY_STRING")
[ -z "$out" -a $? -ne 0 ] && {
	out="<H1>Not found</H1>"
	header Status "404 Not found"
}

hl=${#home}
[ -z "$out" -a "${path:0:$hl}" != "$home" ] && {
	out="<H1>Access denied: ${path:0:$hl} is not in $home</H1>"
	header Status "403 Forbidden"
}

cd "$path"
[ -z "$out" -a $? -ne 0 ] && {
	out="<H1>Access denied</H1>"
	header Status "403 Forbidden"
}

header Status "200 OK"
echo -e "\r"

echo "<html><head><title>Listing for $QUERY_STRING</title></head><body>"

[ "$out" ] && { echo "$out"; fin; }

echo "<a href='..'>UP</a>"
{
	echo '<p><table border=1><tbody>'
	do_find d | while read line; do
		p_dir "$QUERY_STRING$line" "$line"
	done
	echo '</tbody></table></p>'
	echo '<p><table border=1><tbody>'
	do_find f | while read line; do
		p_file "$QUERY_STRING$line" "$line"
	done 
	echo '</tbody></table></p>'
} | sed -re 's@\.000000000(</td>)@\1@g'
p_stat
#p_mem
#p_load
fin
