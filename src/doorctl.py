#!/usr/bin/env python3

import application
from optparse import OptionParser
import logger

if __name__ == "__main__":
    parser = OptionParser()

    argumentOptions = None
    arguments = None

    parser.add_option("-d", "--daemon", dest="daemonize", help="Run program as daemon (runs in terminal by default", action="store_true", default=False)

    (argumentOptions, arguments) = parser.parse_args()

    args = vars(argumentOptions)
    application.externStart(args["daemonize"])

else:
    logger.log("An error has occured")
    logger.log("doorctl.py must be run as main program")
