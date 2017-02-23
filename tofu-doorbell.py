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
from tofuutils import LOG
import tofuversion

MODULE = "Tofu Doorbell"
USAGE = """
    """ + MODULE + """ (v""" + tofuversion.TOFU + """) - A utility for
    determining if a door has been opened and plays a music sample.

    Usage:

    $ ./tofu-doorbell.py -l <logging level>

    -l, --log   Log level, options:

                    debug
                    info
                    warning
                    error
                    critical

    -h, --help  Print usage.
"""

def parseArgs(argv):
    try:
        opts, args = getopt.getopt(
            argv,
            "l:h",
            ["log=", "help"]
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
            if arg not in LOG.LEVELS:
                print USAGE
                sys.exit(-1)
            LOG.setLevel(arg)

def main(argv):
    parseArgs(argv)
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main(sys.argv[1:])

