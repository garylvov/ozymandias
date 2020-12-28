cmake_minimum_required(VERSION 3.0.2)
project(ozymandias)

find_package(catkin REQUIRED COMPONENTS
  diff_drive_controller
  geometry_msgs
  hector_mapping
  robot_state_publisher
  roscpp
  rospy
  sensor_msgs
  std_msgs
)

catkin_package()

include_directories(${catkin_INCLUDE_DIRS})

