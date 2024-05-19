# Raspberry-Pi-web-control

23-1123-1040 JasonC:
* FinalVersions: Best (since only version combining VideoStream w/ MotorControl [24-0519-0830])
  * SocketIO: Final
* Websocket-Robot: Better
  * SocketIO: Prototype
* Flask-Robot: Good
  * Sending raw 'jpg' 
* No-UI-Robot: Nothing
  * No GUI, Manual Code Control

Controlling a Raspberry Pi based robot with any device using websites.
Everything happens realtime!

Current features:
- No UI Robot
  - Basic robot driving
  - Single picture with camera
  - Print continuous lidar Data
- Flask Robot
  - Robot driving (with arrow keys, buttons)
  - Camera pictures (by refreshing the page, you get a new picture)
- Websocket Robot
  - Robot driving (with arrow keys, buttons)
  - Camera Video Stream
  - Lidar Data Graphing
- Final Versions
  - Version1 (Complete Robot Driving Web UI)
- ROS integration (COMING SOON!)

Many of these scripts have little documentation, comments but will soon have.

Basic materials needed:
- Raspberry Pi 4 (Ubuntu)
- Raspberry Pi Camera 
- Slamtec RPLidar A1 M8
- Motor Controller Board
- 2 Motors

How to use:
- Clone repository to a local machine
- Set up and activate a virtual environment under the main directory
- pip3.9 install -r requirements.txt (install all needed python modules)
- Each project has a main python script to run (either init.py, main.py, or server.py)
- after running the python script, go to Google Chrome and type the IP Address of the robot
