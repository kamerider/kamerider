#!/usr/bin/env python

"""
    voice_interact_2.py - robot will reconfirm before executing voice navigation command

"""

import roslib; roslib.load_manifest('pi_speech_tutorial')
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from math import copysign

from sound_play.libsoundplay import SoundClient
confirming = 0
recognise = 1
memory = 'None'

class Voice_Interact:
    def __init__(self):
        rospy.on_shutdown(self.cleanup)

        self.max_speed = rospy.get_param("~max_speed", 0.35)
        self.max_angular_speed = rospy.get_param("~max_angular_speed", 1.5)
        self.speed = rospy.get_param("~start_speed", 0.1)
        self.angular_speed = rospy.get_param("~start_angular_speed", 0.5)
        self.linear_increment = rospy.get_param("~linear_increment", 0.05)
        self.angular_increment = rospy.get_param("~angular_increment", 0.25)
        self.rate = rospy.get_param("~rate", 3)
        r = rospy.Rate(self.rate)
        self.paused = False
          
        self.voice = rospy.get_param("~voice", "voice_don_diphone")
        self.wavepath = rospy.get_param("~wavepath", "")
        
        # Create the sound client object
        self.soundhandle = SoundClient()
        
        rospy.sleep(1)
        self.soundhandle.stopAll()
        
        # Initialize the Twist message we will publish.
        self.msg = Twist()

        # Publish the Twist message to the cmd_vel topic
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel_mux/input/teleop', Twist)
        
        # Announce that we are ready for input
        self.soundhandle.playWave(self.wavepath + "/R2D2a.wav")
        rospy.sleep(1)
        self.soundhandle.say("Ready", self.voice)
        
        rospy.loginfo("Say one of the navigation commands...")

        # Subscribe to the recognizer output
        rospy.Subscriber('/recognizer/output', String, self.reply)

	# A mapping from keywords to commands.
	# Grouping similar commands to a general command
        self.keywords_to_command = {'stop': ['stop', 'halt', 'abort', 'kill', 'panic', 'off', 'freeze', 'shut down', 'turn off', 'help', 'help me','cancel','please stop moving'],
                                    'go slower': ['slow down', 'slower'],
                                    'go faster': ['speed up', 'faster'],
                                    'go ahead': ['forward', 'ahead', 'straight','move forward','start'],
                                    'go backward': ['back', 'backward', 'back up','move backward','reverse'],
                                    'rotate left': ['rotate left'],
                                    'rotate right': ['rotate right'],
                                    'turn left': ['turn left','go left','move left','left','turn to the left'],
                                    'turn right': ['turn right','go right','move right','right','turn to the right'],
                                    'quarter': ['quarter speed'],
                                    'half': ['half speed'],
                                    'full': ['full speed'],
                                    'pause': ['pause speech'],
                                    'continue': ['continue speech'],
					'yes':['yes','confirm', 'positive'],
					'no':['no','negative'],
					'robot':['robot']}
	while not rospy.is_shutdown():
    		self.cmd_vel_pub.publish(self.msg)
    		r.sleep()                       

    # algorithm to find the general command
    def get_command(self, data):
        for (command, keywords) in self.keywords_to_command.iteritems():
            for word in keywords:
                if data.find(word) > -1:
                    return command
        
    def reply(self, msg):
	command = self.get_command(msg.data)

        # Print the recognized words on the screen
	rospy.loginfo("Command: " + str(command))
        
        # Speak the recognized words in the selected voice
	if recognise == 1:
		if str(command) != 'None':
			if str(command) == 'robot':
				self.soundhandle.say("yes, may I help you", self.voice)
				global recognise
				recognise = 0
	elif confirming == 0:
		if str(command) != 'None':
			self.soundhandle.say("are you asking me to" + str(command), self.voice)
			global memory
			memory = str(command)
			global confirming
	    		confirming = 1
	elif confirming == 1:
	  	if str(command) == 'yes':
	    		self.soundhandle.say("roger that", self.voice)
			if memory == 'pause':
				self.paused = True
			elif memory == 'continue':
			    	self.paused = False
			if self.paused:
			    	return   
			if memory == 'go ahead':    
			    	self.msg.linear.x = self.speed
			    	self.msg.angular.z = 0
			elif memory == 'rotate left':
			    	self.msg.linear.x = 0
			    	self.msg.angular.z = self.angular_speed
			elif memory == 'rotate right':  
			    	self.msg.linear.x = 0      
			    	self.msg.angular.z = -self.angular_speed
			elif memory == 'turn left':
			    	if self.msg.linear.x != 0:
					self.msg.angular.z += self.angular_increment
			    	else:        
					self.msg.angular.z = self.angular_speed
			elif memory == 'turn right':    
			    	if self.msg.linear.x != 0:
					self.msg.angular.z -= self.angular_increment
			    	else:        
					self.msg.angular.z = -self.angular_speed
			elif memory == 'go backward':
			    	self.msg.linear.x = -self.speed
			    	self.msg.angular.z = 0
			elif memory == 'stop': 
			    	# Stop the robot!  Publish a Twist message consisting of all zeros.         
			    	self.msg = Twist()
			elif memory == 'go faster':
			    self.speed += self.linear_increment
			    self.angular_speed += self.angular_increment
			    if self.msg.linear.x != 0:
				self.msg.linear.x += copysign(self.linear_increment, self.msg.linear.x)
			    if self.msg.angular.z != 0:
				self.msg.angular.z += copysign(self.angular_increment, self.msg.angular.z)
			    
			elif memory == 'go slower':
			    self.speed -= self.linear_increment
			    self.angular_speed -= self.angular_increment
			    if self.msg.linear.x != 0:
				self.msg.linear.x -= copysign(self.linear_increment, self.msg.linear.x)
			    if self.msg.angular.z != 0:
				self.msg.angular.z -= copysign(self.angular_increment, self.msg.angular.z)
				
			elif memory in ['quarter', 'half', 'full']:
			    if memory == 'quarter':
				self.speed = copysign(self.max_speed / 4, self.speed)
		
			    elif memory == 'half':
				self.speed = copysign(self.max_speed / 2, self.speed)
			    
			    elif memory == 'full':
				self.speed = copysign(self.max_speed, self.speed)
			    
			    if self.msg.linear.x != 0:
				self.msg.linear.x = copysign(self.speed, self.msg.linear.x)

			    if self.msg.angular.z != 0:
				self.msg.angular.z = copysign(self.angular_speed, self.msg.angular.z)
				
			else:
			    return
			self.msg.linear.x = min(self.max_speed, max(-self.max_speed, self.msg.linear.x))
			self.msg.angular.z = min(self.max_angular_speed, max(-self.max_angular_speed, self.msg.angular.z))
			self.cmd_vel_pub.publish(self.msg)
			global confirming
			confirming = 0

	  	elif str(command) == 'no':
	    		self.soundhandle.say("please give command again", self.voice)
			global memory
			memory = 'None'
			global confirming
	    		confirming = 0

    def cleanup(self):
        rospy.loginfo("Shutting down voice interaction...")
        twist = Twist()
        self.cmd_vel_pub.publish(twist)

if __name__=="__main__":
    rospy.init_node('voice_interact')
    try:
        Voice_Interact()
        rospy.spin()
    except:
        pass

