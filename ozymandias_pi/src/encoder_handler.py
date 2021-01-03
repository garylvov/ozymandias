#!/usr/bin/env python3
import rospy
import threading
from sensor_msgs.msg import JointState
from std_msgs.msg import Float32, Int32

left_encoder_pulses = 0
right_encoder_pulses = 0

#approx. 750 pulses per rotation, conversion factor to radians
conversion_factor = (2 * 3.141526) / 750

def left_callback(msg):
    global left_encoder_pulses
    left_encoder_pulses = msg.data

def right_callback(msg):
    global right_encoder_pulses
    right_encoder_pulses = msg.data

def left_pulses_to_velocity():
    vel_pub = rospy.Publisher('left_vel', Float32, queue_size = 10)
    vel = Float32()
    previous_time = 0
    previous_pulses = left_encoder_pulses

    while not (rospy.is_shutdown()):
        now = rospy.Time.now().to_sec()
        if(now - previous_time >= .25):
            # velocity = Δ displacement / Δ time
            vel.data = (left_encoder_pulses - previous_pulses) / (now - previous_time)
            vel.data *= conversion_factor
            previous_time = now
            previous_pulses = left_encoder_pulses
            #Check to prevent wildy erroneous values
            if(-35 < int(vel.data) < 35):
                vel_pub.publish(vel)
    
def right_pulses_to_velocity():
    vel_pub = rospy.Publisher('right_vel', Float32, queue_size = 10)
    vel = Float32()
    previous_time = 0
    previous_pulses = right_encoder_pulses

    while not (rospy.is_shutdown()):
        now = rospy.Time.now().to_sec()
        if(now - previous_time >= .25):
            vel.data = (right_encoder_pulses - previous_pulses) / (now - previous_time)
            vel.data *= conversion_factor
            previous_time = now
            previous_pulses = right_encoder_pulses
            if(-35 < int(vel.data) < 35):
                vel_pub.publish(vel)
    
def pulses_to_JointState():
    states_pub = rospy.Publisher('joint_states', JointState, queue_size = 10)
    state = JointState()

    while not (rospy.is_shutdown()):
        state.header.stamp = rospy.Time.now()
        state.name = 'leftFrontWheelJoint','rightFrontWheelJoint'
        state.position = [left_encoder_pulses * conversion_factor, right_encoder_pulses * conversion_factor]
        states_pub.publish(state)

if __name__=='__main__':
    rospy.init_node('encoder_handler')
    left_encoder_pulses_sub = rospy.Subscriber('left_encoder', Int32, left_callback)
    right_encoder_pulses_sub = rospy.Subscriber('right_encoder', Int32, right_callback)

    jointstate = threading.Thread(target = pulses_to_JointState)
    jointstate.start()

    left_vel = threading.Thread(target = left_pulses_to_velocity)
    left_vel.start()

    right_vel = threading.Thread(target = right_pulses_to_velocity)
    right_vel.start()
