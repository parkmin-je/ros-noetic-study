#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float32

def callback(msg):
    if msg.data >= 35.0:
        rospy.logwarn("⚠️ 경고! 고온 감지: %.1f°C", msg.data)
    else:
        rospy.loginfo("온도 수신: %.1f°C", msg.data)

def listener():
    rospy.init_node('temp_sub')
    rospy.Subscriber('temperature', Float32, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()