#!/usr/bin/env python

# start navigation (ex. amcl_demo.launch)

import roslib
import rospy
import actionlib

#move_base_msgs
from move_base_msgs.msg import *

def stop_move():

        #initialize node
        rospy.init_node('stop_move')

        #Simple Action Client - The simple action client is used to send actions to the
        #robot through a system of "goals". Here, we are setting the parameters as a
        #move_base goal, which is in charge of moving the robot.
        sac = actionlib.SimpleActionClient('move_base', MoveBaseAction )

        #create goal
        #goal = MoveBaseGoal()

        #set goal
        #goal.target_pose.pose.position.x = 1.0
        #goal.target_pose.pose.orientation.w = 1.0
        #goal.target_pose.header.frame_id = 'map'
        #goal.target_pose.header.stamp = rospy.Time.now()

        #start listener
        sac.wait_for_server()

        #send goal
        sac.cancel_goal()

        #finish
        sac.wait_for_result()

        #print result
        rospy.loginfo(sac.get_result())

if __name__ == '__main__':
    try:
        stop_move()
    except rospy.ROSInterruptException:
        print "Keyboard Interrupt"
