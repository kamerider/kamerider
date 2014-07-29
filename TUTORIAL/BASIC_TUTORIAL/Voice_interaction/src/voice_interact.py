#!/usr/bin/env python

"""
    voice_interact.py - robot will reply what the user said

"""

import roslib; roslib.load_manifest('pi_speech_tutorial')
import rospy
from std_msgs.msg import String
from sound_play.libsoundplay import SoundClient

class Voice_Interact:
    def __init__(self):
        rospy.on_shutdown(self.cleanup)

        self.rate = rospy.get_param("~rate", 5)
        r = rospy.Rate(self.rate)
          
        self.voice = rospy.get_param("~voice", "voice_don_diphone")
        self.wavepath = rospy.get_param("~wavepath", "")
        
        # Create the sound client object
        self.soundhandle = SoundClient()
        
        rospy.sleep(1)
        self.soundhandle.stopAll()
        
        # Announce that we are ready for input
        self.soundhandle.playWave(self.wavepath + "/R2D2a.wav")
        rospy.sleep(1)
        self.soundhandle.say("Ready", self.voice)

        # Subscribe to the recognizer output
        rospy.Subscriber('/recognizer/output', String, self.identify)


	while not rospy.is_shutdown():
    		r.sleep()                       



    def identify(self, msg):

    	if msg.data == 'hello':
        	rospy.loginfo(msg.data)
        	self.soundhandle.say("hello", self.voice)
        	rospy.sleep(1)

    	elif msg.data == 'how are you'
        	rospy.loginfo(msg.data)
        	self.soundhandle.say("I am fine", self.voice)
        	rospy.sleep(1)

    	elif msg.data == 'who are you'
        	rospy.loginfo(msg.data)
        	self.soundhandle.say("I am turtle", self.voice)
        	rospy.sleep(1)


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

