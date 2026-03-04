#!/usr/bin/env python3
import rospy
import random
from std_msgs.msg import Float32

def temp_publisher():
    pub = rospy.Publisher('temperature', Float32, queue_size=10)
    rospy.init_node('temp_pub')
    rate = rospy.Rate(1)

    while not rospy.is_shutdown():
        temp = random.uniform(20.0, 40.0)
        rospy.loginfo("온도 발행: %.1f°C", temp)
        pub.publish(temp)
        rate.sleep()

if __name__ == '__main__':
    try:
        temp_publisher()
    except rospy.ROSInterruptException:
        pass