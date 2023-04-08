# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya

import time
from machine import Pin, I2C
import micropython

i2c = I2C(sda=Pin(8), scl=Pin(9))  # Correct I2C pins for UM FeatherS2
lis = micropython.LIS3DH(i2c)

# Getting information about the current Accelerometers Data Range
print("Accelerometer Data Range: ", lis.data_range)
for _ in range(3):
    accx, accy, accz = lis.acceleration
    print("X: ", accx)
    print("Y: ", accy)
    print("Z: ", accz)
    print("----------")
    time.sleep(1)

# Changing Data Range of the accelerometer
lis.data_range = micropython.DATARANGE_8
print("Accelerometer Changed Data Range: ", lis.data_range)
for _ in range(3):
    accx, accy, accz = lis.acceleration
    print("X: ", accx)
    print("Y: ", accy)
    print("Z: ", accz)
    print("----------")
    time.sleep(1)
