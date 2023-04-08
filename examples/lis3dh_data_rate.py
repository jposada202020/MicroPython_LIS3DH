# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya

import time
from machine import Pin, I2C
import micropython

i2c = I2C(sda=Pin(8), scl=Pin(9))
lis = micropython.LIS3DH(i2c)

# Getting information about the current Accelerometers Data Rate
print("Accelerometer Data Rate: ", lis.data_rate)
for _ in range(3):
    accx, accy, accz = lis.acceleration
    print("X: ", accx)
    print("Y: ", accy)
    print("Z: ", accz)
    print("----------")
    time.sleep(1)

# Changing Data Rate of the accelerometer
lis.data_rate = micropython.DATARATE_200
print("Accelerometer Changed Data Rate: ", lis.data_rate)
for _ in range(3):
    accx, accy, accz = lis.acceleration
    print("X: ", accx)
    print("Y: ", accy)
    print("Z: ", accz)
    print("----------")
    time.sleep(1)
