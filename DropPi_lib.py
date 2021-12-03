# =========================================================
# Seeed Studio Raspberry Pi Relay Board Library
#
# Modified from the sample code on the Seeed Studio Wiki
# http://wiki.seeed.cc/Raspberry_Pi_Relay_Board_v1.0/
# =========================================================
# Changes made by K. Dalmeijer specific to DropPi needs
# =========================================================

from __future__ import print_function

import smbus2 as smbus

# The number of relay ports on the relay board.
# This value should never change!
NUM_RELAY_PORTS = 8

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

# Change the following value if your Relay board uses a different I2C address.
DEVICE_ADDRESS1 = 0x20  # 7 bit address (will be left shifted to add the read write bit)
DEVICE_ADDRESS2 = 0x21
# Don't change the values, there's no need for that.
DEVICE_REG_MODE1 = 0x06
DEVICE_REG_DATA1 = 0xff
DEVICE_REG_DATA2 = 0xff

bus = smbus.SMBus(1)  # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)


# Changed relay_on to accomodate multiple relays being called at once.
# Because of timing, I could not accept sequentially turning relays on and off
# one by one. This would cause double exposures in my images because of one
# flash firing a few microseconds behind the other.
#
# Usage: For instance, to fire relays 1,2 and 4 at once;
#
#   relay_on(1,2,4)
#
def relay_on(*relay_numbers):
    global DEVICE_ADDRESS1
    global DEVICE_ADDRESS2
    global DEVICE_REG_DATA1
    global DEVICE_REG_DATA2
    global DEVICE_REG_MODE1

    for relay_num in relay_numbers:
        if isinstance(relay_num, int):
            # do we have a valid relay number?
            if 0 < relay_num <= NUM_RELAY_PORTS:
                if relay_num <= 4:
                    # print('Turning board 0 relay', relay_num, 'ON')
                    DEVICE_REG_DATA1 &= ~(0x1 << (relay_num - 1))
                else:
                    relay_num = relay_num - 4
                    # print('Turning board 1 relay', relay_num, 'ON')
                    DEVICE_REG_DATA2 &= ~(0x1 << (relay_num - 1))
            else:
                print('Invalid relay #:', relay_num)
        else:
            print('Relay number must be an Integer value')
    bus.write_byte_data(DEVICE_ADDRESS1, DEVICE_REG_MODE1, DEVICE_REG_DATA1)
    bus.write_byte_data(DEVICE_ADDRESS2, DEVICE_REG_MODE1, DEVICE_REG_DATA2)


# adjusted relay_off. See relay_on remarks for more information
#
def relay_off(*relay_numbers):
    global DEVICE_ADDRESS1
    global DEVICE_ADDRESS2
    global DEVICE_REG_DATA1
    global DEVICE_REG_DATA2
    global DEVICE_REG_MODE1

    for relay_num in relay_numbers:
        if isinstance(relay_num, int):
            # do we have a valid relay number?
            if 0 < relay_num <= NUM_RELAY_PORTS:
                # print('Turning relay', relay_num, 'OFF')
                if relay_num <= 4:
                    DEVICE_REG_DATA1 |= (0x1 << (relay_num - 1))
                else:
                    relay_num = relay_num - 4
                    DEVICE_REG_DATA2 |= (0x1 << (relay_num - 1))
            else:
                print('Invalid relay #:', relay_num)
        else:
            print('Relay number must be an Integer value')
    bus.write_byte_data(DEVICE_ADDRESS1, DEVICE_REG_MODE1, DEVICE_REG_DATA1)
    bus.write_byte_data(DEVICE_ADDRESS2, DEVICE_REG_MODE1, DEVICE_REG_DATA2)


def relay_all_on():
    global DEVICE_ADDRESS1
    global DEVICE_ADDRESS2
    global DEVICE_REG_DATA1
    global DEVICE_REG_DATA2
    global DEVICE_REG_MODE1

    print('Turning all relays ON')
    DEVICE_REG_DATA1 &= ~(0xf << 0)
    DEVICE_REG_DATA2 &= ~(0xf << 0)
    bus.write_byte_data(DEVICE_ADDRESS1, DEVICE_REG_MODE1, DEVICE_REG_DATA1)
    bus.write_byte_data(DEVICE_ADDRESS2, DEVICE_REG_MODE1, DEVICE_REG_DATA2)


def relay_all_off():
    global DEVICE_ADDRESS1
    global DEVICE_ADDRESS2
    global DEVICE_REG_DATA1
    global DEVICE_REG_DATA2
    global DEVICE_REG_MODE1

    print('Turning all relays OFF')
    DEVICE_REG_DATA1 |= (0xf << 0)
    DEVICE_REG_DATA2 |= (0xf << 0)
    bus.write_byte_data(DEVICE_ADDRESS1, DEVICE_REG_MODE1, DEVICE_REG_DATA1)
    bus.write_byte_data(DEVICE_ADDRESS2, DEVICE_REG_MODE1, DEVICE_REG_DATA2)


def relay_toggle_port(relay_num):
    print('Toggling relay:', relay_num)
    if relay_get_port_status(relay_num):
        # it's on, so turn it off
        relay_off(relay_num)
    else:
        # it's off, so turn it on
        relay_on(relay_num)


def relay_get_port_status(relay_num):
    # determines whether the specified port is ON/OFF
    global DEVICE_REG_DATA1
    global DEVICE_REG_DATA2
    print('Checking status of relay', relay_num)
    res = relay_get_port_data(relay_num)
    if res > 0:
        mask = 1 << (relay_num - 1)
        # return the specified bit status
        # return (DEVICE_REG_DATA & mask) != 0
        return (DEVICE_REG_DATA1 & mask) == 0
    else:
        # otherwise (invalid port), always return False
        print("Specified relay port is invalid")
        return False


def relay_get_port_data(relay_num):
    # gets the current byte value stored in the relay board
    global DEVICE_REG_DATA1
    print('Reading relay status value for relay', relay_num)
    # do we have a valid port?
    if 0 < relay_num <= NUM_RELAY_PORTS:
        # read the memory location
        if relay_num <= 3:
            DEVICE_REG_DATA1 = bus.read_byte_data(DEVICE_ADDRESS1, DEVICE_REG_MODE1)
        else:
            DEVICE_REG_DATA1 = bus.read_byte_data(DEVICE_ADDRESS2, DEVICE_REG_MODE1)
        # return the specified bit status
        return DEVICE_REG_DATA1
    else:
        # otherwise (invalid port), always return 0
        print("Specified relay port is invalid")
        return 0
