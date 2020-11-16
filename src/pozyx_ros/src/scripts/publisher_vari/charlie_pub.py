#!/usr/bin/env python
"""
ROS node that publishes the pose (position + quaternion) of the Pozyx

This is an example of how to combine sensor data and positioning into a single
channel output.

Quite overkill using _Pose, as this consists of 7 float64s, while the source
data comes from integers. Suggestions to replace this are quite welcomed.
"""

import pypozyx
import rospy
import numpy
from geometry_msgs.msg import Point, PoseStamped, Quaternion, PoseWithCovarianceStamped
import tf
import sys

UWB_frame_ID = 'UWB'
odom_frame_ID = 'odom'
tag0_frame_ID = 'tag0_frame'
tag0_topic_ID = 'tag0_pose'

pose = PoseWithCovarianceStamped()
def vicon_cb(data):
    global pose
    pose = data

remote_id = None

def pozyx_pose_pub():
	pub = rospy.Publisher('/charlie_pose', PoseWithCovarianceStamped, vicon_cb, queue_size=1000) 
	pub1 = rospy.Publisher('/tag_pose0', Point, queue_size=1000)
	pub2 = rospy.Publisher('/tag_pose1', Point, queue_size=1000)
    
	rospy.init_node('pozyx_pose_node')
	try:
		# MOD @ 12-08-2020 
		serial_port = pypozyx.get_first_pozyx_serial_port()
		pozyx = pypozyx.PozyxSerial(serial_port)
		# BKP -> pozyx = pypozyx.PozyxSerial(pypozyx.get_serial_ports()[0].device)
	except:
		rospy.loginfo("Pozyx not connected")
		return
	while not rospy.is_shutdown():
		coords = pypozyx.Coordinates()
		tags = pypozyx.Coordinates()
		quat = pypozyx.Quaternion()

		pozyx.doPositioning(coords, pypozyx.POZYX_3D, remote_id=remote_id)
		pozyx.getQuaternion(quat, remote_id=remote_id)

	

		pose.pose.pose.position.x = coords.x/1000.0
		pose.pose.pose.position.y = coords.y/1000.0
		pose.pose.pose.position.z = coords.z/1000.0
		
		# ho messo come messaggio PoseWithCovarianceStamped ed ho aggiunto la covarianza a mano, quindi per accedere alle variabili di pos e orient bisogna fare pose.pose.pose, se fosse solo PoseStamped basta pose.pose
		
		pose.pose.covariance[0]  = 0.01;
		pose.pose.covariance[7]  = 0.01;
		pose.pose.covariance[14] = 99999;
		pose.pose.covariance[21] = 99999;
		pose.pose.covariance[28] = 99999;
		pose.pose.covariance[35] = 0.01;
		

		tags.x = coords.x /1000.0
		tags.y = coords.y /1000.0
		tags.z = coords.z /1000.0

		pose.pose.pose.orientation.x = quat.x
		pose.pose.pose.orientation.y = quat.y
		pose.pose.pose.orientation.z = quat.z
		pose.pose.pose.orientation.w = quat.w
		
		rospy.loginfo("POS: %s, QUAT: %s" % (str(tags), str(quat)))	

		pub.publish(pose)
		pub1.publish(Point(tags.x,tags.y,tags.z))
		pub2.publish(Point(tags.x,tags.y,tags.z))
		
		euler_angles = pypozyx.EulerAngles()
		euler_angles.heading = numpy.deg2rad(euler_angles.heading) 
		tf_quat = tf.transformations.quaternion_from_euler(0, 0, -euler_angles.heading)
		br = tf.TransformBroadcaster()
		br.sendTransform((coords.x/1000.0, coords.y/1000.0, 0),
		tf_quat,
		rospy.Time.now(),
		tag0_frame_ID,
		UWB_frame_ID
		)



if __name__ == '__main__':
    try:
        pozyx_pose_pub()
    except rospy.ROSInterruptException:
        pass
