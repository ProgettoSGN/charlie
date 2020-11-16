
(cl:in-package :asdf)

(defsystem "pozyx_ros-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "DeviceRange" :depends-on ("_package_DeviceRange"))
    (:file "_package_DeviceRange" :depends-on ("_package"))
    (:file "EulerAngles" :depends-on ("_package_EulerAngles"))
    (:file "_package_EulerAngles" :depends-on ("_package"))
  ))