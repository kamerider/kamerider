#!/usr/bin/env python

import roslib; roslib.load_manifest('kobuki_testsuite'); roslib.load_manifest('pi_speech_tutorial'); roslib.load_manifest('turtlebot_follower')
import rospy

from std_msgs.msg import String
from sound_play.libsoundplay import SoundClient
from kobuki_msgs.msg import DigitalInputEvent
from turtlebot_msgs.srv import *

digitalS = [True, True, True, True]
def DigitalInputEventCallback(data):
  global digitalS
  digitalS = data.values

listenS=""
def MicInputEventCallback(msg):
  global listenS
  listenS = msg.data

class MainLoop:
  def __init__(self):
    self.voice = rospy.get_param("~voice", "voice_don_diphone")
    self.soundhandle = SoundClient()
    rospy.sleep(1)
    self.soundhandle.stopAll()
#    rospy.sleep(1)
    self.soundhandle.say("Ready", self.voice)
    rospy.sleep(1)

    # Create sound client
    self.words=SoundClient()
    # Subscribe to the /recognizer/output topic to receive voice commands
    rospy.Subscriber('/recognizer/output', String, MicInputEventCallback)
    # Subscribe to the /mobile_base/events/digital_input topic to receive DIO 
    rospy.Subscriber('/mobile_base/events/digital_input', DigitalInputEvent, DigitalInputEventCallback)
    rospy.sleep(1)

  def talk(self, words):
    self.soundhandle.say(words, self.voice)
    rospy.sleep(1)

if __name__ == '__main__':
  rospy.init_node('follow_me2')
  test=MainLoop()
  count=1
  try:
    while not rospy.is_shutdown():
      while digitalS[2]==True:
        if listenS=='go':
             break;
        pass
      while digitalS[3]==False:
        if digitalS[2]==False:
          if count==1:
            count=0
            test.talk("button two is pressed")
            rospy.wait_for_service('change_state')
            try:
              setfollowstate = rospy.ServiceProxy('change_state', SetFollowState)
              response = setfollowstate("state: 1")
            except rospy.ServiceException, e:
              print "Service call failed: %s"%e
          else:
            pass
        elif digitalS[1]==False:
          if count==0:
            count=1
            test.talk("stop follow")
            rospy.wait_for_service('change_state')
            try:
              setfollowstate = rospy.ServiceProxy('change_state', SetFollowState)
              response = setfollowstate("state: 0")
              print response
            except rospy.ServiceException, e:
              print "Service call fail"
          else:
            pass
  except:
    pass
