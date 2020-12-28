cmake_minimum_required(VERSION 3.0.2)
project(ozymandias_pi)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  sensor_msgs
  std_msgs
  rosserial_python
)

catkin_package()

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

