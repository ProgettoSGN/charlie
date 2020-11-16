#!/usr/bin/env python
"""
ROS node that publishes the pose (position + quaternion) of the Pozyx

This is an example of how to combine sensor data and positioning into a single
channel output.

Quite overkill using _Pose, as this consists of 7 float64s, while the source
data comes from integers. Suggestions to replace this are quite welcomed.
"""
import numpy
import pypozyx
import rospy
from geometry_msgs.msg import Point, PoseStamped, Quaternion
import tf
import decimal 

# my definitions 
from defs import*

# a list for pose records
rec_x = []
rec_y = []
rec_z = []


# number of samples to collect 
n_samples = 10
rcvd_msgs = 0 


pose = PoseStamped()
pose_f = PoseStamped()

def callback(data):
	global rcvd_msgs
	global n_samples
	global pose
	# read incoming message and save into pose
	
	#pose.header.frame_id = UWB_frame_ID
	#pose.header.stamp = rospy.Time.now()
	pose.pose.position.x = data.pose.position.x
	pose.pose.position.y = data.pose.position.y
	pose.pose.position.z = data.pose.position.z
	
	#pose.pose.orientation.x =	data.pose.orientation.x
	#pose.pose.orientation.y =	data.pose.orientation.y
	#pose.pose.orientation.z =	data.pose.orientation.z
	#pose.pose.orientation.w =	data.pose.orientation.w

	
	# DONE AFTER n_samples received messages
   # if received messages are enough, move 1 step forwar the moving window
	#					+-----------+-----------+-----------+-----------+
	#	<--pop(0)--	|				|				|				|				|   <--append--
	#					+-----------+-----------+-----------+-----------+
	#
	# then evaluate the mean
	if rcvd_msgs == n_samples :
		rec_x.append(pose.pose.position.x)
		rec_y.append(pose.pose.position.y)
		rec_z.append(pose.pose.position.z)
		rec_x.pop(0)
		rec_y.pop(0)
		rec_z.pop(0)

		# mean
		pose_f.pose.position.x = sum(rec_x) / len(rec_x)
		pose_f.pose.position.y = sum(rec_y) / len(rec_y)
		pose_f.pose.position.z = sum(rec_z) / len(rec_z)
		
		pose_f.pose.orientation.x =	data.pose.orientation.x
		pose_f.pose.orientation.y =	data.pose.orientation.y
		pose_f.pose.orientation.z =	data.pose.orientation.z
		pose_f.pose.orientation.w =	data.pose.orientation.w
		
		pose_f.header.frame_id = UWB_frame_ID
		pose_f.header.stamp = rospy.Time.now()

		
		
		
		
			
	# fullfill the moving window for the first time with n samples
	elif rcvd_msgs < n_samples:
		rec_x.append(pose.pose.position.x)
		rec_y.append(pose.pose.position.y)
		rec_z.append(pose.pose.position.z)
		rcvd_msgs += 1
		rospy.loginfo("collecting samples: %d / %d collected", rcvd_msgs, n_samples)
		if rcvd_msgs == n_samples :
			rospy.loginfo("DONE - starting to publish")
			pose_f.pose.position.x = sum(rec_x) / n_samples
			pose_f.pose.position.y = sum(rec_y) / n_samples
			pose_f.pose.position.z = sum(rec_z) / n_samples


	else:
		print('error')

			

def filter():
	global coords

	rospy.init_node('filter_node_2')
	#rate = rospy.Rate(100.0)

	filter_sub = rospy.Subscriber(tag1_topic_ID, PoseStamped, callback)
	filter_pub = rospy.Publisher(tag1_topic_ID_f, PoseStamped, queue_size=100)

	
	pose = PoseStamped()
	
	while not rospy.is_shutdown():
	
		filter_pub.publish(pose_f)
		
		# -------------------------- TF --------------------------
		tf_euler = tf.transformations.euler_from_quaternion((pose_f.pose.orientation.x, pose_f.pose.orientation.y, pose_f.pose.orientation.z, pose_f.pose.orientation.w))
		heading = tf_euler[2]
		tf_quat = tf.transformations.quaternion_from_euler(0, 0, heading)
		# publish TF	
		br_0 = tf.TransformBroadcaster()
		br_0.sendTransform((pose_f.pose.position.x, pose_f.pose.position.y, 0),
		tf_quat,
		rospy.Time.now(),
		tag1_frame_ID_f,
		UWB_frame_ID
		)
		

		#rate.sleep()
		


if __name__ == '__main__':
    try:
        filter()
    except rospy.ROSInterruptException:
        pass
