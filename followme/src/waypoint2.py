#!/usr/bin/env python

import actionlib
import roslib; roslib.load_manifest('kobuki_testsuite'); roslib.load_manifest('pi_speech_tutorial')
import rospy
import curses, sys, traceback

from std_msgs.msg import String
from sound_play.libsoundplay import SoundClient
from kobuki_msgs.msg import DigitalInputEvent
from geometry_msgs.msg import PoseStamped


def talker():
    pub = rospy.Publisher('/move_base_simple/goal', PoseStamped)
    rospy.init_node('talker', anonymous=True)
    str='{{,},{{0.0,0.0,0.0},{0.0,0.0,0.0,1.0}}}'
    rospy.loginfo(str)
    pub.publish(str)

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException: pass
