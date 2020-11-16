#!/usr/bin/env python

import pypozyx
import rospy
import numpy as np
import math
from std_msgs.msg import Float64
from geometry_msgs.msg import Point, PoseStamped, Quaternion, PoseWithCovarianceStamped
import tf
import sys
import dynamic_reconfigure.client
from defs import *
import time

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
orient = Point()
startstop = 0.0

def vicon_cb_0(data):
    global tag_center_pose
    tag_center_pose = data
    
def vicon_cb_1(data):
    global amcl_pose
    amcl_pose = data
    
    
def vicon_cb_2(data):
    global orient
    orient = data
        
def pose_fix_callback(config):
		rospy.loginfo("Config AMCL , update_min_d{update_min_d}".format(**config))
			
def motori_cb(data):
    global startstop
    startstop = data
remote_id = None

def pozyx_pose_fix_pub():
	global tag_center_pose
	global amcl_pose
	global orient
	global startstop
	
	rospy.init_node('pozyx_initial_pose_pub')
	
  # si iscrive al topic che contiene la posa del punto centrale tra le due tag
	sub_tag_in_map = rospy.Subscriber(tag_in_map_topic_ID, PoseStamped, vicon_cb_0)
	sub_start_stop = rospy.Subscriber("/start_and_stop", Float64, motori_cb)
	
	sub_amcl_pose = rospy.Subscriber("amcl_pose", PoseWithCovarianceStamped, vicon_cb_1)
	sub_orient = rospy.Subscriber("orientation", Point, vicon_cb_2)
	
	pose_fix_pub = rospy.Publisher("/initialpose", PoseWithCovarianceStamped, queue_size=1)  #100
	pub_start_stop = rospy.Publisher("/start_and_stop", Float64, queue_size=100)
	time.sleep(30) 
	
	client = dynamic_reconfigure.client.Client("amcl", timeout=30, config_callback=pose_fix_callback)
	
	rate = rospy.Rate(50)
	
	while not rospy.is_shutdown():
		initial_pose = PoseWithCovarianceStamped()
		
		# controlla quanto la posa di AMCL si discosta da quella delle UWB, tutto nel frame MAP
		
		amcl_x = amcl_pose.pose.pose.position.x
		amcl_y = amcl_pose.pose.pose.position.y
		
		# punto centrale tra le due tag
		tag_x = tag_center_pose.pose.position.x
		tag_y = tag_center_pose.pose.position.y
		
		# calcola errore di posizionamento
		position_error = math.sqrt( (tag_x - amcl_x)**2 + (tag_y - amcl_y)**2 )
		threshold = 1.5 # metri
		
		"""if (tag0_pose.pose.position.x == 0.0 and tag0_pose.pose.position.y == 0.0 and tag1_pose.pose.position.x == 0.0 and tag0_pose.pose.position.y == 0.0 ):
			POZYX_FAIL = True
		else:
			POZYX_FAIL = False"""
				
		
		if (position_error > threshold and (tag_x != 0.0 and tag_y != 0.0)):
		
			#controllo_precedente = startstop
			#pub_start_stop.publish(0.0) 
			initial_pose.header.frame_id = 'map'
			# ho messo come messaggio PoseWithCovarianceStamped ed ho aggiunto la covarianza a mano, quindi per accedere alle variabili di pos e orient bisogna fare pose.pose.pose, se fosse solo PoseStamped basta pose.pose
			# COV MATRIX
			"""initial_pose.pose.covariance[0]  = 0.0009223539672174041;
			initial_pose.pose.covariance[7]  = 0.00056183405566268;
			initial_pose.pose.covariance[14] = 0.0;
			initial_pose.pose.covariance[21] = 0.0;
			initial_pose.pose.covariance[28] = 0.0;
			initial_pose.pose.covariance[35] = 0.0001573948106108449;"""
			
			initial_pose.pose.covariance[0]  = 0.215;
			initial_pose.pose.covariance[7]  = 0.26;
			initial_pose.pose.covariance[14] = 0.0;
			initial_pose.pose.covariance[21] = 0.0;
			initial_pose.pose.covariance[28] = 0.0;
			initial_pose.pose.covariance[35] = 0.1; #0.07 abbiamo provato ad aumentare per correggere disallineamento
		
		
			# punto medio tra le tag
			initial_pose.pose.pose.position.x = tag_x
			initial_pose.pose.pose.position.y = tag_y
			initial_pose.pose.pose.position.z = 0.0

			# orientazione come ATAN tra 2 punti
			#theta = np.arctan2([tag0_pose.pose.position.y -  tag1_pose.pose.position.y], [tag0_pose.pose.position.x - tag1_pose.pose.position.x])
			
			theta = -orient.z #STM in z-down, viene convertito in z-up
		
			quat = tf.transformations.quaternion_from_euler(0, 0, theta)
		
			initial_pose.pose.pose.orientation = tag_center_pose.pose.orientation
			#initial_pose.pose.pose.orientation.x = quat[0]
			#initial_pose.pose.pose.orientation.y = quat[1]
			#initial_pose.pose.pose.orientation.z = quat[2]
			#initial_pose.pose.pose.orientation.w = quat[3]
		
			pose_fix_pub.publish(initial_pose)
			#rospy.ServiceProxy("request_nomotion_update",Empty)
			#rospy.sleep(1)
			time.sleep(2)
			client.update_configuration({"update_min_d":0.0})
			
			#rospy.sleep(2)
			time.sleep(3)
			client.update_configuration({"update_min_d":0.05})
			#pub_start_stop.publish(controllo_precedente) 
			rate.sleep()


if __name__ == '__main__':
    try:
        pozyx_pose_fix_pub()
    except rospy.ROSInterruptException:
        pass
