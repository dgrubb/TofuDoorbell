# File: tofuaudio.py
# Author: dgrubb
# Date: 02/23/2017

# Provides audio playback functionality.

# System modules
import logging
import os
import subprocess
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

    directory = ""
    playlist = []
    playing = False
    player = None

    def __init__(self, musicList, musicDir):
        LOG.info("Initialising TofuAudio player")
        # N.B: using the list() function ensures a true clone is created, rather
        # than accidentally storing a reference to the original musicList
        self.playlist = list(musicList)
        if musicDir[-1:] != "/":
            self.directory = musicDir + "/"
        else:
            self.directory = musicDir

    def closeAudio(self):
        LOG.info("Shutting down audio player")
        self.stop()

    def isPlaying(self):
        return self.playing

    def playRandom(self):
        self.play(randint(0, len(self.playlist)-1))

    def play(self, index):
        if index < 0 or index > len(self.playlist)-1:
            LOG.error("Requested index [ {0} ] outside playlist range.".format(index))
            return False
        if self.playing:
            self.stop()
        LOG.info("Playing audio clip: {0}".format(self.playlist[index]))
        try:
            self.player = subprocess.Popen(
                ["mplayer", self.directory + self.playlist[index]],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.playing = True
        except:
            LOG.error("Error starting mplayer")

    def stop(self):
        LOG.debug("Stopping audio playback")
        if self.player:
            self.player.stdin.write("q")
            self.player = None
        self.playing = False

