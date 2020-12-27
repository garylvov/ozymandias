#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import JointState
from std_msgs.msg import Int32

left_encoder_pulses = 0
right_encoder_pulses = 0

def left_callback(msg):
    global left_encoder_pulses
    left_encoder_pulses = msg.data
    
def right_callback(msg):
    global right_encoder_pulses
    right_encoder_pulses = msg.data
    
def pulses_to_JointState():
    left_wheel_pub = rospy.Publisher('left_wheel_JointState', JointState, queue_size = 10)
    right_wheel_pub = rospy.Publisher('right_wheel_JointState', JointState, queue_size = 10)
    left_state = JointState()
    right_state = JointState()
    
    while not (rospy.is_shutdown()):
        left_state.position = [(left_encoder_pulses * (2 * 3.141526)) / 750] #750 pulses per rotation, conversion to rad
        right_state.position = [(right_encoder_pulses * (2 * 3.141526)) / 750]
        
        left_wheel_pub.publish(left_state)
        right_wheel_pub.publish(right_state)
    
if __name__=='__main__':
    rospy.init_node('encoder_handler')
    
    left_encoder_pulses_sub = rospy.Subscriber('left_encoder', Int32, left_callback)
    right_encoder_pulses_sub = rospy.Subscriber('right_encoder', Int32, right_callback)
    
    pulses_to_JointState()
