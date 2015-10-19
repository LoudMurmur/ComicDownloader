#!/usr/bin/env python
# --*-- encoding: iso-8859-1 --*--

import os
import logging.config
import util

logging.config.fileConfig(os.path.join(util.getProjectPath(), "config/logger.conf"))

def getLogger(loggerName):
    """Get a configured logger
        -loggerName : a string
    """
    return logging.getLogger(loggerName)
