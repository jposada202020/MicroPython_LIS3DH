# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT
"""
`i2c_helpers`
================================================================================

I2C MicroPython Helpers


* Author(s): Jose D. Montoya


"""
# pylint: disable=unused-argument, no-name-in-module

try:
    import struct
except ImportError:
    import ustruct as struct

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/jposada202020/LIS3DH.git"


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

    def __init__(self, register_address: int, form: str, lenght=1) -> None:
        self.format = form
        self.register = register_address
        self.lenght = struct.calcsize(form)

    def __get__(
        self,
        obj,
        objtype=None,
    ):
        if self.lenght == 1:
            value = obj._i2c.readfrom_mem(obj._address, self.register, self.lenght)[0]
        else:
            value = struct.unpack(
                self.format,
                memoryview(
                    obj._i2c.readfrom_mem(obj._address, self.register, self.lenght)
                ),
            )

        return value

    def __set__(self, obj, value):
        mem_value = struct.pack(self.format, value)
        obj._i2c.writeto_mem(obj._address, self.register, mem_value)
