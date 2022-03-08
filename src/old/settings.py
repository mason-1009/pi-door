#!/usr/bin/env python3

import json
import sys
import logger

def loadSettings(filename, debug=True):
    try:
        if debug:
            logger.log("Opening file: "+filename)
        settingsFile=open(filename, "r")
    except:
        if debug:
            logger.log("Failed to open "+filename)
        return None
    # assuming no exception, operation succeeded
    if debug:
        logger.log("File operation succeeded, parsing JSON settings")
    settingsDict=None
    try:
        settingsDict=json.loads(settingsFile.read())
    except:
        if debug:
            logger.log("Settings file could not be loaded")
        sys.stderr.write("Critical error: file could not be loaded")
        return None
    return settingsDict
