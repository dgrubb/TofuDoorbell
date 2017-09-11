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
INVALID_PINS = {
    "5v":     [2, 4],
    "3.3v":   [1, 17],
    "Ground": [6, 9, 14, 20, 30, 39],
    "I2C":    [27, 28]
}

activePins = []
GPIOinited = False

###############################################################################
# Worker functions
###############################################################################

def initGPIO():
    # Use the board header numbering rather than the BCM SoC pinout
    GPIO.setmode(GPIO.BOARD)
    GPIOinited = True

def setupPin(pin, pinCallback):
    if not isValidPin(pin):
        return False
    if pin in activePins:
        LOG.warning("Can't use pin [ {0} ], already initialised".format(pin))
        return False
    if not GPIOinited:
        initGPIO()
    try:
        GPIO.setup(pin, GPIO.IN)
        # Debounce time may be messy and require more than 300ms
        GPIO.add_event_detect(pin, GPIO.RISING, callback=pinCallback, bouncetime=300)
    except:
        LOG.error("Error setting up pin [ {0} ] as input".format(pin))
        return False
    activePins.append(pin)
    LOG.info("Setup pin [ {0} ] for input".format(pin));
    return True

def closePin(pin):
    if pin not in activePins:
        LOG.error("Error closing pin [ {0} ], not opened".format(pin))
        return False
    GPIO.remove_event_detect(pin)
    GPIO.cleanup(pin)
    activePins.remove(pin)
    if not activePins:
        # We've closed all open pins but they ay be reopened in future
        GPIOinited = False
    return True

def closeAllPins():
    LOG.info("Closing all input pins")
    activePinsCopy = activePins[:]
    for pin in activePinsCopy:
        closePin(pin)

def isValidPin(pin):
    if pin < 1 or pin > 40:
        LOG.error("Pin [ {0} ] outside valid range".format(pin))
        return False
    if pin in INVALID_PINS["5v"]:
        LOG.error("Pin [ {0} ] is invalid as GPIO, 5v power".format(pin))
        return False
    if pin in INVALID_PINS["3.3v"]:
        LOG.error("Pin [ {0} ] is invalid as GPIO, 3.3v power".format(pin))
        return False
    if pin in INVALID_PINS["Ground"]:
        LOG.error("Pin [ {0} ] is invalid as GPIO, power ground".format(pin))
        return False
    if pin in INVALID_PINS["I2C"]:
        LOG.error("Pin [ {0} ] is invalid as GPIO, I2C peripheral".format(pin))
        return False
    LOG.debug("Pin [ {0} ] valided for use as GPIO".format(pin))
    return True
