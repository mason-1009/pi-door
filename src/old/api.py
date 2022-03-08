#!/usr/bin/env python3

from flask import *
from flask_httpauth import HTTPBasicAuth

import os
import hashlib

import settings
import physical

import auth
import logger

# function for cleaning byte arrays and decoding as utf-8
# for serialization
def utf8Decode(data):
    if type(data) == bytes:
        return data.decode('utf-8')
    else:
        # object is not byteArray
        # try encoding and decoding again
        return data.encode("utf-8").decode("utf-8")

# initiallize global object dictionary
globalObjects = dict()

# lock-status = True when door is locked
globalObjects["lock-status"] = False
globalObjects["lock-servo-pin"] = 18
globalObjects["lock-object"] = None

# door-status = True when door is closed
globalObjects["door-status"] = False

# create message of the day object
globalObjects["motd"] = "Message of the Day"

# set general settings
globalObjects["debug"] = True
globalObjects["reed-switch-pin"] = 16

globalObjects["lock-object"] = physical.initServo(globalObjects["lock-servo-pin"], globalObjects["debug"])

globalObjects["fcgi-pipe"] = "/tmp/fcgi-pipe.sock"

# start unlocked
physical.unlock(globalObjects["lock-object"], globalObjects["debug"])

# import settings dictionary
globalObjects["settings"] = settings.loadSettings("settings.json")

globalObjects["authContext"] = auth.securityContext("auth.txt")

# try to import pin number from settings.json
if globalObjects["settings"].get("servo-pin-number") != None:
    globalObjects["lock-servo-pin"] = globalObjects["settings"]["servo-pin-number"]

# import debug preference from settings.json
if globalObjects["settings"].get("debug") != None:
    globalObjects["debug"] = globalObjects["settings"]["debug"]

# import reed switch pin number from settings.json
if globalObjects["settings"].get("reed-switch-pin") != None:
    globalObjects["reed-switch-pin"] = globalObjects["settings"]["reed-switch-pin"]

if globalObjects["settings"].get("fcgi-pipe") != None:
    if globalObjects["debug"]:
        logger.log("Loaded fcgi-pipe location from settings.json")
    globalObjects["fcgi-pipe"] = globalObjects["settings"]["fcgi-pipe"]

# set up door reed switch
physical.initReedSwitch(globalObjects["reed-switch-pin"])

# set up app context
API = Flask(__name__)

# HTTP GET request functions
# Auth is required for any function that modifies data
# Auth not required for simple non-critical data

flaskAuthObject = HTTPBasicAuth()

# create authentication test functions from auth.py
# this function returns the hashed password from the auth file
# flask_httpauth hashes the password and compares it to the stored hash
@flaskAuthObject.get_password
def getPasswordHash(username):
    keyPair = flaskAuthObject.getKeypair()
    if username == keyPair["username"]:
        return keyPair["passHash"]
    else:
        return None

@flaskAuthObject.hash_password
def hashPassword(password):
    return hashlib.sha512(password).hexdigest()

@API.route("/")
@API.route("/index.html")
@API.route("/index")
@API.route("/status")
@API.route("/status.html")
def send_statPage():
    return render_template("status.html")

@API.route("/manage")
@API.route("/manage.html")
def send_managepage():
    return render_template("manage.html")

@API.route("/json/door.json")
@API.route("/json/door")
def getDoorStatus():
    # get door and lock status
    globalObjects["door-status"] = physical.readDoorStatus(globalObjects["reed-switch-pin"], debug=globalObjects["debug"])
    if globalObjects["door-status"] != None and globalObjects["lock-status"] != None:
        return jsonify({"door-status": globalObjects["door-status"], "lock-status": globalObjects["lock-status"]})
    elif globalObjects["door-status"] != None and globalObjects["lock-status"] == None:
        return jsonify({"door-status": globalObjects["door-status"], "lock-status": "error"})
    elif globalObjects["door-status"] == None and globalObjects["lock-status"] != None:
        return jsonify({"door-status": "error", "lock-status": globalObjects["lock-status"]})
    else:
        return jsonify({"door-status": "error", "lock-status": "error"})
    if globalObjects["door-status"] == True and globalObjects["lock-status"] == False:
        lockDoor()

@API.route("/json/motd.json")
@API.route("/json/motd")
def getMOTD():
    # get message of the day
    if globalObjects["motd"] != None:
        return jsonify({"motd": utf8Decode(globalObjects["motd"])})
    else:
        return jsonify({"motd": "error"})

@API.route("/json/light.json")
@API.route("/json/light")
def getLightStatus():
    return jsonify({"light-status": "not yet implemented"})

@API.route("/json/temp.json")
@API.route("/json/temp")
def getTemp():
    return jsonify({"room-temperature": "not yet implemented"})

# API functions for setting values or performing actions
# SHOULD REQUIRE AUTHENTICATION

@API.route("/api/authtest", methods=["POST"])
@API.route("/api/authtest.py", methods=["POST"])
@flaskAuthObject.login_required
def authTest():
    return jsonify({"auth": True})

@API.route("/api/setmotd", methods=["POST"])
@API.route("/api/setmotd.py", methods=["POST"])
@flaskAuthObject.login_required
def setMOTD():
    globalObjects["motd"] = utf8Decode(request.data)
    return jsonify({"motd": utf8Decode(globalObjects["motd"])})

@API.route("/api/unlock", methods=["POST"])
@API.route("/api/unlock.py", methods=["POST"])
@flaskAuthObject.login_required
def unlockDoor():
    logger.log("Received signal to unlock door")
    if globalObjects["lock-status"] == True:
        physical.unlock(globalObjects["lock-object"], globalObjects["debug"])
        globalObjects["lock-status"] = False
        logger.log("Unlocked door")
    return jsonify({"lock-status": globalObjects["lock-status"]})

@API.route("/api/lock", methods=["POST"])
@API.route("/api/lock.py", methods=["POST"])
@flaskAuthObject.login_required
def lockDoor():
    logger.log("Received signal to lock door")
    if globalObjects["lock-status"] == False:
        physical.lock(globalObjects["lock-object"], globalObjects["debug"])
        globalObjects["lock-status"] = True
        logger.log("Locked door")
        return jsonify({"lock-status": globalObjects["lock-status"]})

if __name__ == "__main__":
   if globalObjects["debug"] == True:
       logger.log("Starting Flask development server from API.run()")
   API.run(host='0.0.0.0', port=7777)
else:
    if globalObjects["debug"] == True:
        logger.log("Starting application from FastCGI context")
    WSGIServer(API, bindAddress=globalObjects["fcgi-pipe"]).run()
