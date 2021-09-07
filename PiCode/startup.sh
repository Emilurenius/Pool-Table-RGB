#!/bin/bash

cd /
cd home/pi/projects/Pool-Table-RGB/PiCode/server
node app.js 3000 &
cd ..
python3 lightController.py &