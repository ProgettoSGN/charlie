#!/usr/bin/env python
'''
	questo nodo si iscrive ai topic delle tag (UWB) ed al topic di orientazione (dell'STM) proveniente dalla seriale;
	legge il file "UWB2map_TF.txt" da cui ricava la roto-traslazione tra i frame UWB e map, dopodiche'
	calcola la posa del punto centrale tra le due tag in coordinate map e la pubblica assieme ad una TF
'''
import pypozyx
import rospy
import numpy as np
from math import *
from geometry_msgs.msg import Point, PoseStamped, Quaternion, PoseWithCovarianceStamped
import tf
import sys

from defs import *



tag0_pose = PoseStamped()
tag1_pose = PoseStamped()
map_pose = PoseStamped()
map_yaw = 0.0

orient = Point()

def vicon_cb_0(data):
    global tag0_pose
    tag0_pose = data
    
def vicon_cb_1(data):
    global tag1_pose
    tag1_pose = data
    
    
def vicon_cb_3(data):
    global orient
    orient = data
    
# trasforma da framw UWB a frame map	
def UWB2map(data):
		global map_pose
		global map_yaw
		
		new_pose = PoseStamped()
		new_pose.header.frame_id = map_frame_ID
		

		# ricava gli angoli di eulero della mappa rispetto al sistema UWB
		map_angles = tf.transformations.euler_from_quaternion([map_pose.pose.orientation.x, map_pose.pose.orientation.y, map_pose.pose.orientation.z, map_pose.pose.orientation.w])
		
		map_yaw = map_angles[2] #seleziona la componente di rotazione verticale (asse z, verso l'alto)
		
		
		# ricava gli angoli di eulero della tag rispetto al sistema UWB
		tag_angles = tf.transformations.euler_from_quaternion([data.pose.orientation.x, data.pose.orientation.y, data.pose.orientation.z, data.pose.orientation.w])
		tag_yaw = tag_angles[2]
		

		
		# matrice di rotazione da UWB a MAP 
		# descrive il passaggio di coordinate da MAP a UWB 
		#	cos(th) -sin(th)		 
		#	sin(th)  cos(th)			th = angolo da UWB a MAP
		#
		#	dato che voglio portare le coordinate da UWB a MAP devo usare la trasposta
		#	
		#	 cos(th) +sin(th)		 
		#	-sin(th)  cos(th)			th = angolo da UWB a MAP
		
		
		# prima trasla poi ruota, porta i dati della tag da coordinate uwb in coordinate map
		new_pose.pose.position.x = cos(map_yaw) * (data.pose.position.x - map_pose.pose.position.x) + sin(map_yaw) * (data.pose.position.y - map_pose.pose.position.y)
		new_pose.pose.position.y = -sin(map_yaw) * (data.pose.position.x - map_pose.pose.position.x) + cos(map_yaw) * (data.pose.position.y - map_pose.pose.position.y)
		new_pose.pose.position.z = 0.0 #(data.pose.position.z - map_pose.pose.position.z)
		
		# ruota
		new_pose.pose.orientation = tf.transformations.quaternion_from_euler(0.0, 0.0, tag_yaw - map_yaw)
		 
		return new_pose
		
		

remote_id = None
tag_center = PoseStamped()


def pozyx_tag_center_pub():
	global tag0_pose
	global tag1_pose
	global tag_center

  
	sub_tag_0 = rospy.Subscriber(tag0_topic_ID, PoseStamped, vicon_cb_0)
	sub_tag_1 = rospy.Subscriber(tag1_topic_ID, PoseStamped, vicon_cb_1)
	sub_orien = rospy.Subscriber("orientation", Point, vicon_cb_3)
	
	pub = rospy.Publisher(tag_in_map_topic_ID, PoseStamped, queue_size=100)
	

	rospy.init_node('map_center')
	rate = rospy.Rate(50)
		
	rospy.loginfo('reading file for TF %s -> %s', UWB_frame_ID, map_frame_ID)
	f = open("/home/robot/charlie_ws/src/pozyx_ros/src/scripts/my_pozyx/UWB2map_TF.txt","r") # accedi al file in lettura


	# map_pose conterra' i dati della tf tra UWB e mappa
	map_pose.pose.position.x = float(f.readline()[:-2])
	rospy.loginfo('x: %f',map_pose.pose.position.x)
	map_pose.pose.position.y = float(f.readline()[:-2])
	rospy.loginfo('y: %f',map_pose.pose.position.y)
	map_pose.pose.position.z = float(f.readline()[:-2])
	rospy.loginfo('z: %f',map_pose.pose.position.z)
	map_pose.pose.orientation.x = float(f.readline()[:-2])
	rospy.loginfo('orien.x: %f',map_pose.pose.orientation.x)
	map_pose.pose.orientation.y = float(f.readline()[:-2])
	rospy.loginfo('orien.y: %f',map_pose.pose.orientation.y)
	map_pose.pose.orientation.z = float(f.readline()[:-2])
	rospy.loginfo('orien.z: %f',map_pose.pose.orientation.z)
	map_pose.pose.orientation.w = float(f.readline()[:-2])
	rospy.loginfo('orien.w: %f',map_pose.pose.orientation.w)
	f.close()
	
	tf_UWB_map = tf.TransformBroadcaster()
	
	rospy.loginfo('reading file for TF %s -> %s DONE', UWB_frame_ID, map_frame_ID)
	
	while not rospy.is_shutdown():
		tf_UWB_map.sendTransform((map_pose.pose.position.x,map_pose.pose.position.y,0.),
		(map_pose.pose.orientation.x,map_pose.pose.orientation.y,map_pose.pose.orientation.z, map_pose.pose.orientation.w), 
		rospy.Time.now(),
		map_frame_ID,
		UWB_frame_ID)	
		
		# porta le coordinate dei tag nel frame map
		tag_0_map = UWB2map(tag0_pose)
		tag_1_map = UWB2map(tag1_pose)
		
		tag_center.header.frame_id = map_frame_ID
		# prendi la media tra le posizioni delle tag come positione del laser data dal sistema UWB 
		tag_center.pose.position.x = ( tag_0_map.pose.position.x + tag_1_map.pose.position.x ) / 2.0
		tag_center.pose.position.y = ( tag_0_map.pose.position.y + tag_1_map.pose.position.y ) / 2.0
		
		
		############### tf for check
		theta = -orient.z - map_yaw#STM in z-down, viene convertito in z-up
		
		
		
		z_quat = tf.transformations.quaternion_from_euler(0, 0, theta)
		
		#tag_center.pose.orientation = z_quat	# usa come orientazione quella fornita dall'STM
		tag_center.pose.orientation.x = z_quat[0]
		tag_center.pose.orientation.y = z_quat[1]
		tag_center.pose.orientation.z = z_quat[2]
		tag_center.pose.orientation.w = z_quat[3]
		
		br = tf.TransformBroadcaster()
		br.sendTransform((tag_center.pose.position.x ,tag_center.pose.position.y,0.),
			[tag_center.pose.orientation.x, tag_center.pose.orientation.y, tag_center.pose.orientation.z, tag_center.pose.orientation.w], 
			rospy.Time.now(),
			tag_in_map_frame_ID,
			map_frame_ID)
		###############



		pub.publish(tag_center)
		#rospy.loginfo('Publishing TF and pose from %s -> %s', map_frame_ID, tag_in_map_frame_ID);
		rate.sleep()	



if __name__ == '__main__':
    try:
        pozyx_tag_center_pub()
    except rospy.ROSInterruptException:
        pass
