#!/bin/sh

fin () {
	echo '</body></html>'
	exit 0
}

header () {
	echo -n "$1: "
	shift
	echo -e "$*\r"
}

urlencode () {
	echo "$1" | sed -e "s/'/%27/g" -e "s/\?/%3f/g"
}

[ -z "$INCLUDE_HTTPLIB" ] && exit -1
