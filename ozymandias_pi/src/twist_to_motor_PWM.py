#!/usr/bin/env python3
import rospy
from threading import Thread
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32, Int32

wheel_dist = 0.20955 #Distance between two wheels in meters
wheel_radius = 0.032512 #in meters

left_vel = 0
right_vel = 0

angular_vel = 0
linear_vel = 0

#Approximation of duty cycles correlating to rad/s
#in rad/s-------5---6---7---8, etc.
left_approx_cycle = [32, 40, 48, 56, 64, 76, 84, 92, 100, 108, 120, 132, 140, 148, 156, 164, 172, 184, 196, 210, 220, 232, 244]
right_approx_cycle = [32, 40, 48, 56, 64, 76, 84, 92, 100, 108, 120, 132, 140, 148, 156, 164, 172, 184, 196, 210, 220, 232, 244]

def left_vel_callback(msg):
    global left_vel
    left_vel = msg.data

def right_vel_callback(msg):
    global right_vel
    right_vel = msg.data

def twist_callback(msg):
    global angular_vel, linear_vel
    angular_vel = msg.angular.z
    linear_vel = msg.linear.x

def handle_left():
    left_pub = rospy.Publisher('left_motor', Int32, queue_size = 10)
    command = Int32()
    while not (rospy.is_shutdown()):
        desired = (linear_vel - angular_vel * wheel_dist / 2) / wheel_radius
        if(desired != 0):
            index = (abs(int(desired)) - 5)
            command.data = left_approx_cycle[index]

            if(abs(left_vel) < abs(desired)):
                left_approx_cycle[index] += 2
            elif(abs(left_vel) > abs(desired)):
                left_approx_cycle[index] -= 2

            if(desired < 0):
                command.data = left_approx_cycle[index] * -1
        else:
            command.data = 0
        left_pub.publish(command)
        rate.sleep()

def handle_right():
        right_pub = rospy.Publisher('right_motor', Int32, queue_size = 10)
        command = Int32()
        while not (rospy.is_shutdown()):
            desired = (linear_vel + angular_vel * wheel_dist / 2) / wheel_radius
            if(desired != 0):
                index = (abs(int(desired)) - 5)
                command.data = right_approx_cycle[index]

                if(abs(right_vel) < abs(desired)):
                    right_approx_cycle[index] += 2
                elif(abs(right_vel) > abs(desired)):
                    right_approx_cycle[index] -= 2

                if(desired < 0):
                    command.data = right_approx_cycle[index] * -1
            else:
                command.data = 0
            right_pub.publish(command)
            rate.sleep()

if __name__=='__main__':
    rospy.init_node('twist_to_motor_PWM')
    left_vel_sub = rospy.Subscriber('left_vel', Float32, left_vel_callback)
    right_vel_sub = rospy.Subscriber('right_vel', Float32, right_vel_callback)
    twist_sub = rospy.Subscriber('cmd_vel', Twist, twist_callback)
    rate = rospy.Rate(.75)

    left_handler = Thread(target = handle_left)
    right_handler = Thread(target = handle_right)
    left_handler.start()
    right_handler.start()
