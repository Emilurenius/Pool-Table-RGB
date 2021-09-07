#!/bin/bash

cd /
cd home/pi/projects/Pool-Table-RGB/PiCode/server
node app.js 3000 &
cd ..
sleep 5s
python3 lightController.py &