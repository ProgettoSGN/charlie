; Auto-generated. Do not edit!


(cl:in-package pozyx_ros-msg)


;//! \htmlinclude DeviceRange.msg.html

(cl:defclass <DeviceRange> (roslisp-msg-protocol:ros-message)
  ((timestamp
    :reader timestamp
    :initarg :timestamp
    :type cl:integer
    :initform 0)
   (distance
    :reader distance
    :initarg :distance
    :type cl:integer
    :initform 0)
   (RSS
    :reader RSS
    :initarg :RSS
    :type cl:fixnum
    :initform 0))
)

(cl:defclass DeviceRange (<DeviceRange>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <DeviceRange>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'DeviceRange)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name pozyx_ros-msg:<DeviceRange> is deprecated: use pozyx_ros-msg:DeviceRange instead.")))

(cl:ensure-generic-function 'timestamp-val :lambda-list '(m))
(cl:defmethod timestamp-val ((m <DeviceRange>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader pozyx_ros-msg:timestamp-val is deprecated.  Use pozyx_ros-msg:timestamp instead.")
  (timestamp m))

(cl:ensure-generic-function 'distance-val :lambda-list '(m))
(cl:defmethod distance-val ((m <DeviceRange>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader pozyx_ros-msg:distance-val is deprecated.  Use pozyx_ros-msg:distance instead.")
  (distance m))

(cl:ensure-generic-function 'RSS-val :lambda-list '(m))
(cl:defmethod RSS-val ((m <DeviceRange>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader pozyx_ros-msg:RSS-val is deprecated.  Use pozyx_ros-msg:RSS instead.")
  (RSS m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <DeviceRange>) ostream)
  "Serializes a message object of type '<DeviceRange>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'timestamp)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'timestamp)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'timestamp)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'timestamp)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'distance)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'distance)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'distance)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'distance)) ostream)
  (cl:let* ((signed (cl:slot-value msg 'RSS)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 65536) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <DeviceRange>) istream)
  "Deserializes a message object of type '<DeviceRange>"
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'timestamp)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'timestamp)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'timestamp)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'timestamp)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'distance)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'distance)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'distance)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'distance)) (cl:read-byte istream))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'RSS) (cl:if (cl:< unsigned 32768) unsigned (cl:- unsigned 65536))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<DeviceRange>)))
  "Returns string type for a message object of type '<DeviceRange>"
  "pozyx_ros/DeviceRange")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'DeviceRange)))
  "Returns string type for a message object of type 'DeviceRange"
  "pozyx_ros/DeviceRange")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<DeviceRange>)))
  "Returns md5sum for a message object of type '<DeviceRange>"
  "5e707b9b9136043c8fb64f18e44f685a")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'DeviceRange)))
  "Returns md5sum for a message object of type 'DeviceRange"
  "5e707b9b9136043c8fb64f18e44f685a")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<DeviceRange>)))
  "Returns full string definition for message of type '<DeviceRange>"
  (cl:format cl:nil "uint32 timestamp~%uint32 distance~%int16 RSS~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'DeviceRange)))
  "Returns full string definition for message of type 'DeviceRange"
  (cl:format cl:nil "uint32 timestamp~%uint32 distance~%int16 RSS~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <DeviceRange>))
  (cl:+ 0
     4
     4
     2
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <DeviceRange>))
  "Converts a ROS message object to a list"
  (cl:list 'DeviceRange
    (cl:cons ':timestamp (timestamp msg))
    (cl:cons ':distance (distance msg))
    (cl:cons ':RSS (RSS msg))
))
