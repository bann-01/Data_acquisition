import pyvisa
import serial
import time
import numpy as np
from bitstring import BitArray,BitStream
import json 
import requests
import pickle
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.optimize import curve_fit
import re
from matplotlib.animation import FuncAnimation as FA

def numtostr(mystr):
    return '%20.15e' % mystr

### visa controlled instruments
rm = pyvisa.ResourceManager()      


# Agilent PXA N9030A spectrum analyzer
class PXA:
    def __init__(self, addr = 'GPIB1::24::INSTR'):
        self._gpib = rm.open_resource(addr)
        self._gpib.timeout = 20000
    
    def __del__(self):
        self._gpib.close()
    
    def idn(self):
        return(self._gpib.query("*IDN?"))
    
    def SaveTrace(self,filename):
        self._gpib.write(':MMEM:STOR:TRAC:DATA TRACE1,\"C:\\Temp\\trace1.csv\"')
        data = self._gpib.query(':MMEMory:DATA? \"C:\\Temp\\trace1.csv\"')
        with open(filename,'w') as f:
            f.write(data.replace('\r',''))
    
    def SaveState(self, filename):
        self._gpib.write(':MMEM:STOR:STAT \"C:\\Temp\\state1.state\"')
        self._gpib.write(':MMEMory:DATA? \"C:\\Temp\\state1.state\"')
        state = self._gpib.read_raw()
        with open(filename,'wb') as f:
            f.write(state)
    
    def LoadState(self, filename):
        with open(filename,'rb') as f:
            state = f.read()
            self._gpib.write_binary_values(
                ':MMEM:DATA \"C:\\Temp\\state1.state\",',state)
            self._gpib.write(':MMEM:LOAD:STAT \"C:\\Temp\\state1.state\"')
    
    def center(self,freq): # freq in Hz
        self._gpib.write(':FREQ:CENT '+str(freq)+' Hz')
    
    def span(self,freq): # freq in Hz
        self._gpib.write(':FREQ:SPAN '+str(freq)+' Hz')
    
    def align(self): # align now
        self._gpib.write(':CAL')
    
    def restart(self): # restart measurement
        self._gpib.write(':INIT:REST')
    
    def recall(self,reg): # recall state
        self._gpib.write('*RCL '+str(reg))
 
### Agilent PSG E8257D E8267D signal generator.
class PSG:
    def __init__(self, addr = 'GPIB1::16::INSTR'):
        self._gpib = rm.open_resource(addr)

    def __del__(self):
        self._gpib.close()

    def idn(self):
        return(self._gpib.query("*IDN?"))

    def trig(self):
        self._gpib.write(':INIT')

    def SetFrequency(self, f): # f in Hz
        self._gpib.write(":FREQ "+str(f)+"HZ")

    def SetPower(self, lv): # lv in dBm
        self._gpib.write(":POW "+str(lv)+"DBM")

    def SetPowerOn(self): 
        self._gpib.write(":OUTP ON")

    def SetPowerOff(self):
        self._gpib.write(":OUTP OFF")

    def GetFrequency(self): # freq in Hz
        f = self._gpib.query(":FREQ:CW?")
        return(np.float_(np.fromstring(f,dtype=float,sep=' ')))

    def GetPower(self):
        mystr = 'SOUR:POW?'
        p = self._gpib.query(mystr)
        p = float(pp)
        return p
    
    def IQon(self):
        '''
        turns on vector modulation.
        Caution: without IQ input the source doesn't output anything!
        '''
        self._gpib.write(':WDM:STATe ON')
        result = 'IQ_on'
        return print(result)
    
    def IQoff(self):
        self._gpib.write(':WDM:STATe OFF')
        result = 'IQ_off'
        return print(result)
    
    def IQAD_on(self):
        self._gpib.write(':WDM:IQAD ON')
        result = 'IQAD_on'
        return print(result)    
    
    def IQAD_off(self):
        self._gpib.write(':WDM:IQAD OFF')
        result = 'IQAD_off'
        return print(result)
    
    def IQAD_Ioffset(self,value):        
        if not value <= 5e4 and value >= -5e4:
            raise ValueError('Please check the value range!')        
        self._gpib.write(':WDM:IQAD:IOFF '+str(value)+'MV')

    def IQAD_Qoffset(self,value):        
        if not value <= 5e4 and value >= -5e4:
            raise ValueError('Please check the value range!')        
        self._gpib.write(':WDM:IQAD:QOFF '+str(value)+'MV')
    
    def IQAD_skew(self, value):
        if not value<=10 and value>=-10:
            raise ValueError('Please check the value range!')        
        self._gpib.write(':WDM:IQADjustment:QSKew '+str(value))
   
    def EXTref(self):
        self._gpib.write('ROSC:SOUR EXT')
    
    def INTref(self):
        self._gpib.write('ROSC:SOUR INT')

        
## Keysight 32120A signal generator. As a trigger source. 
class Keysight_34120A:
    def __init__(self, addr = 'GPIB1::10::INSTR'):
        self._gpib = rm.open_resource(addr)
    
    def __del__(self):
        self._gpib.close()
    
    def trig(self):
        self._gpib.write('TRIG:SOUR IMM')
    
    def trig_cycle(self, value):
        self._gpib.write('BM:NCYCles'+str(value))
               


### Keysight E5071C vector network analyzer
class E5071C:
    
    def __init__(self, addr = 'GPIB1::17::INSTR'):
        self._gpib = rm.open_resource(addr)
    
    def __del__(self):
        self._gpib.close()
    
    def idn(self):
        return(self._gpib.query('*IDN?'))
    
    def GetData(self):           # take s21 data in RAM.        
        yy = self._gpib.query(':CALC:DATA:SDAT?')
        yy = np.asarray([float(xx) for xx in yy.split(',')])
        yyre = yy[::2]
        yyim = yy[1::2]
        return yyre, yyim
    
    def Trigger(self):
        self._gpib.write(':INIT:CONT OFF')
        self._gpib.write(':INIT')

    def SetAvgCle(self):
        self._gpib.write('SENS:AVER:CLE')

    def GetFrequency(self):
        freq = self._gpib.query('CALC:X?')
        freq = np.asarray([float(xx) for xx in freq.split(',')])
        return freq

    def GetAvgCount(self):
        return int(self._gpib.query('SENS:AVER:COUN?'))

    def SetAvgCount(self, N_averages = 1):
        self._gpib.write('SENS:AVER:COUN %d' % N_averages)
        
    def SetAvgOn(self):
        self._gpib.write('SENS:AVER:STAT ON')
 
    def SetAvgOff(self,state = False):
        self._gpib.write('SENS:AVER:STAT OFF')

    def SetPower(self,p):
        #p = np.array2string(p)
        p = numtostr(p)
        self._gpib.write('SOUR:POW ' + p)

    def GetPower(self):
        self._gpib.write('SOUR:POW ' + p)

    def SetCenter(self,p):
        #p = np.array2string(p)
        p = numtostr(p)
        self._gpib.write('SENS:FREQ:CENT ' + p)

    def SetSpan(self,p):
        #p = np.array2string(p)
        p = numtostr(p)
        self._gpib.write('SENS:FREQ:SPAN ' + p)

    def SetStart(self,p):
        #p = np.array2string(p)
        p = numtostr(p)
        self._gpib.write('SENS:FREQ:START ' + p)

    def SetEnd(self,p):
        #p = np.array2string(p)
        p = numtostr(p)
        self._gpib.write('SENS:FREQ:STOP ' + p)

    def SetIFBW(self,p):
        #p = np.array2string(p)
        p = numtostr(p)
        self._gpib.write('SENS:BWID ' + p )

    def GetIFBW(self):
        p = self._gpib.query('SENS:BWID?')
        p = float(p)
        return p

    def SetPowerOff(self):
        self._gpib.write('OUTP 0')
        return

    def SetPowerOn(self):
        self._gpib.write('OUTP 1')
        return

    def SetPoints(self, x):
        mystr = '%d' % x
        mystr = 'SENS:SWE:POIN ' + mystr
        self._gpib.write(mystr)

    def GetPoints(self):
        mystr = 'SENS:SWE:POIN?'
        p = self._gpib.query(mystr)
        p = int(p)
        return p

    def SetContinuous(self, var=True):
        if var == True:
            self._gpib.write('INIT:CONT 1')  #Turn on continuous mode
        elif var == False:
            self._gpib.write('INIT:CONT 0')  #Turn off continuous mode