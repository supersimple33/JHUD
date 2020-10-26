#!/usr/bin/python3

import time
import math
import numpy
import datetime
from kalman_filter import *

import board
import busio
import adafruit_lsm9ds1

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)

#calibrate sensor readings using kalman filter
tmpCalibration = []
while len(tmpCalibration) < 500:
    tmpValue = sensor.temperature
    tmpCalibration.append(tmpValue)
stdDev = numpy.std(tmpCalibration)
processVariance = 1e-5
estimatedMeasurementVariance = stdDev ** 2  # 0.05 ** 2
kalman_filter = KalmanFilter(processVariance, estimatedMeasurementVariance)
for iteration in range(1, len(tmpCalibration)):
    kalman_filter.input_latest_noisy_measurement(tmpCalibration[iteration])

#Obtain kalman-filtered temperature in Celsius, rounded to integer form
def getTMP():
    tmpReading = sensor.temperature
    kalman_filter.input_latest_noisy_measurement(tmpReading)
    temperature = kalman_filter.get_latest_estimated_measurement()
    return int(round(temperature))
