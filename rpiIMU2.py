#!/usr/bin/python3

import time
import math
import datetime

import board
import busio
import adafruit_lsm9ds1

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)

RAD_TO_DEG = 57.29578
M_PI = 3.14159265358979323846
G_GAIN = 0.070  # [deg/s/LSB]  If you change the dps for gyro, you need to update this value accordingly
AA =  0.40      # Complementary filter constant
accSensitivity = 0.732/1000 #according to data sheet for linear acceleration +/- 16g range

sensor.accel_range = adafruit_lsm9ds1.ACCELRANGE_16G
sensor.mag_gain = adafruit_lsm9ds1.MAGGAIN_12GAUSS
sensor.gyro_scale = adafruit_lsm9ds1.GYROSCALE_2000DPS

#Function used calculate the magnetometer heading in order to be used with the compass
def calcHeading():
    magX, magY, magZ = sensor.magnetic
    accX, accY, accZ = sensor.acceleration
    #Normalize accelerometer raw values.
    ###################Calculate pitch and roll#########################
    #Us these two lines when the IMU is up the right way. Skull logo is facing down
    accXnorm = accX/math.sqrt(accX * accX + accY * accY + accZ * accZ)
    accYnorm = accY/math.sqrt(accX * accX + accY * accY + accZ * accZ)
    pitch = math.asin(accXnorm)
    roll = -math.asin(accYnorm/math.cos(pitch))

    #Calculate the new tilt compensated values
    magXcomp = magX*math.cos(pitch)+magZ*math.sin(pitch)
    magYcomp = magX*math.sin(roll)*math.sin(pitch)+magY*math.cos(roll)-magZ*math.sin(roll)*math.cos(pitch)

    #Calculate tilt compensated heading
    tiltCompensatedHeading = 180 * math.atan2(magYcomp, magXcomp)/M_PI

    if tiltCompensatedHeading < 0:
        tiltCompensatedHeading += 360
    return tiltCompensatedHeading

#Function used to calculate the acceleration value
def calcAcceleration():
    #Read the accelerometer,gyroscope values
    accX, accY, accZ = sensor.acceleration      #multiply raw reading by sensitvity to obtain acc in g's
    accX *= accSensitivity
    accY *= accSensitivity
    accZ *= accSensitivity

    #Normalize x and y vectors to compensate for gravity
    thetaX = math.atan(accX/math.sqrt(accY**2+accZ**2))
    thetaY = math.atan(accY/math.sqrt(accX**2+accZ**2))
  
    accXComp = accX * math.cos(thetaX)
    accYComp = accY * math.cos(thetaY)

    acceleration = math.sqrt(accXComp**2 + accYComp**2) * 9.807

    return acceleration