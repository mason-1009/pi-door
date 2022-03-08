#!/usr/bin/env python3

import os
import serial
import time
import binascii

class command:
    
    command = bytearray(2)
    parameter = bytearray(4)

    def __init__(self, commandValue=None, parameterValue=None):

        # don't set command value if equal to None
        if not(commandValue == None):
            # break command into bytes
            self.command[0] = commandValue & 0xFF
            self.command[1] = (commandValue >> 8) & 0xFF


        # don't set parameter value if equal to None
        if not(parameterValue == None):
            # break parameter into bytes
            self.parameter[0] = parameterValue & 0xFF
            self.parameter[1] = (parameterValue >> 8) & 0xFF
            self.parameter[2] = (parameterValue >> 16) & 0xFF
            self.parameter[3] = (parameterValue >> 24) & 0xFF

    def assemble(self):

        packet = bytearray(12)

        # static start codes make up the first 2 bytes
        packet[0] = 0x55
        packet[1] = 0xAA
        
        # device ID makes second byte pair
        packet[2] = 0x01
        packet[3] = 0x00

        # concatenate parameter and command bytes
        packet[4] = self.parameter[0]
        packet[5] = self.parameter[1]
        packet[6] = self.parameter[2]
        packet[7] = self.parameter[3]

        packet[8] = self.command[0]
        packet[9] = self.command[1]

        # sum packet and break for checksum bytes
        checksum = sum(packet)

        # append checksum byte and return packet
        packet[10] = checksum & 0xFF
        packet[11] = (checksum >> 8) & 0xFF

        return packet
    
class response:
    
    response = bytearray(2)
    parameter = bytearray(4)

    acknowledge = False

    def __init__(self, _buffer):
        
        # fill parameter from _buffer
        self.parameter[0] = _buffer[4]
        self.parameter[1] = _buffer[5]
        self.parameter[2] = _buffer[6]
        self.parameter[3] = _buffer[7]

        # fill response from _buffer
        self.response[0] = _buffer[8]
        self.response[1] = _buffer[9]

    def assembleParameter(self):
        
        value = 0

        value = self.parameter[0]
        value = value + (self.parameter[1] << 8)
        value = value + (self.parameter[2] << 16)
        value = value + (self.parameter[3] << 24)

        return value
    
    def assembleResponse(self):

        value = 0

        value = self.parameter[0]
        value = value + (self.parameter[1] << 8)

        return value


class data:
    
    data = bytearray()

    def __init__(self, _buffer):
        
        if not(_buffer == None):
            
            # fill data from _buffer
            for byte in _buffer[4:-2]:
                data.append(byte)
            
            return data

        else:
                
            return None
                
class GT511C3:
    
    connection = serial.Serial()

    def __init__(self, device, baudrate=9600):
        
        # configure connection and open
        self.connection.port = device
        self.connection.baudrate = baudrate
        self.connection.open()

    def serialSend(self, packet):
        
        if not self.connection is None:
            self.connection.write(packet)
            return True
        else:
            return False

    def serialListen(self):
        
        _buffer = self.connection.read

    def init(self):
        
        packet = command(commandValue=0x01, parameterValue=1)
        self.serialSend(packet.assemble())

    def close(self):
        
        packet = command(commandValue=0x02, parameterValue=0)
        self.serialSend(packet.assemble())

    def setLED(self, status=True):
        
        packet = command(commandValue=0x12)

        if status:
            packet.parameter[0] = 0x01
        else:
            packet.parameter[0] = 0x00

        packet.parameter[1] = 0x00
        packet.parameter[2] = 0x00
        packet.parameter[3] = 0x00

        self.serialSend(packet.assemble())

    def getFingerPressed(self):
        
        packet = command(commandValue=0x26)

