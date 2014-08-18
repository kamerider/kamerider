#!/usr/bin/env python

"""
    demo.py - demo program for Prof.Okada

"""

import roslib; roslib.load_manifest('pi_speech_tutorial'); roslib.load_manifest('cmvision'); roslib.load_manifest('kobuki_testsuite')

from kobuki_msgs.msg import DigitalInputEvent, Led, ButtonEvent, BumperEvent, DigitalOutput

import rospy
from std_msgs.msg import String, Float64
from sensor_msgs.msg import JointState
from cmvision.msg import Blobs

import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped, Point, Quaternion, Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from tf.transformations import euler_from_quaternion, quaternion_from_euler

from sound_play.libsoundplay import SoundClient
point = 1
original = 0
message = "none"
start = 0
hand = 0
name = "none"
position = 0.0

again = 0
count = 0
turn = 0.0
straight = 0.0
blob_position_x = 0
blob_position_y = 0

button = 0
button_state = 0
bumper = 0
bumper_state = 0

class Demo:
    def __init__(self):
        rospy.on_shutdown(self.cleanup)

	# Subscribe to the /mobile_base/events/bumper topic to receive bumper input
    	rospy.Subscriber('/mobile_base/events/bumper', BumperEvent, self.BumperEventCallback)

    	# publish Led messages to /mobile_base/commands/led1 & /mobile_base/commands/led1 topics to give Led signal
    	self.pub1 = rospy.Publisher('/mobile_base/commands/led1', Led)
    	self.pub2 = rospy.Publisher('/mobile_base/commands/led2', Led)
    	self.led1 = Led()
    	self.led2 = Led()
        
        # publish messages to /mobile_base/commands/digital_output to give digital signal
        #self.pub3 = rospy.Publisher('/mobile_base/commands/digital_output', DigitalOutput)
        #self.digital_out = DigitalOutput()
        #self.digital_out.values = [False, False, False, False]
        #self.digital_out.mask = [True, True, True, True] 

	# Subscribe to arm joint_states
        #rospy.Subscriber('/joint_states', JointState, self.stateCb)

	# publish command message to joints/servos of arm
    	self.joint4 = rospy.Publisher('/arm_wrist_flex_joint/command',Float64)  #4
    	self.joint1 = rospy.Publisher('/arm_shoulder_pan_joint/command',Float64)  #1
	self.joint2 = rospy.Publisher('/arm_shoulder_lift_joint/command',Float64)  #2
    	self.joint3 = rospy.Publisher('/arm_elbow_flex_joint/command',Float64)  #3
	self.joint5 = rospy.Publisher('/gripper_joint/command',Float64)
	self.pos1 = Float64()
    	self.pos2 = Float64()
    	self.pos3 = Float64()
    	self.pos4 = Float64()
    	self.pos5 = Float64()

    	#subscribe to the robot sensor state
    	rospy.Subscriber('/blobs', Blobs, self.callback)
    	self.message = Twist()

	# publish twist messages to mobile base velocity
    	self.pub = rospy.Publisher('/mobile_base/commands/velocity', Twist)
          
        self.voice = rospy.get_param("~voice", "voice_don_diphone")
        self.wavepath = rospy.get_param("~wavepath", "")
        
        # Create the sound client object
        self.soundhandle = SoundClient()
        rospy.sleep(1)
        self.soundhandle.stopAll()

        # Subscribe to the recognizer output
        rospy.Subscriber('/recognizer/output', String, self.identify)

	# Publisher to manually control the robot
        #self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist)

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
            
        self.soundhandle.say("Where to find blue object", self.voice)

	# Arm in "home" position
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
	rospy.sleep(3)

	locations = dict()

	#quaternion = quaternion_from_euler(0.0, 0.0, 90.0)
	#locations['A'] = Pose(Point(0.4, 1.1, 0.000), Quaternion(quaternion[0], quaternion[1], quaternion[2], quaternion[3]))

	#quaternion = quaternion_from_euler(0.0, 0.0, 180.0)
	#locations['B'] = Pose(Point(2.8, 3.5, 0.000), Quaternion(quaternion[0], quaternion[1], quaternion[2], quaternion[3]))

	#quaternion = quaternion_from_euler(0.0, 0.0, -90.0)
	#locations['C'] = Pose(Point(4.0, -2.5, 0.000), Quaternion(quaternion[0], quaternion[1], quaternion[2], quaternion[3]))

	#quaternion = quaternion_from_euler(0.0, 0.0, 0.0)
	#locations['D'] = Pose(Point(0.0, -3.7, 0.000), Quaternion(quaternion[0], quaternion[1], quaternion[2], quaternion[3]))

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

	  if hand == 1:
		self.pos1 = 1.559
		self.pos2 = 0.215
		self.pos3 = -1.508
		self.pos4 = -0.496
		self.pos5 = 0.0
		self.joint1.publish(self.pos1)
		self.joint2.publish(self.pos2)
		self.joint3.publish(self.pos3)
		self.joint4.publish(self.pos4)
		self.joint5.publish(self.pos5)
		rospy.sleep(1.5)

		self.pos1 = 1.565
		self.pos2 = -2.393
		self.pos3 = -0.639
		self.pos4 = 1.335
		self.pos5 = -0.430
		self.joint1.publish(self.pos1)
		self.joint2.publish(self.pos2)
		self.joint3.publish(self.pos3)
		self.joint4.publish(self.pos4)
		self.joint5.publish(self.pos5)
		rospy.sleep(2.5)

		global start
		global hand
		start = 3
		hand = 0

	  if hand == 2:
		self.pos1 = 1.539
		self.pos2 = -2.398
		self.pos3 = -0.297
		self.pos4 = 0.982
		self.joint1.publish(self.pos1)
		self.joint2.publish(self.pos2)
		self.joint3.publish(self.pos3)
		self.joint4.publish(self.pos4)
		rospy.sleep(2)

		self.pos5 = 0.325
		self.joint5.publish(self.pos5)
		rospy.sleep(1)

		self.pos1 = 1.585
		self.pos2 = 0.982
		self.pos3 = -2.429
		self.joint1.publish(self.pos1)
		self.joint2.publish(self.pos2)
		self.joint3.publish(self.pos3)
		self.joint5.publish(self.pos5)
		rospy.sleep(2)

		self.pos4 = -0.1585
		self.joint4.publish(self.pos4)
		rospy.sleep(1)

		global hand
		global start
		hand = 0
		start = 4

	  if start == 1:
		if message == "point A":
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
		  self.soundhandle.say("Going to Japan", self.voice)
		  rospy.sleep(2)
		  self.goal.target_pose.pose = locations['D']
		  self.move_base.send_goal(self.goal)
		  waiting = self.move_base.wait_for_result(rospy.Duration(300))
		  if waiting == 1:
		    self.soundhandle.say("Reached Japan", self.voice)
		    rospy.sleep(2)
		    self.soundhandle.say("Finding blue object", self.voice)
		    rospy.sleep(2)
		    global start
		    start = 2

		if message == "origin":
		  self.soundhandle.say("Going back home", self.voice)
		  rospy.sleep(2)
		  self.goal.target_pose.pose = self.origin
		  self.move_base.send_goal(self.goal)
		  waiting = self.move_base.wait_for_result(rospy.Duration(300))
		  if waiting == 1:
		    #self.soundhandle.say("Reached Malaysia", self.voice)
		    #rospy.sleep(2)
		    if again == 3:
		    	self.soundhandle.say("Here is your blue object", self.voice)
		    	rospy.sleep(2)
		    	global start
		    	start = 10
		    else :
		    	self.soundhandle.say("Home sweet home", self.voice)
		    	rospy.sleep(2)
		    	global start
		    	start = 0

		#self.move_base.wait_for_result(rospy.Duration(5))
		#rospy.Rate(2).sleep()

	  if start == 2:
		self.message.linear.x = 0.0; self.message.linear.y = 0; self.message.linear.z = 0
		self.message.angular.x = 0.0; self.message.angular.y = 0; self.message.angular.z = turn
                self.pub.publish(self.message)
		rospy.sleep(0.3)
		self.message.linear.x = 0.0; self.message.linear.y = 0; self.message.linear.z = 0
		self.message.angular.x = 0.0; self.message.angular.y = 0; self.message.angular.z = 0
                self.pub.publish(self.message)
		rospy.sleep(2.5)

	  if start == 3:
              	if bumper == 0 or bumper == 1 or bumper == 2:
		    if bumper_state == 1:
			  rospy.loginfo("bumper hit!")
			  self.led1.value = 3
			  global start
			  global hand
		    	  self.message.linear.x = 0.0; self.message.linear.y = 0; self.message.linear.z = 0
		    	  self.message.angular.x = 0.0; self.message.angular.y = 0; self.message.angular.z = 0
                          self.pub.publish(self.message)
                          #self.cmd_vel_pub.publish(self.message)
                          rospy.sleep(1)
                          #self.digital_out.values = [True, True, True, True]
                          #self.digital_out.mask = [True, True, True, True]
                          #self.pub3.publish(self.digital_out)
                          start = 10
			  hand = 2

		if start != 10:
              	    self.message.linear.x = 0.05; self.message.linear.y = 0; self.message.linear.z = 0
              	    self.message.angular.x = 0.0; self.message.angular.y = 0; self.message.angular.z = 0
              	    self.pub.publish(self.message)

		#rospy.Rate(5).sleep()
                          
          if start == 4:
              	self.message.linear.x = -0.4; self.message.linear.y = 0; self.message.linear.z = 0
              	self.message.angular.x = 0.0; self.message.angular.y = 0; self.message.angular.z = 0
              	self.pub.publish(self.message)
                #self.cmd_vel_pub.publish(self.message)
		rospy.sleep(2)
              	self.message.linear.x = 0.0; self.message.linear.y = 0; self.message.linear.z = 0
              	self.message.angular.x = 0.0; self.message.angular.y = 0; self.message.angular.z = 0
              	self.pub.publish(self.message)
                #self.cmd_vel_pub.publish.publish(self.message)

          	global message
                message = "origin"
		rospy.sleep(1)
                global start
                start = 1

	  # send the message and delay
          self.pub1.publish(self.led1)
          self.pub2.publish(self.led2)
          rospy.Rate(50).sleep()

    def update_initial_pose(self, initial_pose):
        self.initial_pose = initial_pose
	if original == 0:
		self.origin = self.initial_pose.pose.pose
		global original
		original = 1

    def identify(self, msg):
        # Print the recognized words on the screen
	if start == 0:
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
	  elif msg.data == 'go to japan' or msg.data == 'japan':
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
        # Speak the recognized words in the selected voice
        #self.soundhandle.say(msg.data, self.voice)

    def callback(self, data):
        if(len(data.blobs)):
	    global turn
	    #global straight
	    global blob_position_x
	    #global blob_position_y

	    blob_position_x = 0
	    #blob_position_y = 0
	    for obj in data.blobs:
	      blob_position_x = blob_position_x + obj.x
	      #blob_position_y = blob_position_y + obj.y
	    blob_position_x = blob_position_x/len(data.blobs)
	    #blob_position_y = blob_position_y/len(data.blobs)

	    #rospy.loginfo("blob is at x: %s"%blob_position_x)
	    #rospy.loginfo("blob is at y: %s"%blob_position_y)
	    #rospy.loginfo(len(data.blobs))
	    # turn right if we set off the left cliff sensor
	    if( blob_position_x > 320 ):
		if again == 0:
	        	turn = -0.30
		elif again == 1:
			turn = -0.20
	    # turn left if we set off the right cliff sensor
	    elif( blob_position_x < 307 ):
		if again == 0:
	        	turn = 0.30
		elif again == 1:
			turn = 0.20

	    elif( blob_position_x >= 307 and blob_position_x <= 320):
		if count == 0:
			global again
			again = again + 1

		if again == 1:
			turn = 0.0
			rospy.sleep(1)
		elif again == 2:
			turn = 0.0
			while start != 2:
				rospy.sleep(0.5)
		    	self.soundhandle.say("Found blue object", self.voice)
		   	rospy.sleep(2)
		    	self.soundhandle.say("Try to get blue object", self.voice)
		   	rospy.sleep(2)
			global again
			again = again + 1
			global count
			count = 1
                	global hand
			hand = 1
			global start
			start = 10

                #self.digital_out.values = [True, True, True, True]
                #self.digital_out.mask = [True, True, True, True]
                #self.pub3.publish(self.digital_out)
		#rospy.sleep(1)
                #self.digital_out.values = [False, False, False, False]
                #self.digital_out.mask = [True, True, True, True]
                #self.pub3.publish(self.digital_out)
                #start = 3


	    #if( blob_position_y > 420 ):
	    #    straight = -0.05

	    #elif( blob_position_y < 390 ):
	    #    straight = 0.05

	    #elif( blob_position_y > 390 and blob_position_y < 420):
	    #    straight = 0.0

        else:
	    turn = 0.0

    def BumperEventCallback(self,data2):
	global bumper
	global bumper_state
	bumper = data2.bumper
	bumper_state = data2.state

    #def stateCb(self, msg):        
	#global name
	#global position

    def cleanup(self):
        rospy.loginfo("Shutting down demo....")
	self.move_base.cancel_goal()
        #self.cmd_vel_pub.publish(Twist())
	self.pub.publish(Twist())

if __name__=="__main__":
    rospy.init_node('demo')
    try:
        Demo()
        #rospy.spin()
    except rospy.ROSInterruptException:
        pass

