#!/usr/bin/env python

#import actionlib
import roslib; roslib.load_manifest('kobuki_testsuite'); roslib.load_manifest('pi_speech_tutorial')
import rospy
#import curses, sys, traceback

#from actionlib_msgs.msg import *
from std_msgs.msg import String
from sound_play.libsoundplay import SoundClient
from kobuki_msgs.msg import DigitalInputEvent
from geometry_msgs.msg import *
from move_base_msgs.msg import MoveBaseAction

digitalS = [True, True, True, True]
def DigitalInputEventCallback(data):
  global digitalS
  digitalS = data.values

listenS=""
def MicInputEventCallback(msg):
  global listenS
  listenS = msg.data

#def MoveToPoint(x,y,w):
#  rospy.loginfo('ok4')
#  sac=actionlib.SimpleActionClient("move_base", MoveBaseAction)
#  rospy.loginfo('ok4')
#  sac=wait_for_server(rospy.Duration(60))
#  rospy.loginfo('ok4')
#  goal=MoveBaseGoal()
#  rospy.loginfo('ok4')
#  goal.target_pose.pose.position.x=x
#  goal.target_pose.pose.position.y=y
#  goal.target_pose.orientation.w=w
#  goal.target_pose.header.frame_id='map'
#  goal.target_pose.header.stamp=rospy.Time.now()
#  rospy.loginfo('ok4')
#  move_base.send_goal(goal)
#  sac.wait_for_server()
#  rospy.loginfo('ok4')
#  sac.send_goal(goal)
#  rospy.loginfo('ok4')
#  sac.wait_for_result()
#  rospy.loginfo('ok4')
#  print sac.get_result()

class MainLoop:
  def __init__(self):
    self.voice = rospy.get_param("~voice", "voice_don_diphone")
    self.soundhandle = SoundClient()
    rospy.sleep(1)
    self.soundhandle.stopAll()
    rospy.sleep(1)
    
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
  pub=rospy.Publisher('move_base_simple/goal', PoseStamped)
  rospy.init_node('MainLoop')
  rospy.loginfo('ok1')
#  pub=rospy.Publisher('move_base_simple/goal', MoveBaseGoal)
  rospy.loginfo('ok2')
  test=MainLoop()
  count=01

  try:
    while not rospy.is_shutdown():
      while digitalS[2]==True:
        pass

      while digitalS[3]==False:
        if digitalS[2]==False:
          if count==0:
            test.talk("button two is pressed")
            rospy.loginfo('ok3')
            move=PoseStamped()
            rospy.loginfo('ok4')
            pub.publish(move)
            rospy.loginfo('ok5')
            count=1
        elif digitalS[1]==False:
          if count==1:
            test.talk("reset")
            rospy.loginfo('ok6')
            count=0
  except:
    pass
