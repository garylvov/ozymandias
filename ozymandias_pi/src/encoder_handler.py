#!/usr/bin/env python3
import rospy
import threading
from sensor_msgs.msg import JointState
from std_msgs.msg import Int32

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

def pulses_to_velocity(name, pulses):
    vel_pub = rospy.Publisher(name, Int32, queue_size = 10)
    vel = Int32()
    previous_time = 0
    previous_pulses = pulses

    while not (rospy.is_shutdown()):
        now = rospy.Time.now()
        if(now - previous_time >= 1):
            # velocity = Δ displacement / Δ time
            vel.data = (pulses - previous_pulses) / (now - previous_time)
            vel.data *= conversion_factor
            previous_time = now
            previous_pulses = pulses
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

    left_vel = threading.Thread(target = pulses_to_velocity, kwargs = dict(name = 'left_vel', pulses = left_encoder_pulses))
    left_vel.start()

    right_vel = threading.Thread(target = pulses_to_velocity, kwargs = dict(name = 'right_vel', pulses = right_encoder_pulses))
    right_vel.start()
