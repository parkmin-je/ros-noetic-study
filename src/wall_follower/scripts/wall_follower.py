#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import math

WALL_DIST_TARGET = 0.4
WALL_DIST_MARGIN = 0.15
FRONT_STOP_DIST  = 0.45
FRONT_TURN_DIST  = 0.6
LINEAR_SPEED     = 0.18
ANGULAR_SPEED    = 0.5
KP               = 1.2

class WallFollower:
    def __init__(self):
        rospy.init_node('wall_follower')
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.sub = rospy.Subscriber('/scan', LaserScan, self.scan_callback)
        self.regions = {}
        self.state = 'find_wall'
        self.rate = rospy.Rate(10)

    def get_min_range(self, ranges, start, end, max_val=10.0):
        vals = [r for r in ranges[start:end] if not math.isnan(r) and not math.isinf(r)]
        return min(vals) if vals else max_val

    def scan_callback(self, scan):
        n = len(scan.ranges)
        # 180도 기준: 왼쪽(-90도) ~ 오른쪽(+90도)
        # ranges[0]=오른쪽, ranges[n/2]=정면, ranges[n-1]=왼쪽
        self.regions = {
            'right':       self.get_min_range(scan.ranges, 0,          int(n*0.2)),
            'front_right': self.get_min_range(scan.ranges, int(n*0.2), int(n*0.4)),
            'front':       self.get_min_range(scan.ranges, int(n*0.4), int(n*0.6)),
            'front_left':  self.get_min_range(scan.ranges, int(n*0.6), int(n*0.8)),
            'left':        self.get_min_range(scan.ranges, int(n*0.8), n),
        }

    def decide_state(self):
        r = self.regions
        if not r:
            return
        if r['front'] < FRONT_STOP_DIST:
            self.state = 'emergency_stop'
        elif r['front'] < FRONT_TURN_DIST:
            self.state = 'turn_left'
        elif r['right'] > WALL_DIST_TARGET + WALL_DIST_MARGIN and \
             r['front_right'] > WALL_DIST_TARGET + WALL_DIST_MARGIN:
            self.state = 'find_wall'
        else:
            self.state = 'follow_wall'

    def act(self):
        r = self.regions
        twist = Twist()
        if self.state == 'emergency_stop':
            twist.linear.x  = 0.0
            twist.angular.z = ANGULAR_SPEED * 1.5
        elif self.state == 'turn_left':
            twist.linear.x  = 0.05
            twist.angular.z = ANGULAR_SPEED
        elif self.state == 'find_wall':
            twist.linear.x  = LINEAR_SPEED
            twist.angular.z = -ANGULAR_SPEED * 0.4
        elif self.state == 'follow_wall':
            error = r['right'] - WALL_DIST_TARGET
            twist.linear.x  = LINEAR_SPEED
            twist.angular.z = -KP * error
            if r['front_right'] < WALL_DIST_TARGET:
                twist.angular.z = ANGULAR_SPEED * 0.5
        self.pub.publish(twist)

    def run(self):
        rospy.loginfo("Wall Follower 시작")
        while not rospy.is_shutdown():
            self.decide_state()
            self.act()
            if self.regions:
                rospy.loginfo("상태: %-15s | 전방: %.2f | 우측: %.2f | 좌측: %.2f",
                              self.state,
                              self.regions.get('front', 0),
                              self.regions.get('right', 0),
                              self.regions.get('left', 0))
            self.rate.sleep()

if __name__ == '__main__':
    try:
        wf = WallFollower()
        wf.run()
    except rospy.ROSInterruptException:
        pass
