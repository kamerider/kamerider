#!/usr/bin/env python

# start navigation (ex. amcl_demo.launch)

import roslib
import rospy
import actionlib

from geometry_msgs.msg import Twist

#move_base_msgs
from move_base_msgs.msg import *

class NavTest():
    def __init__(self):
        rospy.init_node('nav_test', anonymous=True)
        
        rospy.on_shutdown(self.shutdown)
        
        # Publisher to manually control the robot (e.g. to stop it)
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist)
        
        # Subscribe to the move_base action server
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        
        rospy.loginfo("Waiting for move_base action server...")
        
        # Wait 60 seconds for the action server to become available
        self.move_base.wait_for_server(rospy.Duration(60))
        
        rospy.loginfo("Connected to move base server")
        
    def shutdown(self):
        rospy.loginfo("Stopping the robot...")
        #self.move_base.cancel_goal()
        #rospy.sleep(1)
        self.cmd_vel_pub.publish(Twist())
        #rospy.sleep(1)

if __name__ == '__main__':
    try:
        x = NavTest()
        x.shutdown()
    except rospy.ROSInterruptException:
        print "Keyboard Interrupt"
