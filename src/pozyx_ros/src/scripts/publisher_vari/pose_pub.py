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
from geometry_msgs.msg import Point, PoseStamped, Quaternion

pose = PoseStamped()
def vicon_cb(data):
    global pose
    pose = data

remote_id = None

def pozyx_pose_pub():
    pub = rospy.Publisher('amcl_pose', PoseStamped, vicon_cb, queue_size=100)
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
        quat = pypozyx.Quaternion()
        
	pozyx.doPositioning(coords, pypozyx.POZYX_3D, remote_id=remote_id)
        pozyx.getQuaternion(quat, remote_id=remote_id)

        rospy.loginfo("POS: %s, QUAT: %s" % (str(coords), str(quat)))

        pose.pose.position.x = coords.x
        pose.pose.position.y = coords.y
        pose.pose.position.z = coords.z

        pose.pose.orientation.x = quat.x
        pose.pose.orientation.y = quat.y
        pose.pose.orientation.z = quat.z
        pose.pose.orientation.w = quat.w

        pub.publish(pose)


if __name__ == '__main__':
    try:
        pozyx_pose_pub()
    except rospy.ROSInterruptException:
        pass
