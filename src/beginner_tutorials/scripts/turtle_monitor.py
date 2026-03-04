#!/usr/bin/env python3
import rospy
from turtlesim.msg import Pose

def callback(msg):
    x = msg.x
    y = msg.y

    if x <= 1.0 or x >= 10.0 or y <= 1.0 or y >= 10.0:
        rospy.logwarn("⚠️ 경고! 거북이가 벽에 가까워짐! x=%.2f, y=%.2f", x, y)
    else:
        rospy.loginfo("위치 정상 — x=%.2f, y=%.2f", x, y)

def listener():
    rospy.init_node('turtle_monitor')
    rospy.Subscriber('/turtle1/pose', Pose, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()