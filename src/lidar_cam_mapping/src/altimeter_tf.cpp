#include "ros/ros.h"
#include "tf/transform_broadcaster.h"
#include "sensor_msgs/Range.h"

std::string p_base_stabilized_frame_;
std::string p_base_footprint_frame_;
tf::TransformBroadcaster* tfB_;
tf::StampedTransform transform_;
tf::Quaternion tmp_;

//mi servono se voglio aggiungere delle rotazioni
#ifndef TF_MATRIX3x3_H
  typedef btScalar tfScalar;
  namespace tf { typedef btMatrix3x3 Matrix3x3; }
#endif

void MsgCallback(const sensor_msgs::Range& msg)
{
//rotazioni
  tmp_.setRPY(0.0, 0.0, 0.0);
  transform_.setRotation(tmp_);
//traslazioni
  transform_.setOrigin(tf::Vector3(0.0, 0.0, msg.range));
  transform_.stamp_ = msg.header.stamp;

  tfB_->sendTransform(transform_);
}

int main(int argc, char **argv) {
  ros::init(argc, argv, ROS_PACKAGE_NAME);

  ros::NodeHandle n;
  ros::NodeHandle pn("~");

  pn.param("base_stabilized_frame", p_base_stabilized_frame_, std::string("base_stabilized"));
  pn.param("base_footprint_frame", p_base_footprint_frame_, std::string("base_footprint"));
  
  tfB_ = new tf::TransformBroadcaster();

  transform_.frame_id_ = p_base_footprint_frame_;
  transform_.child_frame_id_ = p_base_stabilized_frame_;

  ros::Subscriber subscriber = n.subscribe("range_topic", 10, MsgCallback);

  ros::spin();

  delete tfB_;

  return 0;
}
