#!/usr/bin/env python

"""
     color_tracker.py - follow the color desired

"""

import roslib; roslib.load_manifest('cmvision')
import rospy
from cmvision.msg import Blobs

blob_position_x = 0

class Color_Tracker:
    def __init__(self):
        rospy.on_shutdown(self.cleanup)

    	#subscribe to the robot sensor state
    	rospy.Subscriber('/blobs', Blobs, self.callback)

    	while not rospy.is_shutdown():
	    rospy.loginfo("blob is at x: %s"%blob_position_x)

    def callback(self, data):
        if(len(data.blobs)):
	    global blob_position_x

	    blob_position_x = 0

	    for obj in data.blobs:
	      blob_position_x = blob_position_x + obj.x

	    blob_position_x = blob_position_x/len(data.blobs)

    def cleanup(self):
        rospy.loginfo("Shutting down color tracking...")

if __name__=="__main__":
    rospy.init_node('color_tracker')
    try:
        Color_Tracker()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

