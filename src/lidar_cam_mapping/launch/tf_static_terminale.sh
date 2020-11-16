#!/bin/bash
source /home/robot/catkin_ws/devel/setup.bash
rosrun tf static_transform_publisher 0 0 0.3 0 0 0 base_footprint base_stabilized 100
read

