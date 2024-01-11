"""Module for instance of a Keysight E8257D signal generator

This module contains the functions necessary to control and read data from 
a Keysight E8257D signal generator. It inherits from instrument class.

"""
install_directory = 'Z:\\ann\\'

import sys
if install_directory not in sys.path:
        sys.path.append(install_directory)

import visa
from Data_acquisition.devices.base_instrument import instrument

def numtostr(mystr):
    return '%12.8e' % mystr


class Keysight_E8257D(instrument):
    def __init__(self,
                 addr='TCPIP::192.168.1.66::INSTR',
                 reset=True,
                 verb=True):
        super().__init__(addr, reset, verb)
        self.id()

    def SetFrequency(self, frec):
        mystr = numtostr(frec)
        mystr = 'FREQ:CW ' + mystr
        self.write(mystr)

    def GetFrequency(self):
        mystr = 'FREQ:CW?'
        pp = self.query(mystr)
        pp = float(pp)
        return pp

    def SetPower(self, x):
        mystr = numtostr(x)
        mystr = 'SOUR:POW ' + mystr
        self.write(mystr)

    def GetPower(self):
        mystr = 'SOUR:POW?'
        pp = self.query(mystr)
        pp = float(pp)
        return pp

    def SetPowerOn(self):
        self.write('OUTP ON')

    def SetPowerOff(self):
        self.write('OUTP OFF')

    def get_reference(self):
        '''
        gets the 10 MHz reference source
        '''
        bla = self.query(':SOURce:ROSCillator:SOURce?')
        print(bla)

    def GetMetadataString(self):  #Should return a string of metadata adequate to write to a file
        pass

    def EXTref(self):
        self.write('ROSC:SOUR EXT')

    def INTref(self):
        self.write('ROSC:SOUR INT')

    def trig(self):
        self._gpib.write(':INIT')

    def idn(self):
        return(self._gpib.query("*IDN?"))