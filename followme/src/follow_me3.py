#!/usr/bin/env python
import roslib; roslib.load_manifest('turtlebot_follower')

import sys

import rospy
from turtlebot_msgs.srv import *

if __name__ == "__main__":
    x = 0
    rospy.wait_for_service('/turtlebot_follower/change_state')
    try:
        change_state = rospy.ServiceProxy('/turtlebot_follower/change_state', SetFollowState)
        resp1 = change_state(x)
        print resp1
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e
