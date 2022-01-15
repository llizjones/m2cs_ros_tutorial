#!/usr/bin/env python
import rospy
from m2_ps4.msg import *
from std_srvs.srv import Empty, EmptyRequest
from geometry_msgs.msg import Twist
from turtlesim.srv import SetPen, SetPenRequest
# hint: some imports are missing

old_data = Ps4Data()
k = 2
def callback(data):
    global old_data
    global k
    
    t = Twist()
    req = SetPenRequest()
    E = EmptyRequest()
    
    # you should publish the velocity here!
    pub.publish(t)
    
    # hint: to detect a button being pressed, you can use the following pseudocode:
    # 
    #if ((data.button is pressed) and (old_data.button not pressed)):
    # then do something...
    if (data.tpad_y > 0 and k<=5):
    	k+=1
    if (data.tpad_y < 0 and k<=5):
    	k-=1
    if (data.hat_ly != old_data.hat_ly):
        t.linear.x = data.hat_lx*k
    elif (data.hat_ly==-1 or data.hat_ly==1):
        t.linear.x = data.hat_lx*k
    if (data.hat_rx != old_data.hat_rx):
        t.angular.z = data.hat_rx*k
    elif (data.hat_rx==-1 or data.hat_rx==1):
        t.angular.z = data.hat_rx*k
    if (data.circle):
	req.r, req.g, req.b = 255, 0, 0
	srv_col(res)
    if (data.triangle): 	
	req.r, req.g, req.b = 0, 255, 0
	srv_col(res)
    if (data.cross):
	req.r, req.g, req.b = 0, 0, 255
	srv_col(res)
    if (data.square):
	req.r, req.g, req.b = 255, 0, 255
	srv_col(res)
    if (data.ps):
	srv_clr(E)
    pub.publish(t)
    old_data = data
    
if __name__ == '__main__':
    rospy.init_node('ps4_controller')
    
    pub = rospy.Publisher("/turtle1/cmd_vel",Twist,queue_size=1)
    # publisher object goes here... hint: the topic type is Twist
    sub = rospy.Subscriber("/input/ps4_data",Ps4Data,callback)
    
    # one service object is needed for each service called!
    srv_col = rospy.ServiceProxy("turtle1/set_pen", SetPen)
    srv_clr = rospy.ServiceProxy("clear", Empty)
    # fill in the other service client object...
    
    rospy.spin()
