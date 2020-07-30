#!/usr/bin/env python
import rospy
import tf
from std_msgs.msg import String, Header
from geometry_msgs.msg import Twist
from math import sqrt, cos, sin, pi, atan2
import numpy
import sys
#Added
from sensor_msgs.msg import LaserScan
from dynamic_reconfigure.server import Server
from wall_following_assignment.cfg import wallpidConfig

class PID:
    def __init__(self, Kp, Td, Ti, dt):
        self.Kp = Kp
        self.Td = Td
        self.Ti = Ti
        self.curr_error = 0
        self.prev_error = 0
        self.sum_error = 0
        self.prev_error_deriv = 0
        self.curr_error_deriv = 0
        self.control = 0
        self.dt = dt
        
    def update_control(self, current_error, reset_prev=False):
        # todo: implement this
    	self.prev_error_deriv = (self.curr_error - self.prev_error) / self.dt
    	self.prev_error = self.curr_error
    	self.curr_error = current_error
    	self.curr_error_deriv = (self.curr_error - self.prev_error) / self.dt
    	self.sum_error += (current_error * self.dt) #good

    	#P term
        term1 = self.Kp * self.curr_error 
                
        #D term
        term2 = self.Td * self.curr_error_deriv

        #I term
        term3 = self.Ti * self.sum_error

        #return sum
        self.control = term1 + term2 + term3
        pass
        
    def get_control(self):
        return self.control
        
class WallFollowerHusky:
    def __init__(self):
        rospy.init_node('wall_follower_husky', anonymous=True)

        self.forward_speed = rospy.get_param("~forward_speed")
        self.desired_distance_from_wall = rospy.get_param("~desired_distance_from_wall")
        self.hz = 50 

        # todo: set up the command publisher to publish at topic '/husky_1/cmd_vel'
        # using geometry_msgs.Twist messages

        self.pid = PID(3.5,1.75,0.1,0.02) #change variables
        self.cmd = Twist()
        #Commented the dynamic reconfigure server out once I found optimal parameters
        #srv = Server(wallpidConfig, self.callback)
        self.cmd_pub = rospy.Publisher('/husky_1/cmd_vel', Twist, queue_size=10)
        self.cte_pub = rospy.Publisher('/husky_1/cte', String, queue_size=10)
        #from tutorial
        self.laser_sub = rospy.Subscriber("/husky_1/scan", LaserScan, self.laser_scan_callback)

    def callback(self, config, level):
        self.pid.Kp = config.p_cont
        self.pid.Ti = config.i_cont
        self.pid.Td = config.d_cont
        return config      
        
    def laser_scan_callback(self, msg):
        # todo: implement this
        # Populate this command based on the distance to the closest
        # object in laser scan. I.e. compute the cross-track error
        # as mentioned in the PID slides.

        # You can populate the command based on either of the following two methods:
        # (1) using only the distance to the closest wall
        # (2) using the distance to the closest wall and the orientation of the wall
        #
        # If you select option 2, you might want to use cascading PID control. 
  
        # cmd.angular.z = ???

        #To get min values, take min value with range from left side of sensor
        self.numReadings = int(len(msg.ranges)/2)
        self.mymin = 100000
        for i in range(0, self.numReadings):
        	if msg.ranges[i] < self.mymin and msg.ranges[i] > msg.range_min and msg.ranges[i] < msg.range_max:
        		self.mymin = msg.ranges[i]

        #calculate, publish CTE. update control, update angle, publish robot command
        self.error = self.mymin - self.desired_distance_from_wall #calc error
        self.cte_pub.publish(str(self.error)) #publish error
        self.pid.update_control(self.error) #pass error to calculate control
        self.cmd.angular.z = self.pid.get_control() #update angle
        self.cmd.linear.x = self.forward_speed
        self.cmd_pub.publish(self.cmd) #publish the command
        pass      

    def run(self):
        rate = rospy.Rate(self.hz)
        while not rospy.is_shutdown():
            rate.sleep()

    
if __name__ == '__main__':
    wfh = WallFollowerHusky()
    wfh.run()


