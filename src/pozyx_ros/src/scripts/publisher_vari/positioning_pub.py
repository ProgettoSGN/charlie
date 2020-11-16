#!/usr/bin/env python
"""ROS node that performs 3D positioning on Pozyx"""

import pypozyx
import rospy
# from geometry_msgs.msg import Point32
from geometry_msgs.msg import Point
remote_id = None


def pozyx_positioning_pub():
   # pub = rospy.Publisher('pozyx_positioning', Point32, queue_size=100)
    pub = rospy.Publisher('/tag_pose0', Point, queue_size=100)
    pub1 = rospy.Publisher('/tag_pose1', Point, queue_size=100)
    
    rospy.init_node('positioning_pub')
    try:
     # MOD @ 12-08-2020 
        serial_port = pypozyx.get_first_pozyx_serial_port()
        pozyx = pypozyx.PozyxSerial(serial_port)
     # BKP-> pozyx = pypozyx.PozyxSerial(pypozyx.get_serial_ports()[0].device)
    except:
        rospy.loginfo("Pozyx not connected")
        return
    while not rospy.is_shutdown():
        coords = pypozyx.Coordinates()
        pozyx.doPositioning(coords, remote_id=remote_id)
        rospy.loginfo(coords)
        #pub.publish(Point32(coords.x, coords.y, coords.z))
        #pub.publish(Point(coords.x, coords.y, coords.z))
        pub.publish(Point(coords.x/1000.0, coords.y/1000.0, coords.z/1000.0))
        pub1.publish(Point(coords.x/1000.0, coords.y/1000.0, coords.z/1000.0))


if __name__ == '__main__':
    try:
        pozyx_positioning_pub()
    except rospy.ROSInterruptException:
        pass
