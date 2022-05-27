cmake_minimum_required(VERSION 2.8.3)
project(blinkstick_state_notifier)

# find packages
find_package(catkin REQUIRED COMPONENTS
    rospy
    led_notify_msgs
)

# catkin_python_setup()
