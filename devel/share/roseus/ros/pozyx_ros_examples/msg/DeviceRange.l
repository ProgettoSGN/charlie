;; Auto-generated. Do not edit!


(when (boundp 'pozyx_ros_examples::DeviceRange)
  (if (not (find-package "POZYX_ROS_EXAMPLES"))
    (make-package "POZYX_ROS_EXAMPLES"))
  (shadow 'DeviceRange (find-package "POZYX_ROS_EXAMPLES")))
(unless (find-package "POZYX_ROS_EXAMPLES::DEVICERANGE")
  (make-package "POZYX_ROS_EXAMPLES::DEVICERANGE"))

(in-package "ROS")
;;//! \htmlinclude DeviceRange.msg.html


(defclass pozyx_ros_examples::DeviceRange
  :super ros::object
  :slots (_timestamp _distance _RSS ))

(defmethod pozyx_ros_examples::DeviceRange
  (:init
   (&key
    ((:timestamp __timestamp) 0)
    ((:distance __distance) 0)
    ((:RSS __RSS) 0)
    )
   (send-super :init)
   (setq _timestamp (round __timestamp))
   (setq _distance (round __distance))
   (setq _RSS (round __RSS))
   self)
  (:timestamp
   (&optional __timestamp)
   (if __timestamp (setq _timestamp __timestamp)) _timestamp)
  (:distance
   (&optional __distance)
   (if __distance (setq _distance __distance)) _distance)
  (:RSS
   (&optional __RSS)
   (if __RSS (setq _RSS __RSS)) _RSS)
  (:serialization-length
   ()
   (+
    ;; uint32 _timestamp
    4
    ;; uint32 _distance
    4
    ;; int16 _RSS
    2
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint32 _timestamp
       (write-long _timestamp s)
     ;; uint32 _distance
       (write-long _distance s)
     ;; int16 _RSS
       (write-word _RSS s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint32 _timestamp
     (setq _timestamp (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; uint32 _distance
     (setq _distance (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int16 _RSS
     (setq _RSS (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;;
   self)
  )

(setf (get pozyx_ros_examples::DeviceRange :md5sum-) "5e707b9b9136043c8fb64f18e44f685a")
(setf (get pozyx_ros_examples::DeviceRange :datatype-) "pozyx_ros_examples/DeviceRange")
(setf (get pozyx_ros_examples::DeviceRange :definition-)
      "uint32 timestamp
uint32 distance
int16 RSS

")



(provide :pozyx_ros_examples/DeviceRange "5e707b9b9136043c8fb64f18e44f685a")


