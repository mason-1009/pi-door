#!/usr/bin/env python3

import auth
import getpass
import sys

if __name__ == "__main__":
    if len(sys.argv) == 2:
        # load security context
        context = auth.securityContext(sys.argv[1])
        print("Type the username and password when prompted")
        username = input("Username: ")
        context.writeKey(username, getpass.getpass())
        print("Done. Have a nice day")
        sys.exit(0)
    else:
        sys.stderr.write("[Error] incorrect number of command-line arguments\n")
        sys.stderr.write("Usage: ./initauth.py [keyfile]\n")
        sys.exit(1)
