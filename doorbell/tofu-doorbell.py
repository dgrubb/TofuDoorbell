#!/usr/bin/env python

# File: tofu-doorbell.py
# Author: dgrubb
# Date: 02/23/2017

# detects when an spi-based adc indicates a door has opened and plays
# an mp3 sample in reponse.

# system imports
import getopt
import logging
import signal
import sys
import time

# Tofu imports
import tofuaudio
import tofugpio
import tofuversion

###############################################################################

MODULE = "Tofu Doorbell"
DEFAULT_PIN = 32 # According to Pi header pinout, NOT BCM chip pinout
MUSIC_DIR = "./"
LOG = logging.getLogger(MODULE)
LOG_FORMAT = "[ %(asctime)s | %(name)-13s | %(levelname)-8s ] %(message)s"
LOG_LEVELS = {
    "debug":    logging.DEBUG,
    "info":     logging.INFO,
    "warning":  logging.WARNING,
    "error":    logging.ERROR,
    "critical": logging.CRITICAL
}
LOG_LEVEL = LOG_LEVELS["info"] # Default, may be overwritten by user
USAGE = """
    """ + MODULE + """ (v""" + tofuversion.TOFU + """) - A utility for
    determining if a door has been opened and plays a music sample.

    Usage:

    $ ./tofu-doorbell.py -l <logging level> -d <audio directory>

    -l, --log            Log level, options:

                            debug
                            info
                            warning
                            error
                            critical

    -d, --directory     Directory where audio samples are stored. Relative
                        and absolute paths are valid, e.g.,:

                            -d ./music
                            -d /opt/somedir/audio

    -p, --pin           Pin to use as input signal source (Default: 32)

    -h, --help          Print usage.
"""

###############################################################################

def parseArgs(argv):
    global MUSIC_DIR
    global DEFAULT_PIN
    logLevel = LOG_LEVEL
    try:
        opts, args = getopt.getopt(
            argv,
            "l:d:p:h",
            ["log=", "directory=", "pin=", "help"]
        )
    except getopt.GetoptError as e:
        # We haven't instantiated LOG yet so default to basic print
        print e
        print USAGE
        sys.exit(-1)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print USAGE
            sys.exit(-1)
        elif opt in ("-l", "--log"):
            if arg not in LOG_LEVELS:
                print USAGE
                sys.exit(-1)
            else:
                logLevel = LOG_LEVELS[arg]
        elif opt in ("-d", "--directory"):
            MUSIC_DIR = arg
        elif opt in ("-p", "--pin"):
            try:
                pin = int(arg)
            except:
                print USAGE
                sys.exit(-1)
            if not tofugpio.isValidPin(pin):
                print USAGE
                sys.exit(-1)
            DEFAULT_PIN = pin
    logging.basicConfig(format=LOG_FORMAT, level=logLevel)

def main(argv):
    parseArgs(argv)
    LOG.info(
        "Tofu Doorbell initialised, logging level: {0}".format(tofuversion.TOFU)
    )
    LOG.info("Logging level: {0}".format(
        logging.getLevelName(LOG.getEffectiveLevel()))
    )

    musicList = tofuaudio.scanDirectoryForMusicFiles(MUSIC_DIR)
    if not musicList:
        LOG.error("Failed to find audio files")
        return

    player = tofuaudio.TofuAudioPlayer(musicList, MUSIC_DIR)
    if not player:
        LOG.error("Failed to instantiate an audio player")
        return

    def pinCallback(pin):
        LOG.debug("GPIO I/O callback fired")
        player.playRandom()

    LOG.info("Using pin [ {0} ] for input".format(DEFAULT_PIN))
    tofugpio.setupPin(DEFAULT_PIN, pinCallback)

    # Release resources gracefully if forcibly killed
    def signalHandler(signal, frame):
        print "Caught signal ({0}), exiting ...".format(signal)
        tofugpio.closeAllPins()
        player.closeAudio()
        sys.exit(0)
    signal.signal(signal.SIGINT, signalHandler)
    signal.signal(signal.SIGQUIT, signalHandler)
    signal.signal(signal.SIGTERM, signalHandler)

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main(sys.argv[1:])

