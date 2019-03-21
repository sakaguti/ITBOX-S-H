#!/bin/sh
echo $1
/usr/bin/sudo /bin/systemctl $1 mjpg-streamer
