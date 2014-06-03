#!/usr/bin/env python

import roslib
import rospy
import actionlib
from geometry_msgs.msg import *
from move_base_msgs.msg import *

def set_pose():
    rospy.init_node('set_pose')

    location =  Pose(Point(15.322, 11.611, 0.000), Quaternion(0.000, 0.000, 0.629, 0.777))
    self.goal = MoveBaseGoal()
    self.goal.target_pose.pose = location
    self.goal.target_pose.header.frame_id = 'map'
    self.goal.target_pose.header.stamp = rospy.Time.now()
    
    self.move_base.send_goal(self.goal)
    
    time = self.move_base.wait_for_result(rospy.Duration(300))
    
if __name__ == '__main__':
    try:
        set_pose()
        rospy.loginfo("done")
    except Exception, e:
        print "error: ", e
