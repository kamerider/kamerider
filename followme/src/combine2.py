#!/usr/bin/env python

import roslib
import rospy; roslib.load_manifest('kobuki_testsuite'); roslib.load_manifest('pi_speech_tutorial')
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped, Point, Quaternion, Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from math import pow, sqrt
from std_msgs.msg import String
from sound_play.libsoundplay import SoundClient
from kobuki_msgs.msg import DigitalInputEvent

digitalS = [True, True, True, True]
def DigitalInputEventCallback(data):
  global digitalS
  digitalS = data.values

listenS=""
def MicInputEventCallback(msg):
  global listenS
  listenS = msg.data

class NavTest():
    def __init__(self):
#        self.voice = rospy.get_param("~voice", "voice_don_diphone")
#        self.soundhandle = SoundClient()
#        rospy.sleep(1)
#        self.soundhandle.stopAll()
#        rospy.sleep(1)
#        self.soundhandle.say("Ready", self.voice)
#        rospy.sleep(1)
#
#        # Create sound client
#        self.words=SoundClient()
#        # Subscribe to the /recognizer/output topic to receive voice commands
#        rospy.Subscriber('/recognizer/output', String, MicInputEventCallback)
#        # Subscribe to the /mobile_base/events/digital_input topic to receive DIO
#        rospy.Subscriber('/mobile_base/events/digital_input', DigitalInputEvent, DigitalInputEventCal#lback)
#
        rospy.init_node('main_loop', anonymous=True)
        rospy.on_shutdown(self.shutdown)

        self.voice = rospy.get_param("~voice", "voice_don_diphone")
        self.soundhandle = SoundClient()
        rospy.sleep(1)
        self.soundhandle.stopAll()
        rospy.sleep(1)
        self.soundhandle.say("Ready", self.voice)
        rospy.sleep(1)

        # Create sound client
        self.words=SoundClient()
        # Subscribe to the /recognizer/output topic to receive voice commands
        rospy.Subscriber('/recognizer/output', String, MicInputEventCallback)
        # Subscribe to the /mobile_base/events/digital_input topic to receive DIO 
        rospy.Subscriber('/mobile_base/events/digital_input', DigitalInputEvent, DigitalInputEventCallback)
        
        # How long in seconds should the robot pause at each location?
        self.rest_time = rospy.get_param("~rest_time", 10)        
        # Are we running in the fake simulator?
        self.fake_test = rospy.get_param("~fake_test", False)
        # Goal state return values
        goal_states = ['PENDING', 'ACTIVE', 'PREEMPTED', 
                       'SUCCEEDED', 'ABORTED', 'REJECTED',
                       'PREEMPTING', 'RECALLING', 'RECALLED',
                       'LOST']
        
        # Set up the goal locations. Poses are defined in the map frame.  
        # An easy way to find the pose coordinates is to point-and-click
        # Nav Goals in RViz when running in the simulator.
        # Pose coordinates are then displayed in the terminal
        # that was used to launch RViz.
#        locations = dict()
#        
#        locations['hall_1'] = Pose(Point(0.0, 0.5, 0.000), Quaternion(0.000, 0.000, 0.223, 1.000))
#        locations['hall_2'] = Pose(Point(0.0, -0.5, 0.000), Quaternion(0.000, 0.000, -0.670, 0.743))
        #locations['hall_bedroom'] = Pose(Point(-3.719, 4.401, 0.000), Quaternion(0.000, 0.000, 0.733, 0.680))
        #locations['living_room_1'] = Pose(Point(0.720, 2.229, 0.000), Quaternion(0.000, 0.000, 0.786, 0.618))
        #locations['living_room_2'] = Pose(Point(1.471, 1.007, 0.000), Quaternion(0.000, 0.000, 0.480, 0.877))
        #locations['dining_room_1'] = Pose(Point(-0.861, -0.019, 0.000), Quaternion(0.000, 0.000, 0.892, -0.451))
        
        # Publisher to manually control the robot (e.g. to stop it)
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist)
        
        # Subscribe to the move_base action server
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        
        rospy.loginfo("Waiting for move_base action server...")
        
        # Wait 60 seconds for the action server to become available
        self.move_base.wait_for_server(rospy.Duration(60))
        
        rospy.loginfo("Connected to move base server")
        
        # A variable to hold the initial pose of the robot to be set by 
        # the user in RViz
        initial_pose = PoseWithCovarianceStamped()
        
        # Variables to keep track of success rate, running time,
        # and distance traveled
#        n_locations = len(locations)
#        n_goals = 0
#        n_successes = 0
#        i = n_locations
        distance_traveled = 0
        start_time = rospy.Time.now()
        running_time = 0
        location = ""
        last_location = ""
        start=0
        
        # Get the initial pose from the user
        rospy.loginfo("*** Click the 2D Pose Estimate button in RViz to set the robot's initial pose...")
        rospy.wait_for_message('initialpose', PoseWithCovarianceStamped)
        self.last_location = Pose()
        rospy.Subscriber('initialpose', PoseWithCovarianceStamped, self.update_initial_pose)
        
        # Make sure we have the initial pose
        while initial_pose.header.stamp == "":
            rospy.sleep(1)
            
        rospy.loginfo("Starting navigation test")
        self.talk("ready")
        
        state=0
        # Begin the main loop and run through a sequence of locations
        while not rospy.is_shutdown():
            while digitalS[2]==True:
                pass
            while digitalS[3]==False:
                if digitalS[2]==False:
                    if state==0:
                        self.soundhandle.say("navigation to point one", self.voice)
                        i=0
                        state+=1
                        start=1
                elif digitalS[1]==False:
                    if state==1:
                        self.soundhandle.say("to point two", self.voice)
                        i=1
                        state+=1
                elif digitalS[0]==False:
                    if state==2:
                        self.soundhandle.say("back to point one", self.voice)
                        i=0
                        state+=1
                
                if start==1:
 
                  locations = dict()
                  n_locations = len(locations)
                  locations['hall_1'] = Pose(Point(0.0, 0.5, 0.000), Quaternion(0.000, 0.000, 0.223, 1.000))
                  locations['hall_2'] = Pose(Point(0.0, -0.5, 0.000), Quaternion(0.000, 0.000, -0.670,0.743))
                  n_goals = 0
                  n_successes = 0
                  i = n_locations

#            # If we've gone through the current sequence
#            # start with a new random sequence
#            if i == n_locations:
#                i = 0
#                sequence = sample(locations, n_locations)
#                # Skip over first location if it is the same as
#                # the last location
#                if sequence[0] == last_location:
#                    i = 1
#            
#            # Get the next location in the current sequence
#            location = sequence[i]
                        
            # Keep track of the distance traveled.
            # Use updated initial pose if available.
                  if initial_pose.header.stamp == "":
                    distance = sqrt(pow(locations[location].position.x - locations[last_location].position.x, 2) + pow(locations[location].position.y - locations[last_location].position.y, 2))
                  else:
                    rospy.loginfo("Updating current pose.")
                    distance = sqrt(pow(locations[location].position.x - initial_pose.pose.pose.position.x, 2) + pow(locations[location].position.y - initial_pose.pose.pose.position.y, 2))
                    initial_pose.header.stamp = ""
                    
                  # Store the last location for distance calculations
                    last_location = location
                  
    #            # Increment the counters
    #            i += 1
    #            n_goals += 1
    #        
                  # Set up the next goal location
                    self.goal = MoveBaseGoal()
                    self.goal.target_pose.pose = locations[location]
                    self.goal.target_pose.header.frame_id = 'map'
                    self.goal.target_pose.header.stamp = rospy.Time.now()            
                  # Let the user know where the robot is going next
                    rospy.loginfo("Going to: " + str(location))                  
                  # Start the robot toward the next location
                    self.move_base.send_goal(self.goal)
                  # Allow 5 minutes to get there
                    finished_within_time = self.move_base.wait_for_result(rospy.Duration(300))
                  # Check for success or failure
                    if not finished_within_time:
                      self.move_base.cancel_goal()
                      rospy.loginfo("Timed out achieving goal")
                    else:
                      state = self.move_base.get_state()
                      if state == GoalStatus.SUCCEEDED:
                        rospy.loginfo("Goal succeeded!")
                        n_successes += 1
                        distance_traveled += distance
                        rospy.loginfo("State:" + str(state))
                      else:
                        rospy.loginfo("Goal failed with error code: " + str(goal_states[state]))
                        
                      # How long have we been running?
                        running_time = rospy.Time.now() - start_time
                        running_time = running_time.secs / 60.0
            
                      # Print a summary success/failure, distance traveled and time elapsed
                        rospy.loginfo("Success so far: " + str(n_successes) + "/" + 
                                      str(n_goals) + " = " + 
                                      str(100 * n_successes/n_goals) + "%")
                        rospy.loginfo("Running time: " + str(trunc(running_time, 1)) + 
                                      " min Distance: " + str(trunc(distance_traveled, 1)) + " m")
                        rospy.sleep(self.rest_time)
            
    def update_initial_pose(self, initial_pose):
        self.initial_pose = initial_pose

    def shutdown(self):
        rospy.loginfo("Stopping the robot...")
        self.move_base.cancel_goal()
        rospy.sleep(2)
        self.cmd_vel_pub.publish(Twist())
        rospy.sleep(1)
    def talk(self, words):
        self.soundhandle.say(words, self.voice)
        rospy.sleep(1)

#    def navi(self, location):
#      if initial_pose.header.stamp == "":
#        distance = sqrt(pow(locations[location].position.x -
#                            locations[last_location].position.x, 2) +
#                        pow(locations[location].position.y -
#                            locations[last_location].position.y, 2))
#      else:
#        rospy.loginfo("Updating current pose.")
#        distance = sqrt(pow(locations[location].position.x -
#                            initial_pose.pose.pose.position.x, 2) +
#                        pow(locations[location].position.y -
#                            initial_pose.pose.pose.position.y, 2))
#        initial_pose.header.stamp = ""
#        # Store the last location for distance calculations
#        last_location = location
#        # Increment the counters
#        #         i += 1
#        #         n_goals += 1
#        # Set up the next goal location                                                           
#        self.goal = MoveBaseGoal()
#        self.goal.target_pose.pose = locations[location]
#        self.goal.target_pose.header.frame_id = 'map'
#        self.goal.target_pose.header.stamp = rospy.Time.now()
#        # Let the user know where the robot is going next 
#        rospy.loginfo("Going to: " + str(location))
#        # Start the robot toward the next location                                                 
#        self.move_base.send_goal(self.goal)
#        # Allow 5 minutes to get there                                                            
#        finished_within_time = self.move_base.wait_for_result(rospy.Duration(300))
#        # Check for success or failure 
#        if not finished_within_time:
#          self.move_base.cancel_goal()
#          rospy.loginfo("Timed out achieving goal")
#        else:
#          state = self.move_base.get_state()
#          if state == GoalStatus.SUCCEEDED:
#            rospy.loginfo("Goal succeeded!")
#            n_successes += 1
#            distance_traveled += distance
#            rospy.loginfo("State:" + str(state))
#          else:
#            rospy.loginfo("Goal failed with error code: " + str(goal_states[state]))
#            # How long have we been running?
#            running_time = rospy.Time.now() - start_time
#            running_time = running_time.secs / 60.0
#            # Print a summary success/failure, distance traveled and time elapsed
#            rospy.loginfo("Success so far: " + str(n_successes) + "/" +
#                          str(n_goals) + " = " +
#                          str(100 * n_successes/n_goals) + "%")
#            rospy.loginfo("Running time: " + str(trunc(running_time, 1)) +
#                          " min Distance: " + str(trunc(distance_traveled, 1)) + " m")
#            rospy.sleep(self.rest_time)
      
def trunc(f, n):
    # Truncates/pads a float f to n decimal places without rounding
    slen = len('%.*f' % (n, f))
    return float(str(f)[:slen])

if __name__ == '__main__':
    try:
        NavTest()
        #rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("AMCL navigation test finished.")
