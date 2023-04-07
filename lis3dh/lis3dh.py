# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT
"""
`lis3dh`
================================================================================

LIS3DH MicroPython Driver


* Author(s): Jose D. Montoya


"""
# pylint: disable=unused-argument, no-name-in-module

import time
from micropython import const
from lis3dh.i2c_helpers import CBits, RegisterStruct

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/jposada202020/LIS3DH.git"


_REG_WHOAMI = const(0x0F)
_REG_TEMPCFG = const(0x1F)
_REG_CTRL1 = const(0x20)  # Defaults to 0b00000000
_REG_CTRL3 = const(0x22)
_REG_CTRL4 = const(0x23)
_REG_CTRL5 = const(0x24)
_REG_OUT_X_L = const(0x28)

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

# Data Range
DATARANGE_2 = const(0b00)  # +/- 2g (default value)
DATARANGE_4 = const(0b01)  # +/- 4g
DATARANGE_8 = const(0b10)  # +/- 8g
DATARANGE_16 = const(0b11)  # +/- 16g

# Axes Enabling
AXES_X = const(0b001)
AXES_Y = const(0b010)
AXES_X_Y = const(0b011)
AXES_Z = const(0b100)
AXES_Z_X = const(0b101)
AXES_Z_Y = const(0b110)
AXES_Z_Y_X = const(0b111)


class LIS3DH:
    """Main class for the Sensor

    :param ~machine.I2C i2c: The I2C bus the LIS3DH is connected to.
    :param int address: The I2C device address. Defaults to :const:`0x18`

    :raises RuntimeError: if the sensor is not found


    **Quickstart: Importing and using the device**

    Here is an example of using the :class:`LIS3DH` class.
    First you will need to import the libraries to use the sensor

    .. code-block:: python

        from machine import Pin, I2C
        import lis3dh

    Once this is done you can define your `machine.I2C` object and define your sensor object

    .. code-block:: python

        i2c = I2C(sda=Pin(8), scl=Pin(9))  # Correct I2C pins for UM FeatherS2
        lis = lis3dh.LIS3DH(i2c)

    Now you have access to the :attr:`acceleration` attribute

    .. code-block:: python

        acc_x, acc_y, acc_z = lis3dh.acceleration

    """

    _device_id = RegisterStruct(_REG_WHOAMI, "B")
    _device_control = RegisterStruct(_REG_CTRL1, "B")
    _reboot_register = RegisterStruct(_REG_CTRL5, "B")
    _ctrl4_register = RegisterStruct(_REG_CTRL4, "B")
    _reg_xl = RegisterStruct(_REG_OUT_X_L | 0x80, "<hhh")
    _temp_comp = RegisterStruct(_REG_TEMPCFG, "B")

    # CTRL_REG1 (20h) ODR3|ODR2|ODR1|ODR0|LPen|Zen|Yen|Xen
    _axes_enabled = CBits(3, _REG_CTRL1, 3)  # Zen|Yen|Xen
    _data_rate = CBits(4, _REG_CTRL1, 4)  # ODR3|ODR2|ODR1|ODR0

    # TEMP_CFG_REG (1Fh) ADC_PD|TEMP_EN
    _adc_pd = CBits(1, _REG_TEMPCFG, 7)
    _temp_en = CBits(1, _REG_TEMPCFG, 6)

    # CTRL_REG4 (23h) BDU|BLE|FS1|FS0|HR|ST1|ST0|SIM
    _range = CBits(2, _REG_CTRL4, 4)  # FS1|FS0
    _high_resolution = CBits(1, _REG_CTRL4, 3)  # HR
    _block_data = CBits(1, _REG_CTRL4, 7)  # BDU

    # CTRL_REG5 (24h) BOOT
    _reboot = CBits(1, _REG_CTRL5, 7)

    # Conversion Values
    acceleration_scale = {0: 16380, 1: 8190, 2: 4096, 3: 1365}

    def __init__(self, i2c, address=0x18):
        self._i2c = i2c
        self._address = address

        if self._device_id != 0x33:
            raise RuntimeError("Failed to find LIS3DH!")
        self._reboot = 1
        time.sleep(0.01)

        self._axes_enabled = AXES_Z_Y_X
        self._data_rate = DATARATE_400
        self._high_resolution = 1
        self._block_data = 1
        self._adc_pd = 1

    @property
    def axes_enabled(self):
        """The data rate of the accelerometer

        +--------------------------------------------+-------------------------+
        | Mode                                       | Value                   |
        +============================================+=========================+
        | :py:const:`lis3dh.AXES_X`                  | :py:const:`0b001`       |
        +--------------------------------------------+-------------------------+
        | :py:const:`lis3dh.AXES_Y`                  | :py:const:`0b010`       |
        +--------------------------------------------+-------------------------+
        | :py:const:`lis3dh.AXES_X_Y`                | :py:const:`0b011`       |
        +--------------------------------------------+-------------------------+
        | :py:const:`lis3dh.AXES_Z`                  | :py:const:`0b100`       |
        +--------------------------------------------+-------------------------+
        | :py:const:`lis3dh.AXES_Z_X`                | :py:const:`0b101`       |
        +--------------------------------------------+-------------------------+
        | :py:const:`lis3dh.AXES_Z_Y`                | :py:const:`0b110`       |
        +--------------------------------------------+-------------------------+
        | :py:const:`lis3dh.AXES_Z_Y_X`              | :py:const:`0b111`       |
        +--------------------------------------------+-------------------------+


        """

        return self._axes_enabled

    @axes_enabled.setter
    def axes_enabled(self, value):

        self._axes_enabled = value

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

    @property
    def data_range(self):
        """The range of the accelerometer.

        +--------------------------------------------+-------------------------+
        | Mode                                       | Value                   |
        +============================================+=========================+
        | :py:const:`lis3dh.DATARANGE_2`             | :py:const:`0b00`        |
        +--------------------------------------------+-------------------------+
        | :py:const:`lis3dh.DATARANGE_4`             | :py:const:`0b01`        |
        +--------------------------------------------+-------------------------+
        | :py:const:`lis3dh.DATARANGE_8`             | :py:const:`0b10`        |
        +--------------------------------------------+-------------------------+
        | :py:const:`lis3dh.DATARANGE_16`            | :py:const:`0b11`        |
        +--------------------------------------------+-------------------------+


        """

        return self._range

    @data_range.setter
    def data_range(self, value):
        self._range = value

    @property
    def acceleration(self):
        """
        The x, y, z acceleration values returned in a 3-tuple and are in :math:`m/s^2`

        """

        x, y, z = self._reg_xl

        factor = self.acceleration_scale[self.data_range]

        return (x / factor) * 9.806, (y / factor) * 9.806, (z / factor) * 9.806
