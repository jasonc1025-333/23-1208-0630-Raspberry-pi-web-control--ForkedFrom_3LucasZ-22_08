#!/bin/bash
echo Starting Script
/usr/bin/expect -c '
   spawn systemctl stop roboQuestUI.service
   expect "Password: "
   send "ubuntu\n"
   expect "==== AUTHENTICATION COMPLETE ==="

   spawn systemctl stop powerDownWatch.service
   expect "Password: "
   send "ubuntu\n"
   expect "==== AUTHENTICATION COMPLETE ==="
'

cd /home/ubuntu/catkin_ws/src/experiments
source env/bin/activate
cd /home/ubuntu/catkin_ws/src/experiments/Raspberry-pi-web-control
echo Script finished