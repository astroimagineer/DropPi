#!/usr/bin/python
"""*****************************************************************************************************************
    DropPi by Kim Dalmeijer, 2021

    Relay board 0: valve relays [VALVE1, VALVE2, VALVE3, VALVE4]
    Relay board 1: flash and camera relays [CAM, FLASH1, FLASH2, FLASH3]
********************************************************************************************************************"""
from __future__ import print_function
import logging
import sys
import time
import ctypes
import threading
from DropPi_lib import *

# Load libc shared library:
libc = ctypes.CDLL('libc.so.6')

# Definitions of relays on board 0
VALVE_1 = 1
VALVE_2 = 3
VALVE_3 = 2
VALVE_4 = 4

# Definitions of relays on board 1
CAMERA = 5
FLASH_1 = 7
FLASH_2 = 6
FLASH_3 = 8

# General Definitions
DEF_FLASH_DELAY = 30  # (ms)
DEF_CAMERA_DELAY = 2500  # (ms)

MIRROR_LOCKUP = True

# Definitions of timings, these are defaults which will be set with the GUI before execution of the firing process
# Each timing consists of the starttime in ms, and the duration in ms. Valve timings have 4 slots (4 drops).
# Camera and flash timings have a single slot
# Timings for VALVE_1
TIMES_VALVE_1 = list()
TIMES_VALVE_2 = list()
TIMES_VALVE_3 = list()
TIMES_VALVE_4 = list()

TIME_CAMERA = 100
TIME_FLASH = ''

# placeholders for elapsed thread times
v1_elapsed_time = 0
v2_elapsed_time = 0
v3_elapsed_time = 0
v4_elapsed_time = 0
c_elapsed_time = 0
f_elapsed_time = 0


def delayus(us):
    """ Delay microseconds with libc usleep() using ctypes. """
    libc.usleep(int(us))
# ------------------------------------


def thread_valve_1_function(name):
    global v1_elapsed_time
    start_time = time.perf_counter()
    if MIRROR_LOCKUP:
        delayus(700 * 1000)
    for i in range(len(TIMES_VALVE_1)):
        delayus(int(TIMES_VALVE_1[i][0]) * 1000)
        relay_on(VALVE_1)
        delayus(int(TIMES_VALVE_1[i][1]) * 1000)
        relay_off(VALVE_1)
    v1_elapsed_time = time.perf_counter() - start_time


def thread_valve_2_function(name):
    global v2_elapsed_time
    start_time = time.perf_counter()
    if MIRROR_LOCKUP:
        delayus(700 * 1000)
    for i in range(len(TIMES_VALVE_2)):
        delayus(int(TIMES_VALVE_2[i][0]) * 1000)
        relay_on(VALVE_2)
        delayus(int(TIMES_VALVE_2[i][1]) * 1000)
        relay_off(VALVE_2)
    v2_elapsed_time = time.perf_counter() - start_time


def thread_valve_3_function(name):
    global v3_elapsed_time
    start_time = time.perf_counter()
    if MIRROR_LOCKUP:
        delayus(700 * 1000)
    for i in range(len(TIMES_VALVE_3)):
        delayus(int(TIMES_VALVE_3[i][0]) * 1000)
        relay_on(VALVE_3)
        delayus(int(TIMES_VALVE_3[i][1]) * 1000)
        relay_off(VALVE_3)
    v3_elapsed_time = time.perf_counter() - start_time


def thread_valve_4_function(name):
    global v4_elapsed_time
    start_time = time.perf_counter()
    if MIRROR_LOCKUP:
        delayus(700 * 1000)
    for i in range(len(TIMES_VALVE_4)):
        delayus(int(TIMES_VALVE_4[i][0]) * 1000)
        relay_on(VALVE_4)
        delayus(int(TIMES_VALVE_4[i][1]) * 1000)
        relay_off(VALVE_4)
    v4_elapsed_time = time.perf_counter() - start_time


def thread_camera_function(name):
    global c_elapsed_time
    start_time = time.perf_counter()
    if MIRROR_LOCKUP:
        relay_on(CAMERA)
        delayus(150 * 1000)
        relay_off(CAMERA)
        delayus(550 * 1000)
    delayus(TIME_CAMERA * 1000)
    relay_on(CAMERA)
    delayus(DEF_CAMERA_DELAY * 1000)
    relay_off(CAMERA)
    c_elapsed_time = time.perf_counter() - start_time


def thread_flash_function(name, flash1, flash2, flash3):
    global f_elapsed_time
    start_time = time.perf_counter()
    if MIRROR_LOCKUP:
        delayus(700 * 1000)
    delayus(int(TIME_FLASH) * 1000)
    if flash1:
        relay_on(FLASH_1)
    if flash2:
        relay_on(FLASH_2)
    if flash3:
        relay_on(FLASH_3)
    delayus(DEF_FLASH_DELAY * 1000)
    if flash1:
        relay_off(FLASH_1)
    if flash2:
        relay_off(FLASH_2)
    if flash3:
        relay_off(FLASH_3)
    f_elapsed_time = time.perf_counter() - start_time


def main(**kwargs):
    # do whatever and return 0 for success and an
    # integer x, 1 <= x <= 256 for failure
    logformat = '%(asctime)s.%(msecs)03d %(message)s'
    logging.basicConfig(format=logformat, level=logging.INFO, datefmt='%H:%M:%S')

    # set variables for this run from what the main has passed
    global DEF_FLASH_DELAY
    global DEF_CAMERA_DELAY
    global TIME_CAMERA
    global TIME_FLASH
    global TIMES_VALVE_1
    global TIMES_VALVE_2
    global TIMES_VALVE_3
    global TIMES_VALVE_4
    global MIRROR_LOCKUP
    global v1_elapsed_time
    global v2_elapsed_time
    global v3_elapsed_time
    global v4_elapsed_time
    global c_elapsed_time
    global f_elapsed_time

    DEF_FLASH_DELAY = int(kwargs['flash_def'])
    logging.info("FLASH DELAY: %i", DEF_FLASH_DELAY)
    DEF_CAMERA_DELAY = int(kwargs['cam_def'])
    logging.info("CAMERA DELAY: %i", DEF_CAMERA_DELAY)
    TIME_CAMERA = int(kwargs['cam_on'])
    logging.info("CAMERA TIME: %i", TIME_CAMERA)
    TIME_FLASH = int(kwargs['flash_on'])
    logging.info("FLASH TIME: %i", TIME_FLASH)

    MIRROR_LOCKUP = kwargs['mirror']
    TIMES_VALVE_1 = kwargs['v1times']
    TIMES_VALVE_2 = kwargs['v2times']
    TIMES_VALVE_3 = kwargs['v3times']
    TIMES_VALVE_4 = kwargs['v4times']

    logging.info("DropPi    : before creating threads")
    thread_valve_1 = threading.Thread(target=thread_valve_1_function, args=("valve1",))
    thread_valve_2 = threading.Thread(target=thread_valve_2_function, args=("valve2",))
    thread_valve_3 = threading.Thread(target=thread_valve_3_function, args=("valve3",))
    thread_valve_4 = threading.Thread(target=thread_valve_4_function, args=("valve4",))
    thread_camera = threading.Thread(target=thread_camera_function, args=("camera",))
    thread_flash = threading.Thread(target=thread_flash_function, args=("flash", kwargs['flash1_on'], kwargs['flash2_on'], kwargs['flash3_on']))

    logging.info("DropPi    : before running threads")
    thread_camera.start()
    thread_valve_1.start()
    thread_valve_2.start()
    thread_valve_3.start()
    thread_valve_4.start()
    thread_flash.start()

    logging.info("DropPi    : waiting for all threads to finish")
    thread_camera.join()
    thread_valve_1.join()
    thread_valve_2.join()
    thread_valve_3.join()
    thread_valve_4.join()
    thread_flash.join()
    logging.info("DropPi    : all done")

    # calculate error from elapsed times and display results to indicate how trustworthy the app runs
    # if an elapsed time is zero, the valve of flash for that time was not used

    # V1 ERROR CALCULATION
    calculated_elapsed_time = 0
    if v1_elapsed_time != 0:
        if MIRROR_LOCKUP:
            calculated_elapsed_time += 700
        for i in range(len(TIMES_VALVE_1)):
            calculated_elapsed_time += int(TIMES_VALVE_1[i][0])
            calculated_elapsed_time += int(TIMES_VALVE_1[i][1])
        calculated_elapsed_time = calculated_elapsed_time / 1000
        try:
            calculated_error = ((calculated_elapsed_time - v1_elapsed_time) / calculated_elapsed_time) * 100
        except ZeroDivisionError:
            calculated_error = 0
        logging.info(f'V1 timing error: real; {v1_elapsed_time:.4f}, calculated; {calculated_elapsed_time}, error; {abs(calculated_error):.1f}%')

    # V2 ERROR CALCULATION
    calculated_elapsed_time = 0
    if v2_elapsed_time != 0:
        if MIRROR_LOCKUP:
            calculated_elapsed_time += 700
        for i in range(len(TIMES_VALVE_2)):
            calculated_elapsed_time += int(TIMES_VALVE_2[i][0])
            calculated_elapsed_time += int(TIMES_VALVE_2[i][1])
        calculated_elapsed_time = calculated_elapsed_time / 1000
        try:
            calculated_error = ((calculated_elapsed_time - v2_elapsed_time) / calculated_elapsed_time) * 100
        except ZeroDivisionError:
            calculated_error = 0
        logging.info(f'V2 timing error: real; {v2_elapsed_time:.4f}, calculated; {calculated_elapsed_time}, error; {abs(calculated_error):.1f}%')

    # V3 ERROR CALCULATION
    calculated_elapsed_time = 0
    if v3_elapsed_time != 0:
        if MIRROR_LOCKUP:
            calculated_elapsed_time += 700
        for i in range(len(TIMES_VALVE_3)):
            calculated_elapsed_time += int(TIMES_VALVE_3[i][0])
            calculated_elapsed_time += int(TIMES_VALVE_3[i][1])
        calculated_elapsed_time = calculated_elapsed_time / 1000
        try:
            calculated_error = ((calculated_elapsed_time - v3_elapsed_time) / calculated_elapsed_time) * 100
        except ZeroDivisionError:
            calculated_error = 0
        logging.info(
            f'V3 timing error: real; {v3_elapsed_time:.4f}, calculated; {calculated_elapsed_time}, error; {abs(calculated_error):.1f}%')

    # V4 ERROR CALCULATION
    calculated_elapsed_time = 0
    if v4_elapsed_time != 0:
        if MIRROR_LOCKUP:
            calculated_elapsed_time += 700
        for i in range(len(TIMES_VALVE_4)):
            calculated_elapsed_time += int(TIMES_VALVE_4[i][0])
            calculated_elapsed_time += int(TIMES_VALVE_4[i][1])
        calculated_elapsed_time = calculated_elapsed_time / 1000
        try:
            calculated_error = ((calculated_elapsed_time - v4_elapsed_time) / calculated_elapsed_time) * 100
        except ZeroDivisionError:
            calculated_error = 0
        logging.info(
            f'V4 timing error: real; {v4_elapsed_time:.4f}, calculated; {calculated_elapsed_time}, error; {abs(calculated_error):.1f}%')

    # CAMERA ERROR CALCULATION
    calculated_elapsed_time = 0
    if c_elapsed_time != 0:
        if MIRROR_LOCKUP:
            calculated_elapsed_time += 700
        calculated_elapsed_time += int(TIME_CAMERA)
        calculated_elapsed_time += int(DEF_CAMERA_DELAY)
        calculated_elapsed_time = calculated_elapsed_time / 1000
        try:
            calculated_error = ((calculated_elapsed_time - c_elapsed_time) / calculated_elapsed_time) * 100
        except ZeroDivisionError:
            calculated_error = 0
        logging.info(
            f'C timing error: real; {c_elapsed_time:.4f}, calculated; {calculated_elapsed_time}, error; {abs(calculated_error):.1f}%')

    # FLASH ERROR CALCULATION
    calculated_elapsed_time = 0
    if f_elapsed_time != 0:
        if MIRROR_LOCKUP:
            calculated_elapsed_time += 700
        calculated_elapsed_time += int(TIME_FLASH)
        calculated_elapsed_time += int(DEF_FLASH_DELAY)
        calculated_elapsed_time = calculated_elapsed_time / 1000
        try:
            calculated_error = ((calculated_elapsed_time - f_elapsed_time) / calculated_elapsed_time) * 100
        except ZeroDivisionError:
            calculated_error = 0
        logging.info(
            f'F timing error: real; {f_elapsed_time:.4f}, calculated; {calculated_elapsed_time}, error; {abs(calculated_error):.1f}%')

    return 0


# Now see what we're supposed to do next
if __name__ == "__main__":
    sys.exit(main())
