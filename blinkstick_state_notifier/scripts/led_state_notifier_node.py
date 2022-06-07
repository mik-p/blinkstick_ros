#!/usr/bin/env python3

import rospy
from blinkstick import blinkstick
from led_notify_msgs.msg import LEDRGBA
from led_notify_msgs.msg import LEDNotify


class BlinkStickHandler(object):
    def __init__(self):
        # get a blinkstick led
        self.led = blinkstick.find_first()

        # safe delay time
        self.comm_delay_rate = rospy.Rate(1.0 / rospy.Duration(0.1).to_sec())

        # not connected
        if self.led is not None:
            # set the mode to 2
            self.comm_delay_rate.sleep()
            self.led.set_mode(2)
            # show info
            self.comm_delay_rate.sleep()
            self.get_info()
            # start some colour
            self.comm_delay_rate.sleep()
            self.show_unused()

    # get info
    def get_info(self):
        rospy.loginfo("Found device:")
        rospy.loginfo("Manufacturer:  " + self.led.get_manufacturer())
        rospy.loginfo("Description:   " + self.led.get_description())
        rospy.loginfo("Serial:        " + self.led.get_serial())
        rospy.loginfo("Current Color: " +
                      self.led.get_color(color_format="hex"))
        rospy.loginfo("Info Block 1:  " + self.led.get_info_block1())
        rospy.loginfo("Info Block 2:  " + self.led.get_info_block2())
        rospy.loginfo("Mode:          " + str(self.led.get_mode()))

    # safer command handler
    def _set_colour_w_safe_delay(self, r=0, g=0, b=0):
        # delay making a command to avoid usb issue
        self.comm_delay_rate.sleep()
        # do colour command
        self.led.set_color(index=0, red=r, green=g, blue=b)
        # the other side
        self.comm_delay_rate.sleep()
        self.led.set_color(index=1, red=r, green=g, blue=b)

    # show unused
    def show_unused(self):
        rospy.logdebug("unused")
        self._set_colour_w_safe_delay(255, 0, 255)

    # show idle colour
    def show_idle(self):
        rospy.logdebug("idle")
        self._set_colour_w_safe_delay(
            LEDRGBA.BLUE_R, LEDRGBA.BLUE_G, LEDRGBA.BLUE_B)

    # show success colour
    def show_success(self):
        rospy.logdebug("success")
        self._set_colour_w_safe_delay(
            LEDRGBA.GREEN_R, LEDRGBA.GREEN_G, LEDRGBA.GREEN_B)

    # show warning colour
    def show_warning(self):
        rospy.logdebug("warning")
        self._set_colour_w_safe_delay(
            LEDRGBA.YELLOW_R, LEDRGBA.YELLOW_G, LEDRGBA.YELLOW_B)

    # show error colour
    def show_error(self):
        rospy.logdebug("error")
        self._set_colour_w_safe_delay(
            LEDRGBA.RED_R, LEDRGBA.RED_G, LEDRGBA.RED_B)

    # show error colour
    def show_on(self):
        rospy.logdebug("error")
        self._set_colour_w_safe_delay(
            LEDRGBA.RED_R, LEDRGBA.GREEN_G, LEDRGBA.BLUE_B)


class LEDStateNotifier(BlinkStickHandler):
    def __init__(self):
        BlinkStickHandler.__init__(self)

        # queue of led notification commands
        self.notice_queue = []

        # subscribe to led notifications
        self.notification_sub = rospy.Subscriber(
            "~notification", LEDNotify, self.led_notification_cb)

        # create a timer to pop the notification queue
        self.notification_pop_rate = rospy.get_param(
            "~notification_pop_rate", 2.0)

        pop_rate_period = rospy.Rate(self.notification_pop_rate).sleep_dur
        self.notification_timer = rospy.Timer(
            pop_rate_period, self.pop_notice_queue_timer_cb)

    # execute a notification request
    def do_notification(self, note):
        # what kind of notification is it
        if note.alert == LEDNotify.IDLE:
            self.show_idle()
        elif note.alert == LEDNotify.SUCCESS:
            self.show_success()
        elif note.alert == LEDNotify.WARNING:
            self.show_warning()
        elif note.alert == LEDNotify.ERROR:
            self.show_error()
        else:
            self.show_on()  # probably white

    # pop queued requests
    def pop_notice_queue_timer_cb(self, event):
        # any messages then pop them as ready
        if self.notice_queue:
            notification = self.notice_queue.pop(0)

            self.do_notification(notification)

    # receive led notification messages
    def led_notification_cb(self, msg):
        # get to it later in timer callback
        self.notice_queue.append(msg)


# main
if __name__ == '__main__':
    rospy.init_node('led_state_notifier_node')

    server = LEDStateNotifier()
    rospy.spin()
