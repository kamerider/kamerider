#!/usr/bin/env python

import roslib; roslib.load_manifest('kobuki_testsuite'); roslib.load_manifest('pi_speech_tutorial')
import rospy
import curses, sys, traceback

from std_msgs.msg import String
from sound_play.libsoundplay import SoundClient
from kobuki_msgs.msg import DigitalInputEvent

digitalS = [True, True, True, True]
def DigitalInputEventCallback(data):
  global digitalS
  digitalS = data.values

listenS = ""
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

    # Subscribe to the /recognizer/output topic to receive voice commands.  
    rospy.Subscriber('/recognizer/output', String, MicInputEventCallback)
    # Subscribe to the /mobile_base/events/digital_input topic to receive DIO
    rospy.Subscriber('/mobile_base/events/digital_input', DigitalInputEvent, DigitalInputEventCallback)
    rospy.sleep(1)
    
  def talk(self, words):
    self.soundhandle.say(words, self.voice)
    rospy.sleep(1)

if __name__ == '__main__':
  rospy.init_node('140429_02')
  test=MainLoop()
  count=0
  try:
    while not rospy.is_shutdown():
      while digitalS[2]==True:
        pass
      while digitalS[3]==False:
        if digitalS[1]==False:
          if count==0:
            test.talk("program start")
            count=1
        elif digitalS[2]==False:
          if count==1:
            test.talk("button two is pressed")
            count=0
  except:
    pass
