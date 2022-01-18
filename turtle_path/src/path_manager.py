#!/usr/bin/env python
import rospy
from math import pi, fmod, sin, cos, sqrt
from turtle_path.srv import *
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
# hint: some imports are missing

cur_pos = Pose()

def cb_pose(data): # get the current position from subscribing the turtle position

    global cur_pos
    cur_pos = data

def cb_walk(req):

    global cur_pos
    
    if (req.distance < 0):
        rospy.loginfo("[-] Error: Invalid Input")
        return False
    
    # hint: calculate the projected (x, y) after walking the distance,
    # and return false if it is outside the boundary
    px = cur_pos.x + req.distance * cos(cur_pos.theta)
    py = cur_pos.y + req.distance * sin(cur_pos.theta)
    if int(px) not in range(0,11) or int(py) not in range(0,11):
        rospy.loginfo("[-] Error: Input out of Range")
        return False

    rate = rospy.Rate(100) # 100Hz control loop
    vel = Twist()

    while True: # control loop
        
        # in each iteration of the control loop, publish a velocity
        # hint: you need to use the formula for distance between two points
        separation = sqrt((cur_pos.x - px)**2 + (cur_pos.y - py)**2)
        
        vel.linear.x = 1.4 * separation
        pub.publish(vel)
        
        rate.sleep()
        
        if abs(separation) < 0.05:
            break
    
    # publish a velocity 0 at the end, to ensure the turtle really stops
    pub.publish(vel)

    return True

def cb_orientation(req):

    global cur_pos
    
    rate = rospy.Rate(100) # 100Hz control loop
    vel = Twist()
    
    while True: # control loop
        
        # in each iteration of the control loop, publish a velocity

        # hint: signed smallest distance between two angles: 
        # see https://stackoverflow.com/questions/1878907/the-smallest-difference-between-2-angles
        dist = fmod(req.orientation - cur_pos.theta + 3 * pi, 2 * pi) - pi
        
        vel.angular.z = 1.2 * dist
        pub.publish(vel)
        
        rate.sleep()
        
        if abs(dist) < 0.05:
            break
    
    # publish a velocity 0 at the end, to ensure the turtle really stops
    pub.publish(vel)

    return True

if __name__ == '__main__':
    rospy.init_node('path_manager')
    
    pub = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=1)
    # publisher of the turtle velocity
    rospy.Subscriber("/turtle1/pose", Pose, cb_pose)
    # subscriber of the turtle position, callback to cb_pose
    
    ## init each service server here:
    # callback to cb_orientation
    rospy.Service("set_orientation", SetOrientation, cb_orientation)
    rospy.Service("walk_distance", WalkDistance, cb_walk)		# callback to cb_walk
    
    rospy.spin()

