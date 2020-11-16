#!/usr/bin/env python

import pypozyx
import rospy
import numpy as np
import math
from std_msgs.msg import Float64
from geometry_msgs.msg import Point, PoseStamped, Quaternion, PoseWithCovarianceStamped
from sensor_msgs.msg import LaserScan
import tf
import sys
import dynamic_reconfigure.client
from defs import *

from std_srvs.srv import Empty

'''
	pose.pose.position.x = data.pose.position.x
	pose.pose.position.y = data.pose.position.y
	pose.pose.position.z = data.pose.position.z
	
	#pose.pose.orientation.x =	data.pose.orientation.x
	#pose.pose.orientation.y =	data.pose.orientation.y
	#pose.pose.orientation.z =	data.pose.orientation.z
	#pose.pose.orientation.w =	data.pose.orientation.w
	'''
tag_center_pose = PoseStamped()
amcl_pose = PoseWithCovarianceStamped()
scansione = LaserScan()
startstop = 0.0
th_laser = 100

def vicon_cb_0(data):
    global tag_center_pose
    tag_center_pose = data
    
def vicon_cb_1(data):
    global amcl_pose
    amcl_pose = data
    
    
def lidar_cb(data):
    global scansione
    scansione = data
        

			
def motori_cb(data):
    global startstop
    startstop = data
remote_id = None

def amcl2robot_pose_pub():
	global tag_center_pose
	global amcl_pose
	global orient
	global startstop
	global th_laser
	
  # si iscrive al topic che contiene la posa del punto centrale tra le due tag
	sub_tag_in_map = rospy.Subscriber(tag_in_map_topic_ID, PoseStamped, vicon_cb_0)
	sub_amcl_pose = rospy.Subscriber("amcl_pose", PoseWithCovarianceStamped, vicon_cb_1)
	sub_amcl_pose = rospy.Subscriber("/scan", LaserScan, lidar_cb)
	sub_start_stop = rospy.Subscriber("/start_and_stop", Float64, motori_cb)


	
	robot_pose_pub = rospy.Publisher("/robot_pose", Point, queue_size=100)
	pub_start_stop = rospy.Publisher("/start_and_stop", Float64, queue_size=100)
    
	rospy.init_node('amcl2robot_pose_PY')
	
	
	while not rospy.is_shutdown():
		
		# controlla quanto la posa di AMCL si discosta da quella delle UWB, tutto nel frame MAP
		
		amcl_x = amcl_pose.pose.pose.position.x
		amcl_y = amcl_pose.pose.pose.position.y
		amcl_orient = tf.transformations.euler_from_quaternion((amcl_pose.pose.pose.orientation.x, amcl_pose.pose.pose.orientation.y, amcl_pose.pose.pose.orientation.z, amcl_pose.pose.pose.orientation.w ))
		amcl_orient = amcl_orient[2] # prendo lo yaw 
		
		# punto centrale tra le due tag
		tag_x = tag_center_pose.pose.position.x
		tag_y = tag_center_pose.pose.position.y
		tag_orient = tf.transformations.euler_from_quaternion((tag_center_pose.pose.orientation.x, tag_center_pose.pose.orientation.y, tag_center_pose.pose.orientation.z, tag_center_pose.pose.orientation.w ))
		tag_orient = tag_orient[2] # prendo lo yaw 
		
		if ( np.sum(scansione.intensities) <= th_laser ):
			blind_laser = True
		else :
			blind_laser = False
		
		robot_pose = Point()
		
		
		if ( blind_laser ):
		
			#controllo_precedente = startstop
			#pub_start_stop.publish(0.0) 
						
			robot_pose.x = tag_x
			robot_pose.y = tag_y
			robot_pose.z = tag_orient
			rospy.loginfo("Laser offline, navigazione UWB in corso")
			
			
			
		else:

			robot_pose.x = amcl_x
			robot_pose.y = amcl_y
			robot_pose.z = amcl_orient
			
		robot_pose_pub.publish(robot_pose)
		# -------------------------- TF --------------------------
		tf_quat = tf.transformations.quaternion_from_euler(0, 0, robot_pose.z)
		# publish TF	
		br_0 = tf.TransformBroadcaster()
		br_0.sendTransform((robot_pose.x, robot_pose.y, 0),
		tf_quat,
		rospy.Time.now(),
		robot_pose_frame_ID,
		map_frame_ID
		)


if __name__ == '__main__':
    try:
        amcl2robot_pose_pub()
    except rospy.ROSInterruptException:
        pass
