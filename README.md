# Overview

Ozymandias is created with ROS. Ozymandias is meant to enable Teleop, Navigation, and SLAM from a differential drive and lidar.

## Three folders, Three machines
**ozymandias** runs on a full desktop install of ROS Noetic, with many packages: the navigation stack, the hector_slam package, and all required rosdeps.

How to install noetic on a computer: http://wiki.ros.org/noetic/Installation

**ozymandias_pi** runs on a raspberry pi 4, using ROS Noetic built from source, with some additional packages: Rosserial, RPlidar, common_msgs, usb_cam, and all required rosdeps (except tf and rosbag migration. Using the rosdep tool says it needs these packages, but it should work without them.) 

How to install noetic on pi https://varhowto.com/install-ros-noetic-raspberry-pi-4/

**arduino** contains the script to load onto an arduino mega. The Rosserial libary needs to be added to the arduino IDE, which can be done through the library manager.

The arduino communicates via a rosserial wired connection with the rasp pi. The rasp pi communicates via ssh wireless connection with the full desktop install.

## Components

Parts bill (approx $270 of electronics):

https://docs.google.com/spreadsheets/d/13E-844a8HjoTu_wGjwuedb2U05IyiHjkcKU0VbZ1k_E/edit?usp=sharing

Wiring Schematic:

https://docs.google.com/drawings/d/1u5N3b1Fn6B7iz71muJR3zRIVmPBXByMRte5-a001hI8/edit?usp=sharing

# Website
https://garylvov.com
# YouTube Channel:
https://www.youtube.com/channel/UCC3ApHQWzKKH0EaZwGiQIEA
