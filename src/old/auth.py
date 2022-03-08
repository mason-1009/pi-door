#!/usr/bin/env python3

import os
import json
import hashlib
import logger

class securityContext:

    keyFile = None

    loadedAuth = dict()
    loadedAuth["username"] = None
    loadedAuth["passHash"] = None

    def __init__(self, filepath):
        self.keyFile = filepath

    def setKeyFile(self, filename):
        self.keyFile=filename
        logger.log("Setting key file path as "+filename)

    def loadKey(self):
        # try to open the key file
        try:
            logger.log("Loading keyfile data")
            fileObj = open(self.keyFile, "r")
            fileBuffer = fileObj.read()
            fileObj.close()
        except FileNotFoundError:
            logger.log("There was an error opening the keyfile")
            return False

        # load data
        parsed = json.loads(fileBuffer)
        # set cache to loaded data
        self.loadedAuth["username"] = parsed["username"]
        self.loadedAuth["passHash"] = parsed["passHash"]
        return True

    def rewriteKey(self, jsonText):
        logger.log("Opening keyfile for wiping and editing")
        fileObj = open(self.keyFile, "w")
        logger.log("Writing keyfile")
        fileObj.write(jsonText)
        fileObj.flush()
        fileObj.close()

        # reload key
        self.loadKey()

    def hashPassword(self, password):
        # converts plain text password to hash for storage
        if type(password) == bytes:
            passHash = hashlib.sha512(password).hexdigest()
        else:
            passHash = hashlib.sha512(password.encode()).hexdigest()
        return passHash
    
    def writeKey(self, username, password):
        keyObj = dict()
        keyObj["username"] = username
        keyObj["passHash"] = self.hashPassword(password)
        self.rewriteKey(json.dumps(keyObj))
    
    def getKeypair(self):
        return self.loadedAuth
        
    def comparePassInput(self, username, password):
        # assemble auth dictionary
        keyObj = dict()
        keyObj["username"] = username
        keyObj["passHash"] = self.hashPassword(password)

        usernamePass = False
        passwordPass = False

        if keyObj["username"] == self.loadedAuth["username"]:
            usernamePass = True

        if keyObj["passHash"] == self.loadedAuth["passHash"]:
            passwordPass = True
        else:
            # send alert to console if user fails auth
            logger.log("User "+keyObj["username"]+" failed to authenticate - wrong password!")

        # return dictionary containing auth status
        return {"username": usernamePass, "password": passwordPass}
