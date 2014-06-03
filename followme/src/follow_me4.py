#!/usr/bin/env python

import roslib; roslib.load_manifest('kobuki_testsuite'); roslib.load_manifest('pi_speech_tutorial'); roslib.load_manifest('turtlebot_follower')
import rospy
import sys

from std_msgs.msg import String
from sound_play.libsoundplay import SoundClient
from kobuki_msgs.msg import DigitalInputEvent
from geometry_msgs.msg import Twist
from turtlebot_msgs.srv import *

digitalS = [True, True, True, True]
def DigitalInputEventCallback(data):
  global digitalS
  digitalS = data.values

listenS=""
def MicInputEventCallback(msg):
  global listenS
  listenS = msg.data

def RobotReverse(distance):
  while not distance==0:
    rospy.loginfo("okInverse")
    twist.linear.x=-0.5
    pub.publish(twist)
    rospy.sleep(1)
    distance-=1

def FollowStartStop(x):
  rospy.wait_for_service('/turtlebot_follower/change_state')
  try:
    change_state = rospy.ServiceProxy('/turtlebot_follower/change_state', SetFollowState)
    response=change_state(x)
  except rospy.ServiceException, e:
    pass

class MainLoop:
  def __init__(self):
    self.voice = rospy.get_param("~voice", "voice_don_diphone")
    self.soundhandle = SoundClient()
    rospy.sleep(1)
    self.soundhandle.stopAll()
    rospy.sleep(1)
    self.soundhandle.say("Ready", self.voice)
    rospy.sleep(1)
    pub = rospy.Publisher('cmd_vel', Twist)
    rospy.sleep(1)
    # Create sound client
    self.words=SoundClient()
    # Subscribe to the /recognizer/output topic to receive voice commands.  
    rospy.Subscriber('/recognizer/output', String, MicInputEventCallback)
    # Subscribe to the /mobile_base/events/digital_input topic to receive DIO
    rospy.Subscriber('/mobile_base/events/digital_input', DigitalInputEvent, DigitalInputEventCallback)
    rospy.sleep(1)
    
    twist=Twist()
    pub=rospy.Publisher('cmd_vel',Twist)
    
  def talk(self, words):
    self.soundhandle.say(words, self.voice)
    rospy.sleep(1)

if __name__ == '__main__':
  rospy.init_node('MainLoop')
  test=MainLoop()
  count=0
  follow=0
  stop_listen_time=5
  wait_time=10
#  rospy.loginfo("ok")
  try:
    while not rospy.is_shutdown():
      FollowStartStop(0)
#      rospy.loginfo("ok1")
      while digitalS[2]==True:
#        rospy.loginfo("ok2")
        pass
      test.talk("i am ready")
      rospy.sleep(3)
      while digitalS[3]==False:
# Debug
        if listenS=="move":
#        if digitalS[2]==False:
# Debug   if count==0:
#          count=1
          test.talk("please stand one meter away in front of me")
          rospy.sleep(4)
          test.talk("start recognizing")
          rospy.sleep(3)
          test.talk("start follow")
          rospy.sleep(1)
          follow=1
#        elif digitalS[1]==True:
#          FollowStartStop(0)
#          rospy.loginfo("STOPFollow")
#          count=0
#        else:
#          pass

        if follow==1:
#          test.talk("please stand one meter away in front of me")
#          rospy.sleep(4)
#          test.talk("start recognizing")
#          rospy.sleep(3)
#          test.talk("start follow")
#          rospy.sleep(1)
          FollowStartStop(1)

# Debug
          if listenS=="wait":
#            if digitalS[1]==False:
# Debug
            test.talk("ok")
            rospy.sleep(1)
            test.talk("please walk to me")
            rospy.sleep(3)
            follow=2
            FollowStartStop(0)
 #         else:
 #           pass
        elif follow==2:
          rospy.sleep(wait_time)
          FollowStartStop(1)
  except:
    pass
