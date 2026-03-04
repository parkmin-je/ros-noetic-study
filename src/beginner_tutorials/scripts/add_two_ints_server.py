#!/usr/bin/env python3
from beginner_tutorials.srv import AddTwoInts, AddTwoIntsResponse
import rospy

def handle_add_two_ints(req):
    result = req.a + req.b
    rospy.loginfo("요청: %s + %s = %s" % (req.a, req.b, result))
    return AddTwoIntsResponse(result)

def add_two_ints_server():
    rospy.init_node('add_two_ints_server')
    s = rospy.Service('add_two_ints', AddTwoInts, handle_add_two_ints)
    rospy.loginfo("두 정수 덧셈 서비스 준비 완료!")
    rospy.spin()

if __name__ == "__main__":
    add_two_ints_server()