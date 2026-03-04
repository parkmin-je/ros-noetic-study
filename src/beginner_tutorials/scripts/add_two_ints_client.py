#!/usr/bin/env python3
import sys
import rospy
from beginner_tutorials.srv import AddTwoInts

def add_two_ints_client(x, y):
    rospy.wait_for_service('add_two_ints')
    try:
        add_two_ints = rospy.ServiceProxy('add_two_ints', AddTwoInts)
        resp = add_two_ints(x, y)
        return resp.sum
    except rospy.ServiceException as e:
        rospy.logerr("서비스 호출 실패: %s" % e)

if __name__ == "__main__":
    x = int(sys.argv[1])
    y = int(sys.argv[2])
    rospy.loginfo("요청: %d + %d" % (x, y))
    print("결과: %d" % add_two_ints_client(x, y))