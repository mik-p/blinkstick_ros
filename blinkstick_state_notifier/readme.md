blinksitck_state_notifier
===

ROS driver for blinkstick to use a visual notification tool

install
---

```bash
# install python package
sudo pip install blinkstick
# sudo pip install -r requirements.txt

# as root add a usb rule
sudo echo "SUBSYSTEM==\"usb\", ATTR{idVendor}==\"20a0\", ATTR{idProduct}==\"41e5\", MODE:=\"0666\"" | sudo tee /etc/udev/rules.d/85-blinkstick.rules

# reload rules
sudo udevadm control --reload
sudo udevadm trigger
```
