# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT
"""
`lis3dh`
================================================================================

LIS3DH MicroPython Driver


* Author(s): Jose D. Montoya


"""
# pylint: disable=unused-argument

import time
from micropython import const

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/jposada202020/LIS3DH.git"


_REG_WHOAMI = const(0x0F)
_REG_TEMPCFG = const(0x1F)
_REG_CTRL1 = const(0x20)  # Defaults to 0b00000000
_REG_CTRL3 = const(0x22)
_REG_CTRL4 = const(0x23)
_REG_CTRL5 = const(0x24)

# Data rate
DATARATE_1344 = const(0b1001)  # 1344 Hz
DATARATE_400 = const(0b0111)  # 400Hz
DATARATE_200 = const(0b0110)  # 200Hz
DATARATE_100 = const(0b0101)  # 100Hz
DATARATE_50 = const(0b0100)  # 50Hz
DATARATE_25 = const(0b0011)  # 25Hz
DATARATE_10 = const(0b0010)  # 10 Hz
DATARATE_1 = const(0b0001)  # 1 Hz
DATARATE_POWERDOWN = const(0)
DATARATE_LOWPOWER_1K6HZ = const(0b1000)
DATARATE_LOWPOWER_5KHZ = const(0b1001)


class CBits:
    """
    Changes bits from a byte register
    """

    def __init__(self, num_bits: int, register_address: int, start_bit: int) -> None:
        self.bit_mask = ((1 << num_bits) - 1) << start_bit
        self.register = register_address
        self.star_bit = start_bit

    def __get__(
        self,
        obj,
        objtype=None,
    ) -> int:

        reg = obj._i2c.readfrom_mem(obj._address, self.register, True)[0]
        reg = (reg & self.bit_mask) >> self.star_bit

        return reg

    def __set__(self, obj, value: int) -> None:

        memory_value = obj._i2c.readfrom_mem(obj._address, self.register, True)[0]
        memory_value &= ~self.bit_mask

        value <<= self.star_bit
        memory_value |= value

        obj._i2c.writeto_mem(obj._address, self.register, bytes([memory_value]))


class RegisterStruct:
    """
    Register Struct
    """

    def __init__(self, register_address: int, form: str) -> None:
        self.format = form
        self.register = register_address

    def __get__(
        self,
        obj,
        objtype=None,
    ):

        return obj._i2c.readfrom_mem(obj._address, self.register, True)[0]

    def __set__(self, obj, value):

        obj._i2c.writeto_mem(obj._address, self.register, bytes([value]))


class LIS3DH:
    """Driver base for the LIS3DH accelerometer."""

    _device_id = RegisterStruct(_REG_WHOAMI, "B")
    _device_control = RegisterStruct(_REG_CTRL1, "B")
    _rebbot_register = RegisterStruct(_REG_CTRL5, "B")
    _data_rate = CBits(4, _REG_CTRL1, 4)

    _test_add = CBits(3, _REG_CTRL1, 2)

    def __init__(self, int1=None, int2=None):
        # Check device ID.
        if self._device_id != 0x33:
            raise RuntimeError("Failed to find LIS3DH!")
        # Reboot

        self._reboot_register = 0x80
        time.sleep(0.01)  # takes 5ms

        self._device_control = 0x07

        self._data_rate = DATARATE_400

    @property
    def data_rate(self):
        """The data rate of the accelerometer

        +--------------------------------------------+-------------------------+
        | Mode                                       | Value                   |
        +============================================+=========================+
        | :py:const:`lis3dh.DATARATE_1`              | :py:const:`0b0001`      |
        +--------------------------------------------+-------------------------+
        | :py:const:`lis3dh.DATARATE_10`             | :py:const:`0b0010`      |
        +--------------------------------------------+-------------------------+
        | :py:const:`lis3dh.DATARATE_25`             | :py:const:`0b0011`      |
        +--------------------------------------------+-------------------------+
        | :py:const:`lis3dh.DATARATE_50`             | :py:const:`0b0100`      |
        +--------------------------------------------+-------------------------+
        | :py:const:`lis3dh.DATARATE_100`            | :py:const:`0b0101`      |
        +--------------------------------------------+-------------------------+
        | :py:const:`lis3dh.DATARATE_200`            | :py:const:`0b0110`      |
        +--------------------------------------------+-------------------------+
        | :py:const:`lis3dh.DATARATE_400`            | :py:const:`0b0111`      |
        +--------------------------------------------+-------------------------+
        | :py:const:`lis3dh.DATARATE_1344`           | :py:const:`0b1001`      |
        +--------------------------------------------+-------------------------+
        | :py:const:`lis3dh.DATARATE_POWERDOWN`      | :py:const:`0b0000`      |
        +--------------------------------------------+-------------------------+
        | :py:const:`lis3dh.DATARATE_LOWPOWER_1600`  | :py:const:`0b1000`      |
        +--------------------------------------------+-------------------------+
        | :py:const:`lis3dh.DATARATE_LOWPOWER_5000`  | :py:const:`0b1001`      |
        +--------------------------------------------+-------------------------+


        """

        return self._data_rate

    @data_rate.setter
    def data_rate(self, value):

        self._data_rate = value
