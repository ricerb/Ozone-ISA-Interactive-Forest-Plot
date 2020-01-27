#!/usr/bin/env bash

cd ~/dev/Ozone-ISA-Interactive-Forest-Plot/
./venv/bin/gunicorn -w 2 -b 0.0.0.0:8050  fp_ozone_resp:server

