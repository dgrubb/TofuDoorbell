# File: tofuutils.py
# Author: dgrubb
# Date: 02/23/2017

# Functions for providing basic utilities such as logging.

# System modules
import logging

LOG_LEVEL = logging.INFO
FORMAT = "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"

# Instantiate a logger
logger = logging.getLogger(__name__)
logger.basicConfig(format=FORMAT, level=LOG_LEVEL)

LOG = logger

