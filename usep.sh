#!/bin/bash

echo $1
if [ "$1"x = "py3"x ];then
	echo "use python3."
	rm /usr/bin/python
	ln -s /usr/bin/python3 /usr/bin/python
elif [ "$1"x = "py2"x ];then
	echo "use python2."
	rm /usr/bin/python
    ln -s /usr/bin/python2 /usr/bin/python
else
	echo "do not change python version."
fi
