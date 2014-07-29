#!/usr/bin/env python

"""
    turtlebot_arm_2.py - move turtlebot arm according to predefined gestures using built in buttons

"""

import roslib; roslib.load_manifest('kobuki_testsuite');
import rospy
from std_msgs.msg import Float64
from kobuki_msgs.msg import ButtonEvent

# assign random number to prevent wrong identity and status of button
button = 5
button_state = 5

class Loop:
    def __init__(self):
        rospy.on_shutdown(self.cleanup)


    	# Subscribe to the /mobile_base/events/button topic to receive built-in button input
    	rospy.Subscriber('/mobile_base/events/button', ButtonEvent, self.ButtonEventCallback)


	# publish command message to joints/servos of arm
    	self.joint1 = rospy.Publisher('/arm_shoulder_pan_joint/command',Float64)
	self.joint2 = rospy.Publisher('/arm_shoulder_lift_joint/command',Float64)
    	self.joint3 = rospy.Publisher('/arm_elbow_flex_joint/command',Float64)
    	self.joint4 = rospy.Publisher('/arm_wrist_flex_joint/command',Float64)
	self.joint5 = rospy.Publisher('/gripper_joint/command',Float64)
	self.pos1 = Float64()
    	self.pos2 = Float64()
    	self.pos3 = Float64()
    	self.pos4 = Float64()
    	self.pos5 = Float64()
	
	# Initial gesture of robot arm
	self.pos1 = 1.565
	self.pos2 = 2.102
	self.pos3 = -2.439
	self.pos4 = -1.294
	self.pos5 = 0.0
	self.joint1.publish(self.pos1)
	self.joint2.publish(self.pos2)
	self.joint3.publish(self.pos3)
	self.joint4.publish(self.pos4)
	self.joint5.publish(self.pos5)

	while not rospy.is_shutdown():
      	    if button == 0:
		if button_state == 1:
	    		# gesture 1
	    		self.pos1 = 1.559
	    		self.pos2 = 0.215
	    		self.pos3 = -1.508
	    		self.pos4 = -0.496
	    		self.pos5 = 0.0
			rospy.sleep(3)
		
      	    if button == 1:
		if button_state == 1:
	    		# gesture 2
	    		self.pos1 = 1.565
	    		self.pos2 = -2.393
	    		self.pos3 = -0.639
	    		self.pos4 = 1.335
	    		self.pos5 = -0.430
			rospy.sleep(3)

      	    if button == 2:
		if button_state == 1:
	    		# initial gesture
	    		self.pos1 = 1.565
	    		self.pos2 = 2.102
	    		self.pos3 = -2.439
	    		self.pos4 = -1.294
	    		self.pos5 = 0.0
			rospy.sleep(3)


	    self.joint1.publish(self.pos1)
	    self.joint2.publish(self.pos2)
	    self.joint3.publish(self.pos3)
	    self.joint4.publish(self.pos4)
	    self.joint5.publish(self.pos5)
      	    rospy.Rate(5).sleep()


    def ButtonEventCallback(self,data1):
    	global button
    	global button_state
    	button = data1.button
    	button_state = data1.state


    def cleanup(self):
        rospy.loginfo("Shutting down turtlebot arm....")

if __name__=="__main__":
    rospy.init_node('turtlebot_arm')
    try:
        Loop()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

