#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist

def turtle_circle():
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rospy.init_node('turtle_circle')
    rate = rospy.Rate(10)

    msg = Twist()
    msg.linear.x = 2.0   # 직진 속도
    msg.angular.z = 1.0  # 회전 속도

    while not rospy.is_shutdown():
        pub.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        turtle_circle()
    except rospy.ROSInterruptException:
        pass