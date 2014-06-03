#!/usr/bin/env python
import roslib
import rospy

from geometry_msgs.msg import Twist

def mover():
    pub = rospy.Publisher('cmd_vel', Twist)
    rospy.init_node('robot_mover')

    twist = Twist()
    twist.linear.x = 0.1; # move forward at 0.1 m/s   

    rospy.loginfo("Moving the robot forward.")
    pub.publish(twist)
    rospy.sleep(1)

    rospy.loginfo("Moving the robot backward.")
    twist.linear.x = -0.1; # move backward at 0.1 m/s
    pub.publish(twist)
    rospy.sleep(1);

    rospy.loginfo("Turning the robot left.");
    twist = Twist();
    twist.angular.z = 0.5
    pub.publish(twist)
    rospy.sleep(1);
    
    rospy.loginfo("Turning the robot right.");
    twist.angular.z = -0.5
    pub.publish(twist)
    rospy.sleep(1);

    rospy.loginfo("Stopping!")
    twist = Twist()
    pub.publish(twist)

    rospy.loginfo("Node exiting.");

if __name__ == '__main__':
    try:
        mover()
    except rospy.ROSInterruptException: pass
