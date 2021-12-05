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


def thread_valve_1_function():
    global v1_elapsed_time
    start_time = time.perf_counter()
    if MIRROR_LOCKUP:
        delayus(700 * 1000)
    for i in range(len(TIMES_VALVE_1)):
        delayus(float(TIMES_VALVE_1[i][0]) * 1000)
        relay_on(VALVE_1)
        delayus(float(TIMES_VALVE_1[i][1]) * 1000)
        relay_off(VALVE_1)
    v1_elapsed_time = time.perf_counter() - start_time


def thread_valve_2_function():
    global v2_elapsed_time
    start_time = time.perf_counter()
    if MIRROR_LOCKUP:
        delayus(700 * 1000)
    for i in range(len(TIMES_VALVE_2)):
        delayus(float(TIMES_VALVE_2[i][0]) * 1000)
        relay_on(VALVE_2)
        delayus(float(TIMES_VALVE_2[i][1]) * 1000)
        relay_off(VALVE_2)
    v2_elapsed_time = time.perf_counter() - start_time


def thread_valve_3_function():
    global v3_elapsed_time
    start_time = time.perf_counter()
    if MIRROR_LOCKUP:
        delayus(700 * 1000)
    for i in range(len(TIMES_VALVE_3)):
        delayus(float(TIMES_VALVE_3[i][0]) * 1000)
        relay_on(VALVE_3)
        delayus(float(TIMES_VALVE_3[i][1]) * 1000)
        relay_off(VALVE_3)
    v3_elapsed_time = time.perf_counter() - start_time


def thread_valve_4_function():
    global v4_elapsed_time
    start_time = time.perf_counter()
    if MIRROR_LOCKUP:
        delayus(700 * 1000)
    for i in range(len(TIMES_VALVE_4)):
        delayus(float(TIMES_VALVE_4[i][0]) * 1000)
        relay_on(VALVE_4)
        delayus(float(TIMES_VALVE_4[i][1]) * 1000)
        relay_off(VALVE_4)
    v4_elapsed_time = time.perf_counter() - start_time


def thread_camera_function():
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


def thread_flash_function(flash1, flash2, flash3):
    global f_elapsed_time
    start_time = time.perf_counter()
    # WAIT FOR MIRROR LOCKUP IF NEEDED
    if MIRROR_LOCKUP:
        delayus(700 * 1000)
    # TURN ON
    delayus(float(TIME_FLASH) * 1000)
    if not flash1:
        TMPFLASH_1 = 0
    else:
        TMPFLASH_1 = FLASH_1
    if not flash2:
        TMPFLASH_2 = 0
    else:
        TMPFLASH_2 = FLASH_2
    if not flash3:
        TMPFLASH_3 = 0
    else:
        TMPFLASH_3 = FLASH_3
    relay_on(TMPFLASH_1, TMPFLASH_2, TMPFLASH_3)
    # TURN OFF
    delayus(DEF_FLASH_DELAY * 1000)
    relay_off(TMPFLASH_1, TMPFLASH_2, TMPFLASH_3)
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

    DEF_FLASH_DELAY = float(kwargs['flash_def'])
    logging.info("FLASH DELAY: %i", DEF_FLASH_DELAY)
    DEF_CAMERA_DELAY = float(kwargs['cam_def'])
    logging.info("CAMERA DELAY: %i", DEF_CAMERA_DELAY)
    TIME_CAMERA = float(kwargs['cam_on'])
    logging.info("CAMERA TIME: %i", TIME_CAMERA)
    TIME_FLASH = float(kwargs['flash_on'])
    logging.info("FLASH TIME: %i", TIME_FLASH)

    MIRROR_LOCKUP = kwargs['mirror']
    TIMES_VALVE_1 = kwargs['v1times']
    TIMES_VALVE_2 = kwargs['v2times']
    TIMES_VALVE_3 = kwargs['v3times']
    TIMES_VALVE_4 = kwargs['v4times']

    logging.info("DropPi    : before creating threads")
    thread_valve_1 = threading.Thread(target=thread_valve_1_function)
    thread_valve_2 = threading.Thread(target=thread_valve_2_function)
    thread_valve_3 = threading.Thread(target=thread_valve_3_function)
    thread_valve_4 = threading.Thread(target=thread_valve_4_function)
    thread_camera = threading.Thread(target=thread_camera_function)
    thread_flash = threading.Thread(target=thread_flash_function, args=(
        kwargs['flash1_on'], kwargs['flash2_on'], kwargs['flash3_on']))

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
            calculated_elapsed_time += float(TIMES_VALVE_1[i][0])
            calculated_elapsed_time += float(TIMES_VALVE_1[i][1])
        calculated_elapsed_time = calculated_elapsed_time / 1000
        try:
            calculated_error = ((calculated_elapsed_time - v1_elapsed_time) / calculated_elapsed_time) * 100
        except ZeroDivisionError:
            calculated_error = 0
        logging.info(
            f'Valve1 timings: real; {v1_elapsed_time:.4f},'
            f' calculated; {calculated_elapsed_time},'
            f' error; {abs(calculated_error):.1f}%')

    # V2 ERROR CALCULATION
    calculated_elapsed_time = 0
    if v2_elapsed_time != 0:
        if MIRROR_LOCKUP:
            calculated_elapsed_time += 700
        for i in range(len(TIMES_VALVE_2)):
            calculated_elapsed_time += float(TIMES_VALVE_2[i][0])
            calculated_elapsed_time += float(TIMES_VALVE_2[i][1])
        calculated_elapsed_time = calculated_elapsed_time / 1000
        try:
            calculated_error = ((calculated_elapsed_time - v2_elapsed_time) / calculated_elapsed_time) * 100
        except ZeroDivisionError:
            calculated_error = 0
        logging.info(
            f'Valve2 timings: real; {v2_elapsed_time:.4f},'
            f' calculated; {calculated_elapsed_time},'
            f' error; {abs(calculated_error):.1f}%')

    # V3 ERROR CALCULATION
    calculated_elapsed_time = 0
    if v3_elapsed_time != 0:
        if MIRROR_LOCKUP:
            calculated_elapsed_time += 700
        for i in range(len(TIMES_VALVE_3)):
            calculated_elapsed_time += float(TIMES_VALVE_3[i][0])
            calculated_elapsed_time += float(TIMES_VALVE_3[i][1])
        calculated_elapsed_time = calculated_elapsed_time / 1000
        try:
            calculated_error = ((calculated_elapsed_time - v3_elapsed_time) / calculated_elapsed_time) * 100
        except ZeroDivisionError:
            calculated_error = 0
        logging.info(
            f'Valve3 timings: real; {v3_elapsed_time:.4f},'
            f' calculated; {calculated_elapsed_time},'
            f' error; {abs(calculated_error):.1f}%')

    # V4 ERROR CALCULATION
    calculated_elapsed_time = 0
    if v4_elapsed_time != 0:
        if MIRROR_LOCKUP:
            calculated_elapsed_time += 700
        for i in range(len(TIMES_VALVE_4)):
            calculated_elapsed_time += float(TIMES_VALVE_4[i][0])
            calculated_elapsed_time += float(TIMES_VALVE_4[i][1])
        calculated_elapsed_time = calculated_elapsed_time / 1000
        try:
            calculated_error = ((calculated_elapsed_time - v4_elapsed_time) / calculated_elapsed_time) * 100
        except ZeroDivisionError:
            calculated_error = 0
        logging.info(
            f'Valve4 timings: real; {v4_elapsed_time:.4f},'
            f' calculated; {calculated_elapsed_time},'
            f' error; {abs(calculated_error):.1f}%')

    # CAMERA ERROR CALCULATION
    calculated_elapsed_time = 0
    if c_elapsed_time != 0:
        if MIRROR_LOCKUP:
            calculated_elapsed_time += 700
        calculated_elapsed_time += float(TIME_CAMERA)
        calculated_elapsed_time += float(DEF_CAMERA_DELAY)
        calculated_elapsed_time = calculated_elapsed_time / 1000
        try:
            calculated_error = ((calculated_elapsed_time - c_elapsed_time) / calculated_elapsed_time) * 100
        except ZeroDivisionError:
            calculated_error = 0
        logging.info(
            f'Camera timings: real; {c_elapsed_time:.4f},'
            f' calculated; {calculated_elapsed_time},'
            f' error; {abs(calculated_error):.1f}%')

    # FLASH ERROR CALCULATION
    calculated_elapsed_time = 0
    if f_elapsed_time != 0:
        if MIRROR_LOCKUP:
            calculated_elapsed_time += 700
        calculated_elapsed_time += float(TIME_FLASH)
        calculated_elapsed_time += float(DEF_FLASH_DELAY)
        calculated_elapsed_time = calculated_elapsed_time / 1000
        try:
            calculated_error = ((calculated_elapsed_time - f_elapsed_time) / calculated_elapsed_time) * 100
        except ZeroDivisionError:
            calculated_error = 0
        logging.info(
            f'Flash timings: real; {f_elapsed_time:.4f},'
            f' calculated; {calculated_elapsed_time},'
            f' error; {abs(calculated_error):.1f}%')

    return 0


# Now see what we're supposed to do next
if __name__ == "__main__":
    sys.exit(main())
