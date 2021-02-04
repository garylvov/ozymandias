#!/usr/bin/env python3
import rospy
import threading
from std_msgs.msg import Float32, Int32

vel = 0

def vel_callback(msg):
    global vel
    vel = msg.data

def handle_vel():
    vel_pub = rospy.Publisher('left_motor', Int32, queue_size = 10)
    command_speed = Int32()
    command_speed.data = 0
    while not (rospy.is_shutdown()):
        if(vel < 10.00):
            command_speed.data += 5
        if(vel > 10.00):
            command_speed.data -=5
        vel_pub.publish(command_speed)
        rate.sleep()
if __name__=='__main__':
    rospy.init_node('vel_test')
    vel_sub = rospy.Subscriber('left_vel', Float32, vel_callback)
    rate = rospy.Rate(.75)
    handle_vel()
