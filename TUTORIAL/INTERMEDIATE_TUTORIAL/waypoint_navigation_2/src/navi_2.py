#!/usr/bin/env python

"""
    navi_2.py - enable turtlebot to navigate to predefined location based on voice command

"""

import roslib; roslib.load_manifest('pi_speech_tutorial')
import rospy
from std_msgs.msg import String

import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped, Point, Quaternion, Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from tf.transformations import quaternion_from_euler

from sound_play.libsoundplay import SoundClient
point = 1
original = 0
message = "none"
start = 0

class NavToPoint:
    def __init__(self):
        rospy.on_shutdown(self.cleanup)
          
        self.voice = rospy.get_param("~voice", "voice_don_diphone")
        self.wavepath = rospy.get_param("~wavepath", "")
        
        # Create the sound client object
        self.soundhandle = SoundClient()
        rospy.sleep(1)
        self.soundhandle.stopAll()

        # Subscribe to the recognizer output
        rospy.Subscriber('/recognizer/output', String, self.identify)

	# Publisher to manually control the robot
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist)

	# Subscribe to the move_base action server
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        rospy.loginfo("Waiting for move_base action server...")
        # Wait for the action server to become available
        self.move_base.wait_for_server(rospy.Duration(120))
        rospy.loginfo("Connected to move base server")

        # Announce that we are ready for input
        self.soundhandle.playWave(self.wavepath + "/R2D2a.wav")
        rospy.sleep(1)
        self.soundhandle.say("initiated", self.voice)
	rospy.sleep(1)

        # A variable to hold the initial pose of the robot to be set by the user in RViz
        initial_pose = PoseWithCovarianceStamped()
        rospy.Subscriber('initialpose', PoseWithCovarianceStamped, self.update_initial_pose)

	# Get the initial pose from the user
	self.soundhandle.say("Where am I", self.voice)
        rospy.loginfo("*** Click the 2D Pose Estimate button in RViz to set the robot's initial pose...")
        rospy.wait_for_message('initialpose', PoseWithCovarianceStamped)
        self.last_location = Pose()
        
        # Make sure we have the initial pose
        while initial_pose.header.stamp == "":
        	rospy.sleep(1)
            
        self.soundhandle.say("Ready to go", self.voice)
	rospy.sleep(1)


	locations = dict()

	quaternion = quaternion_from_euler(0.0, 0.0, 1.5708)
	locations['A'] = Pose(Point(0.5, 0.5, 0.000), Quaternion(quaternion[0], quaternion[1], quaternion[2], quaternion[3]))

	quaternion = quaternion_from_euler(0.0, 0.0, 3.1412)
	locations['B'] = Pose(Point(0.5, -0.5, 0.000), Quaternion(quaternion[0], quaternion[1], quaternion[2], quaternion[3]))

	quaternion = quaternion_from_euler(0.0, 0.0, -1.5708)
	locations['C'] = Pose(Point(1.0, 1.0, 0.000), Quaternion(quaternion[0], quaternion[1], quaternion[2], quaternion[3]))

	quaternion = quaternion_from_euler(0.0, 0.0, 0.0)
	locations['D'] = Pose(Point(1.0, -1.0, 0.000), Quaternion(quaternion[0], quaternion[1], quaternion[2], quaternion[3]))

	self.goal = MoveBaseGoal()
        rospy.loginfo("Starting navigation test")

	while not rospy.is_shutdown():
	  self.goal.target_pose.header.frame_id = 'map'
	  self.goal.target_pose.header.stamp = rospy.Time.now()
	  if start == 1:
		if message == "point A":
		  # Assume point A is Argentina
		  self.soundhandle.say("Going to Argentina", self.voice)
		  rospy.sleep(2)
		  self.goal.target_pose.pose = locations['A']
	  	  self.move_base.send_goal(self.goal)
		  waiting = self.move_base.wait_for_result(rospy.Duration(300))
		  if waiting == 1:
		    self.soundhandle.say("Reached Argentina", self.voice)
		    rospy.sleep(2)
		    self.soundhandle.say("Ready for next location", self.voice)
		    rospy.sleep(2)
		    global start
		    start = 0

		if message == "point B":
		  # Assume point B is Brazil
		  self.soundhandle.say("Going to Brazil", self.voice)
		  rospy.sleep(2)
		  self.goal.target_pose.pose = locations['B']
		  self.move_base.send_goal(self.goal)
		  waiting = self.move_base.wait_for_result(rospy.Duration(300))
		  if waiting == 1:
		    self.soundhandle.say("Reached Brazil", self.voice)
		    rospy.sleep(2)
		    self.soundhandle.say("Ready to go", self.voice)
		    rospy.sleep(2)
		    global start
		    start = 0

		if message == "point C":
		  # Assume point C is China
		  self.soundhandle.say("Going to China", self.voice)
		  rospy.sleep(2)
		  self.goal.target_pose.pose = locations['C']
		  self.move_base.send_goal(self.goal)
		  waiting = self.move_base.wait_for_result(rospy.Duration(300))
		  if waiting == 1:
		    self.soundhandle.say("Reached China", self.voice)
		    rospy.sleep(2)
		    self.soundhandle.say("Ready for next place", self.voice)
		    rospy.sleep(2)
		    global start
		    start = 0

		if message == "point D":
		  # Assume point D is Denmark
		  self.soundhandle.say("Going to Denmark", self.voice)
		  rospy.sleep(2)
		  self.goal.target_pose.pose = locations['D']
		  self.move_base.send_goal(self.goal)
		  waiting = self.move_base.wait_for_result(rospy.Duration(300))
		  if waiting == 1:
		    self.soundhandle.say("Reached Denmark", self.voice)
		    rospy.sleep(2)
		    self.soundhandle.say("Where is my next location", self.voice)
		    rospy.sleep(2)
		    global start
		    start = 0

		if message == "origin":
		  self.soundhandle.say("Going back home", self.voice)
		  rospy.sleep(2)
		  self.goal.target_pose.pose = self.origin
		  self.move_base.send_goal(self.goal)
		  waiting = self.move_base.wait_for_result(rospy.Duration(300))
		  if waiting == 1:
		    self.soundhandle.say("Reached home", self.voice)
		    rospy.sleep(2)
		    global start
		    start = 0

		rospy.Rate(3).sleep()

    def update_initial_pose(self, initial_pose):
        self.initial_pose = initial_pose
	if original == 0:
		self.origin = self.initial_pose.pose.pose
		global original
		original = 1

    def identify(self, msg):
        # Print the recognized words on the screen
        if msg.data == 'go to argentina' or msg.data == 'argentina':
		global message
		message = "point A"
		rospy.loginfo(message)
		global start
		start = 1
        elif msg.data == 'go to brazil' or msg.data == 'brazil':
		global message
		message = "point B"
		rospy.loginfo(message)
		global start
		start = 1
	elif msg.data == 'go to china' or msg.data == 'china':
		global message
		message = "point C"
		rospy.loginfo(message)
		global start
		start = 1
	elif msg.data == 'go to denmark' or msg.data == 'denmark':
		global message
		message = "point D"
		rospy.loginfo(message)
		global start
		start = 1
        elif msg.data == 'go back to original place' or msg.data == 'go back' or msg.data == 'original' or msg.data == 'go home':
		global message
		message = "origin"
		rospy.loginfo(message)
		global start
		start = 1

    def cleanup(self):
        rospy.loginfo("Shutting down navigation	....")
	self.move_base.cancel_goal()
        self.cmd_vel_pub.publish(Twist())

if __name__=="__main__":
    rospy.init_node('navi_point')
    try:
        NavToPoint()
        rospy.spin()
    except:
        pass

