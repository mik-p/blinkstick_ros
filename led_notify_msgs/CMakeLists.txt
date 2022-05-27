cmake_minimum_required(VERSION 2.8.3)
project(led_notify_msgs)

find_package(catkin REQUIRED COMPONENTS
  std_msgs
  message_generation
)

add_message_files(
  FILES
  LEDRGBA.msg
  LEDNotify.msg
)

# add_service_files(
#   FILES
# )

generate_messages(
  DEPENDENCIES
  std_msgs
)

catkin_package(CATKIN_DEPENDS message_runtime std_msgs)
