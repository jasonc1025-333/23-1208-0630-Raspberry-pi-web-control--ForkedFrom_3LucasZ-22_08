#!/bin/bash
echo Starting Script!
# START:
systemctl stop roboQuestUI.service
ubuntu
cd /home/ubuntu/catkin_ws/src/experiments
source env/bin/activate
cd /home/ubuntu/catkin_ws/src/experiments/Raspberry-pi-web-control/FinalVersions/Version1
python3.9 __init__.py
systemctl stop powerDownWatch.service

# STOP:
# systemctl start powerDownWatch.service