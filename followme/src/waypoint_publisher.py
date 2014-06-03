#!/usr/bin/env python

import rospy
import actionlib
import roslib

from geometry_msgs.msg import PoseStamped
from std_msgs.msg import String

def waypoint_publisher():
    pub = rospy.Publisher('/move_base_simple/goal', PoseStamped)
    rospy.init_node('waypoint_publisher', anonymous=True)
    r = rospy.Rate(1) # 10hz
    while not rospy.is_shutdown():
        PoseStamped.frame_id="map"
        PoseStamped.x = 0.5
        PoseStamped.y = 0.5
        PoseStamped.w = 1.0
        rospy.loginfo(PoseStamped)
        pub.publish(PoseStamped)
        r.sleep()

if __name__ == '__main__':
    try:
        waypoint_publisher()
    except rospy.ROSInterruptException: pass
