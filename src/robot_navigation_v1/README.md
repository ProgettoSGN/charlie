## Package summary

- robot_navigation 
    - [launch]
    - [maps]
        - replace to your map in this folder
    - [param]
        - files for move_base parameters 
    - [rviz]
        - rviz setting
    - [scripts]
        - python scripts
    - [urdf]
        - robot.urdf.xacro (turtlebot3 urdf for test)
        - [custom_robot]
            - your robot descriptions
        

---
### background
In order to navigate a robot, we will need 4 basic topics:
1. /cmd_vel
    - this topic will be used to control the motor of the robot and will be used by [move_base](http://wiki.ros.org/move_base)
2. /scan
    - this topic will be used by AMCL for localization 
3. /odom
    - this is a standart topic in ROS to know the position of the robot which requires robot descriptions and TF

---

### Publish Odom message
> rosrun robot_navigation position_euler_pub.py 

I have modified based on your previous python file to publish the odom message.
The /Odom message will be used for fetching the robot current pose and `move_base` to navigate the robot 

---

## Test your laser scan with amcl 
**Note1:** Please copy your map data to the `maps' folder


**Note2:** Please make sure you have enable your robot description  
In `robot_remote.launch`, Disable `Line 5` & Enable `Line 7`

Step 1:
> bring up your hardware robot and sensors

Step 2:
> roslaunch robot_navigation robot_amcl_test.launch

In `robot_amcl_test.launch` it will roslaunch `robot_remote.launch` which read in your robot URDF and publish transformation info under the rostopic `/tf`

AMCL will used the transformation information, map info and laser data in `/scan` topic for localization 

---

### To navigate your robot 
**prerequisite** : you need to have `/cmd_vel` topic to allow `move_base` to control and navigate your robot

Step 1:
> bring up your hardware robot and sensors

Step 2:
> roslaunch robot_navigation robot_navigation.launch

Step 3:
> rosrun robot_navigation move_base_simple.py


