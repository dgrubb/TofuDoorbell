# File: tofuaudio.py
# Author: dgrubb:
# Date: 02/23/2017

# Provides audio playback functionality.

# System modules
import logging
import os

MODULE = "Tofu Audio"
LOG = logging.getLogger(MODULE)

def scanDirectoryForMusicFiles(directory):
    musicFiles = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".mp3"):
                LOG.debug("{0}".format(file))
                musicFiles.append(file)
    LOG.info("Found {0} .mp3 files in {1}".format(len(musicFiles), directory))
    return musicFiles
