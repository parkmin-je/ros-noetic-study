#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class ObstacleAvoider:
    def __init__(self):
        rospy.init_node('obstacle_avoider')
        self.cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        rospy.Subscriber('/scan', LaserScan, self.scan_callback)
        self.safe_distance = 0.7  # 감지 거리 늘림
        self.turning = False
        self.turn_count = 0
        rospy.loginfo("장애물 회피 노드 시작!")

    def get_valid_min(self, ranges):
        valid = [r for r in ranges if r == r and r != float('inf') and r > 0.01]
        return min(valid) if valid else 999

    def scan_callback(self, msg):
        twist = Twist()
        ranges = msg.ranges
        total = len(ranges)

        # 정면 / 좌측 / 우측 분리
        front = ranges[total//2 - 20 : total//2 + 20]
        left  = ranges[total//2 + 20 : total//2 + 60]
        right = ranges[total//2 - 60 : total//2 - 20]

        front_min = self.get_valid_min(front)
        left_min  = self.get_valid_min(left)
        right_min = self.get_valid_min(right)

        rospy.loginfo(f"전방: {front_min:.2f} 좌: {left_min:.2f} 우: {right_min:.2f}")

        if front_min < self.safe_distance:
            # 장애물 감지 → 더 넓은 쪽으로 회전
            twist.linear.x = 0.0
            if left_min > right_min:
                twist.angular.z = 0.8   # 왼쪽이 넓으면 왼쪽으로
                rospy.loginfo("← 왼쪽 회전")
            else:
                twist.angular.z = -0.8  # 오른쪽이 넓으면 오른쪽으로
                rospy.loginfo("→ 오른쪽 회전")
        else:
            # 직진
            twist.linear.x = 0.3
            twist.angular.z = 0.0

        self.cmd_pub.publish(twist)

if __name__ == '__main__':
    avoider = ObstacleAvoider()
    rospy.spin()
