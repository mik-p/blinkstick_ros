import time
from blinkstick import blinkstick


# get info
def get_info(leds):
    for bstick in leds:
        print("Found device:")
        print("    Manufacturer:  " + bstick.get_manufacturer())
        print("    Description:   " + bstick.get_description())
        print("    Serial:        " + bstick.get_serial())
        print("    Current Color: " + bstick.get_color(color_format="hex"))
        print("    Info Block 1:  " + bstick.get_info_block1())
        print("    Info Block 2:  " + bstick.get_info_block2())
        print("    Mode:          " + str(bstick.get_mode()))


# led = blinkstick.find_first()
led = blinkstick.find_all()
print(led)

get_info(led)

if led is None:
    print("BlinkStick not found...\n\nExiting...")
else:
    for l in led:
        # wsxxx mode
        l.set_mode(2)
        time.sleep(0.01)

        l.set_color(index=0, name="green")
        time.sleep(0.01)
        l.set_color(index=1, name="green")
        time.sleep(1)

        l.set_color(index=0, hex="#ff00ff")
        time.sleep(0.01)
        l.set_color(index=1, hex="#ff00ff")
        time.sleep(0.01)
        print(l.get_serial() + " " + l.get_color(color_format="hex"))
        time.sleep(1)

        # l.turn_off()
