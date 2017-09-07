# File: tofugpio.py
# Author: dgrubb
# Date: 09/07/2017

# Provides GPIO access.

# System modules
import logging
import os

# Pi modules
import RPi.GPIO as GPIO

MODULE = "Tofu GPIO"
LOG = logging.getLogger(MODULE)

###############################################################################
# Worker functions
###############################################################################

def setupPin(pin, pinCallback):
    # Use the board header numbering rather than the BCM SoC pinout
    GPIO.setMode(GPIO.BOARD)
    # Debounce time may be messy and require more than 300ms
    GPIO.add_event_detect(pin, GPIO.RISING, callback=pinCallback, bouncetime=300)

