#!/usr/bin/env python3
import rospy
import pygame
from std_msgs.msg import Int32

def handle_input():
    left_pub = rospy.Publisher('left_motor', Int32, queue_size = 10)
    right_pub = rospy.Publisher('right_motor', Int32, queue_size = 10)
    left = Int32()
    right = Int32()

    while not(rospy.is_shutdown()):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    left.data = 255
                    right.data = 255
                if event.key == pygame.K_DOWN:
                    left.data = -255
                    right.data = -255
                if event.key == pygame.K_LEFT:
                    left.data = -100
                    right.data = 100
                if event.key == pygame.K_RIGHT:
                    left.data = 100
                    right.data = -100
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
    handle_input()
