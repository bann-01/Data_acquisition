"""Module for instance of a R&S SGS100A RF source

This module contains the functions necessary to control and read data from 
a R&S SGS100A RF source. It inherits from instrument class.

"""

install_directory = 'Z:\\ann\\'

import sys
if install_directory not in sys.path:
        sys.path.append(install_directory)

import visa
from Data_acquisition.devices.base_instrument import instrument

def numtostr(mystr):
    return '%12.8e' % mystr


class RS_SGS100A(instrument):
    def __init__(self,
                 addr='TCPIP::192.168.1.43::INSTR',
                 reset=True,
                 verb=True):
        super().__init__(addr, reset, verb)
        # self.id()

    def SetFrequency(self, frec):
        # mystr = numtostr(frec)
        mystr = 'FREQ:CW %d' % frec
        self.write(mystr)

    def GetFrequency(self):
        mystr = 'FREQ:CW?'
        pp = self.query(mystr)
        pp = float(pp)
        return pp

    def SetPhase(self, phase):
        mystr = 'SOUR:PHAS %.2f' % phase
        self.write(mystr)

    def Getphase(self):
        mystr = 'SOUR:PHAS?'
        pp = self.query(mystr)
        pp = float(pp)
        return pp

    def SetPower(self, x):
        mystr = numtostr(x)
        mystr = 'SOUR:POW:POW ' + mystr
        self.write(mystr)

    def GetPower(self):
        mystr = 'SOUR:POW:POW?'
        pp = self.query(mystr)
        pp = float(pp)
        return pp

    def SetPowerOn(self):
        self.write('OUTP ON')

    def SetPowerOff(self):
        self.write('OUTP OFF')

    def IQon(self):
        '''
        turns on vector modulation.
        Caution: without IQ input the source doesn't output anything!
        '''
        self.write('IQ:STATe ON')

    def IQoff(self):
        self.write('IQ:STATe OFF')

    def EXTref(self):
        self.write('SOUR:ROSC:SOUR EXT')

    def INTref(self):
        self.write('SOUR:ROSC:SOUR INT')

    def GetMetadataString(
            self
    ):  #Should return a string of metadata adequate to write to a file
        pass

    def trig(self):
        self._gpib.write(':INIT')

    def idn(self):
        return(self._gpib.query("*IDN?"))