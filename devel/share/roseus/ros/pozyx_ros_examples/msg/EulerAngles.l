;; Auto-generated. Do not edit!


(when (boundp 'pozyx_ros_examples::EulerAngles)
  (if (not (find-package "POZYX_ROS_EXAMPLES"))
    (make-package "POZYX_ROS_EXAMPLES"))
  (shadow 'EulerAngles (find-package "POZYX_ROS_EXAMPLES")))
(unless (find-package "POZYX_ROS_EXAMPLES::EULERANGLES")
  (make-package "POZYX_ROS_EXAMPLES::EULERANGLES"))

(in-package "ROS")
;;//! \htmlinclude EulerAngles.msg.html


(defclass pozyx_ros_examples::EulerAngles
  :super ros::object
  :slots (_yaw _roll _pitch ))

(defmethod pozyx_ros_examples::EulerAngles
  (:init
   (&key
    ((:yaw __yaw) 0.0)
    ((:roll __roll) 0.0)
    ((:pitch __pitch) 0.0)
    )
   (send-super :init)
   (setq _yaw (float __yaw))
   (setq _roll (float __roll))
   (setq _pitch (float __pitch))
   self)
  (:yaw
   (&optional __yaw)
   (if __yaw (setq _yaw __yaw)) _yaw)
  (:roll
   (&optional __roll)
   (if __roll (setq _roll __roll)) _roll)
  (:pitch
   (&optional __pitch)
   (if __pitch (setq _pitch __pitch)) _pitch)
  (:serialization-length
   ()
   (+
    ;; float32 _yaw
    4
    ;; float32 _roll
    4
    ;; float32 _pitch
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _yaw
       (sys::poke _yaw (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _roll
       (sys::poke _roll (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _pitch
       (sys::poke _pitch (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _yaw
     (setq _yaw (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _roll
     (setq _roll (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _pitch
     (setq _pitch (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get pozyx_ros_examples::EulerAngles :md5sum-) "a95abc59ede2a93c5088a3b41defbc41")
(setf (get pozyx_ros_examples::EulerAngles :datatype-) "pozyx_ros_examples/EulerAngles")
(setf (get pozyx_ros_examples::EulerAngles :definition-)
      "float32 yaw
float32 roll
float32 pitch

")



(provide :pozyx_ros_examples/EulerAngles "a95abc59ede2a93c5088a3b41defbc41")


