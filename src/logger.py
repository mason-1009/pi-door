#!/usr/bin/env python3

import time

def log(text):
    # concat log text with time
    print('<'+time.ctime(time.time())+'> '+"[Debug] "+text)
