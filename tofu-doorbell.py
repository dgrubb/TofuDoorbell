#!/usr/bin/env python

# File: tofu-doorbell.py
# Author: dgrubb
# Date: 02/23/2017

# detects when an spi-based adc indicates a door has opened and plays
# an mp3 sample in reponse.

# system imports
import getopt
import logging
import sys
import time

# Tofu imports
import tofuaudio
import tofuversion

###############################################################################

MODULE = "Tofu Doorbell"
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

    -h, --help          Print usage.
"""

###############################################################################

def parseArgs(argv):
    global MUSIC_DIR
    logLevel = LOG_LEVEL
    try:
        opts, args = getopt.getopt(
            argv,
            "l:d:h",
            ["log=", "directory=", "help"]
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
    logging.basicConfig(format=LOG_FORMAT, level=logLevel)

def main(argv):
    parseArgs(argv)
    LOG.info(
        "Tofu Doorbell initialised, logging level: {0}".format(
            logging.getLevelName(LOG.getEffectiveLevel())
        )
    )

    player = tofuaudio.TofuAudioPlayer()
    if not player:
        LOG.error("Failed to instantiate an audio player")
        return

    musicList = tofuaudio.scanDirectoryForMusicFiles(MUSIC_DIR)
    if not musicList:
        LOG.error("Failed to find audio files")
        return

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main(sys.argv[1:])

