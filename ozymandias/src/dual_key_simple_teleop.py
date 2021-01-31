#!/usr/bin/env python3
import rospy
import pygame
import threading
from std_msgs.msg import Int32

angular_speed = 50
linear_speed = 100

rkey = False
lkey = False
upkey = False
downkey = False

def handle_input():
    global rkey, lkey, upkey, downkey
    while not(rospy.is_shutdown()):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        upkey = True
                    if event.key == pygame.K_DOWN:
                        downkey = True
                    if event.key == pygame.K_LEFT:
                        rkey = True
                    if event.key == pygame.K_RIGHT:
                        lkey = True
            if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        upkey = False
                    if event.key == pygame.K_DOWN:
                        downkey = False
                    if event.key == pygame.K_LEFT:
                        rkey = False
                    if event.key == pygame.K_RIGHT:
                        lkey = False
def handle_vel():
    left_pub = rospy.Publisher('left_motor', Int32, queue_size = 10)
    right_pub = rospy.Publisher('right_motor', Int32, queue_size = 10)
    left = Int32()
    right = Int32()
    while not(rospy.is_shutdown()):
        if(upkey and (lkey or rkey)):
            if(upkey and lkey):
                left.data = linear_speed
                right.data = angular_speed
            elif(upkey and rkey):
                left.data = angular_speed
                right.data = linear_speed
        elif(downkey and (lkey or rkey)):
            if(downkey and lkey):
                left.data = -linear_speed
                right.data = -angular_speed
            elif(downkey and rkey):
                left.data = -angular_speed
                right.data = -linear_speed
        elif(upkey):
            left.data = linear_speed
            right.data = linear_speed
        elif(downkey):
            left.data = -linear_speed
            right.data = -linear_speed
        elif(lkey):
            left.data = angular_speed
            right.data = -angular_speed
        elif(rkey):
            left.data = -angular_speed
            right.data = angular_speed
        else:
            left.data = 0
            right.data = 0
        left_pub.publish(left)
        right_pub.publish(right)
        rate.sleep()

if __name__=='__main__':
    rospy.init_node('simplest_teleop')
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    rate = rospy.Rate(10)

    input = threading.Thread(target = handle_input)
    input.start()

    output = threading.Thread(target = handle_vel)
    output.start()
