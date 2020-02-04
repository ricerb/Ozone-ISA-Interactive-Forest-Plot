#!/usr/bin/env bash

cd ~/dev/Ozone-ISA-Interactive-Forest-Plot

./venv/bin/gunicorn \
	-w 2 \
	-b 0.0.0.0:8050 \
	--chdir=. \
	--daemon \
	--log-file server-logs.txt \
	--access-logfile access-logs.txt \
	app:server

