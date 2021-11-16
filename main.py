#!/usr/bin/python
"""*****************************************************************************************************************
    DropPi by Kim Dalmeijer, 2021

    Relay board 0: valve relays [VALVE1, VALVE2, VALVE3, VALVE4]
    Relay board 1: flash and camera relays [CAM, FLASH1, FLASH2, FLASH3]
********************************************************************************************************************"""
from __future__ import print_function

import sys
import time

from DropPi_lib import *

# Definitions of relays on board 0
VALVE_1 = 0
VALVE_2 = 1
VALVE_3 = 2
VALVE_4 = 3

# Definitions of relays on board 1
CAM = 4
FLASH_1 = 5
FLASH_2 = 6
FLASH_3 = 7

# General Definitions
DEF_FLASH_DELAY = 16  # (ms)
DEF_CAM_DELAY = 16  # (ms)

timings = [["a", 2], ["b", 1], ["c", 0]]


def process_loop():
    # turn all of the relays on
    # relay_all_on(0)
    # wait a second
    # time.sleep(0.5)
    # relay_all_on(1)
    # time.sleep(1)
    # turn all of the relays off
    # relay_all_off(0)
    # time.sleep(0.5)
    # relay_all_off(1)
    # wait a second
    # time.sleep(1)

    # now cycle each relay every second in an infinite loop
    while True:
        for i in range(1, 9):
            relay_on(i)
            time.sleep(0.005)
            relay_off(i)
            time.sleep(0.2)


# Now see what we're supposed to do next
if __name__ == "__main__":
    try:
        process_loop()
    except KeyboardInterrupt:
        # tell the user what we're doing...
        print("\nExiting application")
        # turn off all of the relays
        relay_all_off()
        relay_all_off()
        # exit the application
        sys.exit(0)
