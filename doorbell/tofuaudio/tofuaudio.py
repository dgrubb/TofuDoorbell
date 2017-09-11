# File: tofuaudio.py
# Author: dgrubb
# Date: 02/23/2017

# Provides audio playback functionality.

# System modules
import logging
import os
from random import randint

MODULE = "Tofu Audio"
LOG = logging.getLogger(MODULE)

###############################################################################
# Worker functions
###############################################################################

def scanDirectoryForMusicFiles(directory):
    musicFiles = []
    # Walk the target directory looking for .mp3 files
    try:
        LOG.debug("Searching for .mp3 files in directory: {0}".format(directory))
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".mp3"):
                    LOG.debug("Found mp3 file: {0}".format(file))
                    musicFiles.append(file)
    except:
        LOG.error("Error scanning directory: {0}".format(directory))
    LOG.info("Found {0} .mp3 files in {1}".format(len(musicFiles), directory))
    return musicFiles

###############################################################################
# Classes
###############################################################################

class TofuAudioPlayer():

    playlist = []
    playing = False

    def __init__(self, musicList):
        # N.B: using the list() function ensures a true clone is created, rather
        # than accidentally storing a reference to the original musicList
        self.playlist = list(musicList)

    def isPlaying(self):
        return self.playing

    def playRandom(self):
        play(randint(0, len(playlist)))

    def play(self, index):
        if index < 0 or index > len(playlist):
            LOG.error("Requested index [ {0} ] outside playlist range.".format(index))
            return False
        if playing:
            self.stop()

    def stop(self):
        playing = False

