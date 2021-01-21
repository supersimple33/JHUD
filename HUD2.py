#HUD2.py
#This program will compile all the IMU and OBDII readings
#and display them onto the TFT screen.
#Created by XiaoXing Zhao and William Voge
#Edited 5/16/2016

import pygame
import sys
import os
import time
from rpiIMU2 import *
from temp_read2 import *
from pynog import *

# MARK: comment in when adding touch screen here and line 27
# os.environ['SDL_VIDEODRIVER'] = 'fbcon'   #set up os environment to display to TFT
# os.environ['SDL_FBDEV'] = '/dev/fb1'
# os.environ['SDL_MOUSEDEV'] = '/dev/input/touchscreen' #set up touchscreen as mouse input
# os.environ['SDL_MOUSEDRV'] = 'TSLIB'

black = 0, 0, 0
white = 255, 255, 255
green = 50, 226, 50
blue = 84, 179, 247
red = 255, 71, 71

pygame.init()
pygame.mouse.set_visible(True) # could set his back to false

screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
width, height = screen.get_size()

font = pygame.font.Font(None, 40)
font2 = pygame.font.Font(None, 60)
font3 = pygame.font.Font(None, 54)
fontSmall = pygame.font.Font(None, 36)

quit_text = font.render("QUIT", 1, (255, 250, 255))   #set up texts as buttons
q_text_pos = quit_text.get_rect()
q_text_pos.centerx = screen.get_rect().centerx + 100
q_text_pos.centery = screen.get_rect().centery + 100

compass_text = font.render("COMPASS", 1, (255, 250, 255))
c_text_pos = compass_text.get_rect()
c_text_pos.centerx = 70
c_text_pos.centery = 220

display_compass = 0     #toggle displaying compass
display_F = 1           #toggle displaying fahrenheit
display_kph = 0         #toggle displaying km per hour

def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

time_count = 0
acceleration = 0

while 1:
    time_count += 1
    temperature = getTMP()
    speed = getSpeed()
    rpm = getRPM()
    coolant = getCoolantTemp()
    intake = getIntakeTemp()
    load = getLoad()
    throttle = getThrottle()

    # speed = 55 # temp
    # rpm = 879 # temp
    # coolant = 170
    # intake = 110
    # load = 44
    # throttle = 78
    #Handle value error due to incorrect math domain
    try:
        heading = int(calcHeading()) - 20
        if heading < 0:
            heading = 360 + heading
        if time_count % 2: 
            acceleration = calcAcceleration()
    except ValueError:
        heading = 1000

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            p = pygame.mouse.get_pos()
        #touch screen button press detection logic, for quit button

        # MARK: added in order to silence p event in the beiginning before p is defined
        try:
            if p == 0:
                testedP = 1
        except NameError:
            continue

        if p[0]>240 and p[0]<285 and p[1]>200 and p[1]<220: 
            sys.exit()
        elif p[0]>50 and p[0]<90 and p[1]>200 and p[1]<230:
            display_compass ^= 1
        elif p[0]>213 and p[0]<300 and p[1]>140 and p[1]<200 :
            display_F ^= 1
        elif p[0]>20 and p[0]<width/3 and p[1]>20 and p[1]<70:
            display_kph ^= 1

    print("temperature is " + str(temperature))
    print("heading is " + str(heading))
    print("acceleration is " + str(acceleration))
    print("speed is " + str(speed))
    print("RPM is " + str(rpm))
    print("coolant is " + str(coolant))
    print("intake is " + str(intake))
    print("load is " + str(load))
    print("throttle is " + str(throttle))

    screen.fill(black)
    screen.blit(quit_text, q_text_pos)
    screen.blit(compass_text, c_text_pos)

    # MARK: New Compass
    pygame.draw.line(screen, green, (width / 4, height / 2), (3 * width / 4, height / 2))

    offset = (10 - (heading % 10)) / 10.0
    greenBarArray = [-1.5, -1.0, -0.5, 0.0, 0.5]
    if offset >= 0.8:
        greenBarArray = [-2.0, -1.5, -1.0, -0.5, 0.0]
    elif offset <= 0.2:
        greenBarArray = [-1.0, -0.5, 0.0, 0.5, 1.0]
    for mover in greenBarArray:
        posComp = ((width / 2) + ((mover + offset) * (width / 5))) # HERE
        pygame.draw.line(screen, green, (posComp, height / 2), (posComp, (height / 2) + (height / 12)))
        if abs(mover) != 1.5 and abs(mover) != 0.5:
            if offset > 0.5:
                headingGText = font2.render(str(int(round(heading / 10) + mover + 1) * 10), 1, red)
                greenHeadingRect = headingGText.get_rect()
                greenHeadingRect.centerx = posComp
                greenHeadingRect.centery = (height / 2) + (height / 6)
                screen.blit(headingGText, greenHeadingRect)
            else:
                headingGText = font2.render(str(int(round(heading / 10) + mover) * 10), 1, red)
                greenHeadingRect = headingGText.get_rect()
                greenHeadingRect.centerx = posComp
                greenHeadingRect.centery = (height / 2) + (height / 6)
                screen.blit(headingGText, greenHeadingRect)

    # MARK: New Speed
    pygame.draw.line(screen, green, (width / 7, (height / 7) - 2), (width / 7, (6 * height / 7) + 2))
    pygame.draw.line(screen, green, (width / 7, (height / 7) - 2), (0, (height / 7) - 2))
    pygame.draw.line(screen, green, (width / 7, (6 * height / 7) + 2), (0, (6 * height / 7) + 2))

    offsetS = (speed % 10) / 10.0
    print("Offset: " + str(offsetS))

    speedBarArray = [-1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5]
    if offsetS >= 0.8:
        speedBarArray = [-2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5]
    elif offsetS >= 0.3 and offsetS < 0.8:
        speedBarArray = [-2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0]
    for moverB in speedBarArray:
        if ((round(speed / 10) + (-1 * moverB)) * 10 < 0 and offsetS <= 0.5) or ((round(speed / 10) + (-1 * moverB)) * 10 < 10 and offsetS > 0.5):
            continue
        posSpeedBar = (height / 2) + ((moverB + (offsetS)) * (height / 5))
        pygame.draw.line(screen, green, (width / 7, posSpeedBar), ((width / 7) - (height / 24), posSpeedBar))
        if abs(moverB) != 1.5 and abs(moverB) != 0.5 and abs(moverB) != 2.5:
            if offsetS > 0.5 or speed == 15:
                speedTinyText = font.render(str(int(round(speed / 10) + (-1 * moverB)) * 10 - 10), 1, red)
                speedTinyRect = speedTinyText.get_rect()
                speedTinyRect.centerx = (width / 7) - (width / 14)
                speedTinyRect.centery = posSpeedBar
                screen.blit(speedTinyText, speedTinyRect)
            else:
                speedTinyText = font.render(str(int(round(speed / 10) + (-1 * moverB)) * 10), 1, red)
                speedTinyRect = speedTinyText.get_rect()
                speedTinyRect.centerx = (width / 7) - (width / 14)
                speedTinyRect.centery = posSpeedBar
                screen.blit(speedTinyText, speedTinyRect)

    rectBlackOut = pygame.Rect(0, 0, 0, 0)
    rectBlackOut.top = (height / 2) - (width / 25)
    rectBlackOut.left = (width / 7) - (width / 9)
    rectBlackOut.height = (2 * width / 25) + 1
    rectBlackOut.width = (width / 9) - 1
    pygame.draw.rect(screen, black, rectBlackOut)

    pygame.draw.line(screen, green, (width / 7, height / 2), ((width / 7) - (width / 25), (height / 2) + (width / 25)))
    pygame.draw.line(screen, green, (width / 7, height / 2), ((width / 7) - (width / 25), (height / 2) - (width / 25)))
    pygame.draw.line(screen, green, ((width / 7) - (width / 9), (height / 2) - (width / 25)), ((width / 7) - (width / 25), (height / 2) - (width / 25)))
    pygame.draw.line(screen, green, ((width / 7) - (width / 9), (height / 2) + (width / 25)), ((width / 7) - (width / 25), (height / 2) + (width / 25)))
    pygame.draw.line(screen, green, ((width / 7) - (width / 9), (height / 2) + (width / 25)), ((width / 7) - (width / 9), (height / 2) - (width / 25)))

    speedTrueText = font3.render(str(speed), 1, red)
    speedTrueRect = speedTrueText.get_rect()
    speedTrueRect.centerx = (width / 7) - ((width / 15))
    speedTrueRect.centery = height / 2
    screen.blit(speedTrueText, speedTrueRect)

    # MARK: New RPM
    pygame.draw.line(screen, green, (6 * width / 7, (height / 7) - 2), (6 * width / 7, (6 * height / 7) + 2))
    pygame.draw.line(screen, green, (6 * width / 7, (height / 7) - 2), (width, (height / 7) - 2))
    pygame.draw.line(screen, green, (6 * width / 7, (6 * height / 7) + 2), (width, (6 * height / 7) + 2))

    rpm = int(rpm / 10)
    offsetS = (rpm % 10) / 10.0
    print("Offset: " + str(offsetS))

    speedBarArray = [-1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5]
    if offsetS >= 0.8:
        speedBarArray = [-2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5]
    elif offsetS >= 0.3 and offsetS < 0.8:
        speedBarArray = [-2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0]
    for moverB in speedBarArray:
        if ((round(rpm / 10) + (-1 * moverB)) * 10 < 0 and offsetS <= 0.5) or ((round(rpm / 10) + (-1 * moverB)) * 10 < 10 and offsetS > 0.5):
            continue
        posSpeedBar = (height / 2) + ((moverB + (offsetS)) * (height / 5))
        pygame.draw.line(screen, green, (6 * width / 7, posSpeedBar), ((6 * width / 7) + (height / 24), posSpeedBar))
        if abs(moverB) != 1.5 and abs(moverB) != 0.5 and abs(moverB) != 2.5:
            if offsetS > 0.5 or rpm == 15:
                speedTinyText = font.render(str(int(round(rpm / 10) + (-1 * moverB)) * 10 - 10), 1, red)
                speedTinyRect = speedTinyText.get_rect()
                speedTinyRect.centerx = (6 * width / 7) + (width / 14)
                speedTinyRect.centery = posSpeedBar
                screen.blit(speedTinyText, speedTinyRect)
            else:
                speedTinyText = font.render(str(int(round(rpm / 10) + (-1 * moverB)) * 10), 1, red)
                speedTinyRect = speedTinyText.get_rect()
                speedTinyRect.centerx = (6 * width / 7) + (width / 14)
                speedTinyRect.centery = posSpeedBar
                screen.blit(speedTinyText, speedTinyRect)

    rectBlackOutRev = pygame.Rect(0, 0, 0, 0)
    rectBlackOutRev.top = (height / 2) - (width / 25)
    rectBlackOutRev.width = (width / 9) - 1
    rectBlackOutRev.right = (6 * width / 7) + (width / 9) # Check Debug Here
    rectBlackOutRev.height = (2 * width / 25) + 1
    
    pygame.draw.rect(screen, black, rectBlackOutRev)

    pygame.draw.line(screen, green, (6 * width / 7, height / 2), ((6 * width / 7) + (width / 25), (height / 2) + (width / 25)))
    pygame.draw.line(screen, green, (6 * width / 7, height / 2), ((6 * width / 7) + (width / 25), (height / 2) - (width / 25)))
    pygame.draw.line(screen, green, ((6 * width / 7) + (width / 9), (height / 2) - (width / 25)), ((6 * width / 7) + (width / 25), (height / 2) - (width / 25)))
    pygame.draw.line(screen, green, ((6 * width / 7) + (width / 9), (height / 2) + (width / 25)), ((6 * width / 7) + (width / 25), (height / 2) + (width / 25)))
    pygame.draw.line(screen, green, ((6 * width / 7) + (width / 9), (height / 2) + (width / 25)), ((6 * width / 7) + (width / 9), (height / 2) - (width / 25)))

    speedTrueText = font3.render(str(rpm), 1, red)
    speedTrueRect = speedTrueText.get_rect()
    speedTrueRect.centerx = (6 * width / 7) + ((width / 15))
    speedTrueRect.centery = height / 2
    screen.blit(speedTrueText, speedTrueRect)
    
    pygame.display.flip()
    time.sleep(0.1)
