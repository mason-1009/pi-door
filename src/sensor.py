#!/usr/bin/env python3

import logger
import json
import serial

import threading
import time

# define constants
CELCIUS = 0
FAHRENHEIT = 1

class Sensor():

    arduinoSensor = None
    updateThread = None

    temperature = None
    humidity = None

    def updateThread(self):

        if self.arduinoSensor == None:
            logger.log("[ERROR] Arduino sensor array cannot be detected, sensor array will not function properly")
        else:
            logger.log("Arduino sensor array is initiallized, continuing...")
            logger.log("Setting sensor update loop")

            while True:

                try:

                    # read line and parse
                    parsed = json.loads(self.arduinoSensor.readline().decode("utf-8").strip())

                    # save parsed data
                    self.temperature = parsed["temperature"]
                    self.humidity = parsed["humidity"]

                except json.JSONDecodeError:

                    logger.log("[ERROR] JSON from Arduino sensor could not be parsed, retrying...")

    def __init__(self, port, baudrate):

        # create sensor object
        # device and baud are set from settings.json
        self.arduinoSensor = serial.Serial(port, baudrate)

        # enable loop update threading
        self.updateThread = threading.Thread(target=self.updateThread)

        # start update threading
        self.updateThread.start()

    def getTemperature(self, tempFormat=0):
        if tempFormat==0:
            return self.temperature
        elif tempFormat==1:
            return (self.temperature*(9.0/5.0)+32)
        else:
            return self.temperature

    def getHumidity(self):
        return self.humidity
    
