#ifndef MYSERIAL_ROS_H
#define MYSERIAL_ROS_H

// other includes
#include "ros/ros.h"
#include "std_msgs/String.h"
#include "std_msgs/Int32.h"
#include "std_msgs/Float64.h"
#include <geometry_msgs/Point.h>
#include <geometry_msgs/Pose.h>
#include "geometry_msgs/PoseStamped.h"

#define HEADER_A 26
#define HEADER_B 27
#define PAYLOAD_POSE 44

union D{
	    char   s[4];
	    float  n;
	    } d;
	    
typedef enum{
    HEADER_1,
    HEADER_2,
    ID,
    wait_PAYLOAD,
} state;
state state_msg;

int serial_port;


// front/back position
double pos_x_f;
double pos_y_f;
double pos_z_f; 

double pos_x_b;
double pos_y_b;
double pos_z_b;

// start and stop
double startstop;

// waypoint to reach
double way_x;
double way_y;
double way_z;

// robot current pose
double robot_pose_x;
double robot_pose_y;
double robot_pose_z;

// receive message
double heading;
bool new_message_available;
geometry_msgs::Point h_angle;

int serial_init(void);
void Pose_cb_forward(const geometry_msgs::PoseStamped::ConstPtr&);
void Pose_cb_back(const geometry_msgs::PoseStamped::ConstPtr&);
void start_and_stop_cb(const std_msgs::Float64::ConstPtr&);
void waypoint_cb(const geometry_msgs::Point::ConstPtr&);
void robot_pose_cb(const geometry_msgs::Point::ConstPtr&);

// reading functions
void read_from_serial(void);
void decode_payload(void);
void parser_mess(unsigned char buffer);



#endif
