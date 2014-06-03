#!/usr/bin/env python

import roslib
import rospy
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, Point, Quaternion, Twist
from tf.transformations import quaternion_from_euler
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from math import pi

class NavTest():
    def __init__(self):
        rospy.init_node('nav_test', anonymous=True)
        
#        rospy.on_shutdown(self.shutdown)
        
        # Publisher to manually control the robot (e.g. to stop it)
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist)
        
        # Subscribe to the move_base action server
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        
        rospy.loginfo("Waiting for move_base action server...")
        
        # Wait 60 seconds for the action server to become available
        self.move_base.wait_for_server(rospy.Duration(60))
        
        rospy.loginfo("Connected to move base server")
                
        #create goal                                                            
        goal = MoveBaseGoal()

        #set goal
        goal.target_pose.pose.position.x = 0.0
        goal.target_pose.pose.position.y = 1.0
        goal.target_pose.pose.orientation.w = 1.0
        goal.target_pose.header.frame_id = 'map'
        goal.target_pose.header.stamp = rospy.Time.now()
        
        # Start the robot toward the next location
        self.move_base.send_goal(goal)
            
        # Allow 30 seconds to get there
        finished_within_time = self.move_base.wait_for_result(rospy.Duration(30))

        rospy.loginfo("OK 1")

    def shutdown(self):
        rospy.loginfo("Stopping the robot...")
        #self.move_base.cancel_goal()
        rospy.sleep(2)
        self.cmd_vel_pub.publish(Twist())
        rospy.sleep(1)

if __name__ == '__main__':
    try:
        x = NavTest()
        rospy.sleep(2)
        x.shutdown()
        rospy.loginfo("OK 2")
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")
