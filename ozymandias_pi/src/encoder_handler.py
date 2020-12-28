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
    states_publisher = rospy.Publisher('joint_states', JointState, queue_size = 10)
    state = JointState()
    
    while not (rospy.is_shutdown()):
        state.header.stamp = rospy.Time.now()
        state.name = 'leftFrontWheelJoint','rightFrontWheelJoint'
        state.position = [(left_encoder_pulses * (2 * 3.141526)) / 750,(right_encoder_pulses * (2 * 3.141526)) / 750] #750 pulses per rotation, conversion to rad
        states_publisher.publish(state)
    
if __name__=='__main__':
    rospy.init_node('encoder_handler')
    rate = rospy.Rate(100)
    left_encoder_pulses_sub = rospy.Subscriber('left_encoder', Int32, left_callback)
    right_encoder_pulses_sub = rospy.Subscriber('right_encoder', Int32, right_callback)
    
    pulses_to_JointState()