# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "pozyx_ros_examples: 2 messages, 0 services")

set(MSG_I_FLAGS "-Ipozyx_ros_examples:/home/robot/charlie_ws/src/pozyx_ros_examples/msg;-Istd_msgs:/opt/ros/kinetic/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(pozyx_ros_examples_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/robot/charlie_ws/src/pozyx_ros_examples/msg/DeviceRange.msg" NAME_WE)
add_custom_target(_pozyx_ros_examples_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "pozyx_ros_examples" "/home/robot/charlie_ws/src/pozyx_ros_examples/msg/DeviceRange.msg" ""
)

get_filename_component(_filename "/home/robot/charlie_ws/src/pozyx_ros_examples/msg/EulerAngles.msg" NAME_WE)
add_custom_target(_pozyx_ros_examples_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "pozyx_ros_examples" "/home/robot/charlie_ws/src/pozyx_ros_examples/msg/EulerAngles.msg" ""
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(pozyx_ros_examples
  "/home/robot/charlie_ws/src/pozyx_ros_examples/msg/DeviceRange.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/pozyx_ros_examples
)
_generate_msg_cpp(pozyx_ros_examples
  "/home/robot/charlie_ws/src/pozyx_ros_examples/msg/EulerAngles.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/pozyx_ros_examples
)

### Generating Services

### Generating Module File
_generate_module_cpp(pozyx_ros_examples
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/pozyx_ros_examples
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(pozyx_ros_examples_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(pozyx_ros_examples_generate_messages pozyx_ros_examples_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/robot/charlie_ws/src/pozyx_ros_examples/msg/DeviceRange.msg" NAME_WE)
add_dependencies(pozyx_ros_examples_generate_messages_cpp _pozyx_ros_examples_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/robot/charlie_ws/src/pozyx_ros_examples/msg/EulerAngles.msg" NAME_WE)
add_dependencies(pozyx_ros_examples_generate_messages_cpp _pozyx_ros_examples_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(pozyx_ros_examples_gencpp)
add_dependencies(pozyx_ros_examples_gencpp pozyx_ros_examples_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS pozyx_ros_examples_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(pozyx_ros_examples
  "/home/robot/charlie_ws/src/pozyx_ros_examples/msg/DeviceRange.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/pozyx_ros_examples
)
_generate_msg_eus(pozyx_ros_examples
  "/home/robot/charlie_ws/src/pozyx_ros_examples/msg/EulerAngles.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/pozyx_ros_examples
)

### Generating Services

### Generating Module File
_generate_module_eus(pozyx_ros_examples
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/pozyx_ros_examples
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(pozyx_ros_examples_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(pozyx_ros_examples_generate_messages pozyx_ros_examples_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/robot/charlie_ws/src/pozyx_ros_examples/msg/DeviceRange.msg" NAME_WE)
add_dependencies(pozyx_ros_examples_generate_messages_eus _pozyx_ros_examples_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/robot/charlie_ws/src/pozyx_ros_examples/msg/EulerAngles.msg" NAME_WE)
add_dependencies(pozyx_ros_examples_generate_messages_eus _pozyx_ros_examples_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(pozyx_ros_examples_geneus)
add_dependencies(pozyx_ros_examples_geneus pozyx_ros_examples_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS pozyx_ros_examples_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(pozyx_ros_examples
  "/home/robot/charlie_ws/src/pozyx_ros_examples/msg/DeviceRange.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/pozyx_ros_examples
)
_generate_msg_lisp(pozyx_ros_examples
  "/home/robot/charlie_ws/src/pozyx_ros_examples/msg/EulerAngles.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/pozyx_ros_examples
)

### Generating Services

### Generating Module File
_generate_module_lisp(pozyx_ros_examples
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/pozyx_ros_examples
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(pozyx_ros_examples_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(pozyx_ros_examples_generate_messages pozyx_ros_examples_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/robot/charlie_ws/src/pozyx_ros_examples/msg/DeviceRange.msg" NAME_WE)
add_dependencies(pozyx_ros_examples_generate_messages_lisp _pozyx_ros_examples_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/robot/charlie_ws/src/pozyx_ros_examples/msg/EulerAngles.msg" NAME_WE)
add_dependencies(pozyx_ros_examples_generate_messages_lisp _pozyx_ros_examples_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(pozyx_ros_examples_genlisp)
add_dependencies(pozyx_ros_examples_genlisp pozyx_ros_examples_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS pozyx_ros_examples_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(pozyx_ros_examples
  "/home/robot/charlie_ws/src/pozyx_ros_examples/msg/DeviceRange.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/pozyx_ros_examples
)
_generate_msg_nodejs(pozyx_ros_examples
  "/home/robot/charlie_ws/src/pozyx_ros_examples/msg/EulerAngles.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/pozyx_ros_examples
)

### Generating Services

### Generating Module File
_generate_module_nodejs(pozyx_ros_examples
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/pozyx_ros_examples
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(pozyx_ros_examples_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(pozyx_ros_examples_generate_messages pozyx_ros_examples_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/robot/charlie_ws/src/pozyx_ros_examples/msg/DeviceRange.msg" NAME_WE)
add_dependencies(pozyx_ros_examples_generate_messages_nodejs _pozyx_ros_examples_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/robot/charlie_ws/src/pozyx_ros_examples/msg/EulerAngles.msg" NAME_WE)
add_dependencies(pozyx_ros_examples_generate_messages_nodejs _pozyx_ros_examples_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(pozyx_ros_examples_gennodejs)
add_dependencies(pozyx_ros_examples_gennodejs pozyx_ros_examples_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS pozyx_ros_examples_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(pozyx_ros_examples
  "/home/robot/charlie_ws/src/pozyx_ros_examples/msg/DeviceRange.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/pozyx_ros_examples
)
_generate_msg_py(pozyx_ros_examples
  "/home/robot/charlie_ws/src/pozyx_ros_examples/msg/EulerAngles.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/pozyx_ros_examples
)

### Generating Services

### Generating Module File
_generate_module_py(pozyx_ros_examples
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/pozyx_ros_examples
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(pozyx_ros_examples_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(pozyx_ros_examples_generate_messages pozyx_ros_examples_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/robot/charlie_ws/src/pozyx_ros_examples/msg/DeviceRange.msg" NAME_WE)
add_dependencies(pozyx_ros_examples_generate_messages_py _pozyx_ros_examples_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/robot/charlie_ws/src/pozyx_ros_examples/msg/EulerAngles.msg" NAME_WE)
add_dependencies(pozyx_ros_examples_generate_messages_py _pozyx_ros_examples_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(pozyx_ros_examples_genpy)
add_dependencies(pozyx_ros_examples_genpy pozyx_ros_examples_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS pozyx_ros_examples_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/pozyx_ros_examples)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/pozyx_ros_examples
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(pozyx_ros_examples_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/pozyx_ros_examples)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/pozyx_ros_examples
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(pozyx_ros_examples_generate_messages_eus std_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/pozyx_ros_examples)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/pozyx_ros_examples
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(pozyx_ros_examples_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/pozyx_ros_examples)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/pozyx_ros_examples
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(pozyx_ros_examples_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/pozyx_ros_examples)
  install(CODE "execute_process(COMMAND \"/usr/bin/python2\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/pozyx_ros_examples\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/pozyx_ros_examples
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(pozyx_ros_examples_generate_messages_py std_msgs_generate_messages_py)
endif()
