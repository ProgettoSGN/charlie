#!/usr/bin/env python
"""
ROS node that performs positioning and Euler measurement on Pozyx

This shows how to separate the position and IMU data in two separate channels.
"""

import pypozyx
import numpy
import rospy
from geometry_msgs.msg import Point
# from pozyx_ros_examples.msg import EulerAngles
from nav_msgs.msg import Odometry
import tf
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3

# names for frames
tag_frame_ID = "tag_0"
UWB_frame_ID = "UWB"


# control vars
records = 0
n_samples = 10

remote_id = None


def pozyx_position_euler_pub():
    #position_pub = rospy.Publisher(
     #   'pozyx_positioning', Point32, queue_size=100)
    position_pub = rospy.Publisher(
        '/tag_pose0', Point, queue_size=100)
    #euler_pub = rospy.Publisher(
    #    'pozyx_euler_angles', EulerAngles, queue_size=100)
    euler_pub = rospy.Publisher(
        '/orientation', Point, queue_size=100)
    
    vx = 0.0
    vy = 0.0
    vth = 0.0
    rospy.init_node('position_euler_pub') #PROVA
    #pub odom msg for move_base
    odom_pub = rospy.Publisher("odom", Odometry, queue_size=50)
    odom_broadcaster = tf.TransformBroadcaster()
    current_time = rospy.Time.now()
    last_time = rospy.Time.now()
    
    #rospy.init_node('position_euler_pub')
    try:
        # MOD @ 12-08-2020 
        serial_port = pypozyx.get_first_pozyx_serial_port()
        pozyx = pypozyx.PozyxSerial(serial_port)
        #BKP -> pozyx = pypozyx.PozyxSerial(pypozyx.get_serial_ports()[0].device)
    except:
        rospy.loginfo("Pozyx not connected")
        return
    while not rospy.is_shutdown():

	#################### COORDS ####################
        coords = pypozyx.Coordinates() 

        pozyx.doPositioning(coords, remote_id=remote_id)
	
	# convert from mm to m
	#rospy.loginfo("POS_1: %s m" % (str(coords)))
	coords.x = coords.x / 1000.0
	coords.y = coords.y / 1000.0
	coords.z = coords.z / 1000.0
	#rospy.loginfo("POS_1: %s m" % (str(coords)))
	'''
	if records < n_samples:
		coords.x += coords.x
		coords.y += coords.y
		coords.z += coords.z
		records = 'done'
		continue
	elif records == 'done':
		coords.x /= n_samples
		coords.y /= n_samples
		coords.z /= n_samples
		records = 'finish'
		continue
	'''
        position_pub.publish(coords.x, coords.y, coords.z)

	#################### ANGLES #####################
        euler_angles = pypozyx.EulerAngles()

        pozyx.getEulerAngles_deg(euler_angles)
	
	# convert from degrees to radians ( *3.14/180 )
	euler_angles.heading = numpy.deg2rad(euler_angles.heading) 
	euler_angles.roll = numpy.deg2rad(euler_angles.roll)
	euler_angles.pitch = numpy.deg2rad(euler_angles.pitch)

	
        rospy.loginfo("POS: %s, ANGLES: %s" % (str(coords), str(euler_angles)))
        euler_pub.publish(euler_angles.heading,euler_angles.roll, euler_angles.pitch)


	#################### PUBLISHING ODOM TF ################
        # combine pos and angle info and publish as odom msg
        current_time = rospy.Time.now()

        # odometry is 6DOF, created quaternion from yaw
        odom_quat = tf.transformations.quaternion_from_euler(0, 0, euler_angles.heading)
        # publish the transform over tf
        odom_broadcaster.sendTransform((coords.x,coords.y, 0.),odom_quat,current_time,tag_frame_ID,UWB_frame_ID)


        # publish the odometry message over ROS
        odom = Odometry()
        odom.header.stamp = current_time
        odom.header.frame_id = UWB_frame_ID

        odom.pose.pose = Pose(Point(coords.x, coords.y, 0.), Quaternion(*odom_quat))
        odom.child_frame_id = tag_frame_ID
        odom.twist.twist = Twist(Vector3(vx, vy, 0), Vector3(0, 0, vth)) # set the velocity
        odom_pub.publish(odom)
        last_time = current_time


     

if __name__ == '__main__':
    try:
        pozyx_position_euler_pub()
    except rospy.ROSInterruptException:
        pass
