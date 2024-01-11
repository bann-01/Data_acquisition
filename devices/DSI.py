"""Module for instance of a DS instrument RF synthesizer.

"""
import serial

install_directory = 'Z:\\ann\\'

import sys
if install_directory not in sys.path:
        sys.path.append(install_directory)

badCommandResponse = b'[BADCOMMAND]\r\n'

class DSI():
    def __init__(self,
                 addr="COM4",
                 timeout=1):
        self.ser = serial.Serial(addr, 115200, timeout)
        self.ser.open()

    def OpenCheck(self):
        if self.ser.isOpen():             # make sure port is open
            print(self.ser.name + ' open...') # tell the user we are starting

    def SetFrequency(self, frec):
        frec = 'FREQ:CW {}GHz\n'.format(frec)
        bfrec = bytes(frec, 'utf-8')
        self.ser.write(bfrec)
        self.ser.readline()

    def GetFrequency(self):
        frec = 'FREQ:CW?'
        bfrec = bytes(frec, 'utf-8')
        ff    = self.ser.write(bfrec)
        return ff

    def SetPower(self, power = 1.0):
        mystr = 'POWER {}'.format(power)
        bpower = bytes(power, 'utf-8')
        self.ser.write(bpower)
        self.ser.readline()

    def GetPower(self):
        power = 'POWER? \n'
        bpower = bytes(power, 'utf-8')
        a      = self.ser.write(bpower)
        return a

    def SetPowerOn(self):
        on = 'OUTP:STAT ON'
        bon = bytes(on, 'utf-8')
        self.ser.write(bon)
        self.ser.readline()

    def SetPowerOff(self):
        off = 'OUTP:STAT OFF'
        bon = bytes(off, 'utf-8')
        self.ser.write(bon)
        self.ser.readline()