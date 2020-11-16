#!/usr/bin/env python
"""
ROS node that performs positioning and Euler measurement on Pozyx

This shows how to separate the position and IMU data in two separate channels.
"""

import pypozyx
import rospy
from geometry_msgs.msg import Point
import numpy
# from pozyx_ros_examples.msg import EulerAngles

from geometry_msgs.msg import Point, PoseStamped, Quaternion, PoseWithCovarianceStamped
import tf
import sys



remote_id = None
UWB_frame_ID = 'UWB'
odom_frame_ID = 'odom'
tag0_frame_ID = 'tag0_frame'
tag0_topic_ID = 'tag0_pose'



def pozyx_position_euler_pub():
	global rcvd_msgs
	global rec_x
	global rec_y
	#position_pub = rospy.Publisher(
	#   'pozyx_positioning', Point32, queue_size=100)
	position_pub = rospy.Publisher('/charlie_pose', Point, queue_size=100)
	#euler_pub = rospy.Publisher(
	#    'pozyx_euler_angles', EulerAngles, queue_size=100)
	euler_pub = rospy.Publisher('/orientation', Point, queue_size=100)
	pub1 = rospy.Publisher('/tag_pose0', Point, queue_size=100)
	pub2 = rospy.Publisher('/tag_pose1', Point, queue_size=100)
	

	rospy.init_node('position_euler_pub')
	rate=rospy.Rate(1)
	try:
	  # MOD @ 12-08-2020 
	  serial_port = pypozyx.get_first_pozyx_serial_port()
	  pozyx = pypozyx.PozyxSerial(serial_port)
	  #BKP -> pozyx = pypozyx.PozyxSerial(pypozyx.get_serial_ports()[0].device)
	except:
	  rospy.loginfo("Pozyx not connected")
	  return
	while not rospy.is_shutdown():
			coords = pypozyx.Coordinates()
			tags = pypozyx.Coordinates()
			pozyx.doPositioning(coords, remote_id=remote_id)
			pozyx.doPositioning(tags, remote_id=remote_id)
			
			euler_angles = pypozyx.EulerAngles()
			pozyx.getEulerAngles_deg(euler_angles)
			
			euler_pub.publish(euler_angles.heading,
							 euler_angles.roll, euler_angles.pitch)
			
							 
			rospy.loginfo("X: %f Y: %f" , tags.x, tags.y)
			rospy.loginfo(euler_angles)
	
			pub1.publish(tags.x/1000.0,tags.y/1000.0,tags.z/1000.0)
			pub2.publish(tags.x/1000.0, tags.y/1000.0,tags.z/1000.0)

			position_pub.publish(coords.x/1000.0, coords.y/1000.0, coords.z/1000.0)



			euler_angles.heading = numpy.deg2rad(euler_angles.heading) 
			tf_quat = tf.transformations.quaternion_from_euler(0, 0, -euler_angles.heading)
			br = tf.TransformBroadcaster()
			br.sendTransform((coords.x/1000.0, coords.y/1000.0, 0),
			tf_quat,
			rospy.Time.now(),
			tag0_frame_ID,
			UWB_frame_ID			
			)
					
			rate.sleep()
			
if __name__ == '__main__':
    try:
        pozyx_position_euler_pub()
    except rospy.ROSInterruptException:
        pass
