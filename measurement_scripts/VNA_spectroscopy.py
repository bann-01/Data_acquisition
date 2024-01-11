# VNA spectroscopy.

# Principle sweep : probe frequency.
# Principle meas  : S21 parameters - Re(S21), Im(S21).
# Aux sweep       : powers or frequencies of aux tones for examples.

import sys
sys.path.append('Z:\\ann\\')

import pyvisa
import serial

import numpy as np
from scipy.optimize import curve_fit

from bitstring import BitArray,BitStream
import re
import json 
import requests
import pickle
import time
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation as FA

from bann_labtools.devices.devices_GPIB as E5071C 
import bann_labtools.devices.BF_thermometer as BF_thermometer 


# Define VNA. Can be other models.
VNA  = E5071C(21) 


class VNA_aux_sweeper:
        '''
        in preparation.
        '''
    def __init__(self):
        self.numswp  = 0
        self.instr_list = []
        self.range_list = []
    def add_aux_sweep(self, sweep_device, sweep_range):
        self.numswp = self.numswp + 1
        self.instr_list.append(sweep_device)
        self.range_list.append(sweep_range)


class VNA_aux_constant:
        '''
        in preparation.
        '''
    def __init__(self):
        self.numconst  = 0
        self.instr_list = []
        self.value_list = []
    def add_aux_sweep(self, const_device, const_value):
        self.numswp = self.numswp + 1
        self.instr_list.append(const_device)
        self.value_list.append(const_value)


class VNA_spec:
    
    def __init__(self, VNA, FilePath, AuxSweeper = None, AuxConst = None, Thermo_ip = '192.168.0.1', Temperalog = True, Tempersens = True):
        '''
        in preparation.
        
        kwargs['temperature'] : Manual temperature input, only needeed when Tempersens = False.
        
        '''
       
        thermometer = BF_thermometer(ip = Thermo_ip , url='/channel/measurement/latest', timeout = 10)

        self.vna   = VNA

        if Temperalog == True:
            if Tempersens == True:
                self.temperature = thermometer.temperature_log(sensor_number = 6, ip = Thermo_ip)
            else:
                self.temperature = kwargs['temperature']
        else:
            self.temperature = None
        self.filepath     = FilePath
        self.aux_sweeper  = AuxSweeper

    def SetVNA(self, Avg = True, ProbeFreqStart = 4e9, ProbeFreqStop = 5e9, NumPts = 101,  VNApower = 0, Navg = 1):

        self.vna.PowerOn();self.vna.SetPower(VNApower)
        self.vna.SetStart(ProbeFreqStart);self.vna.SetEnd(ProbeFreqStop) 
        self.vna.SetPoints(num_pts);self.vna.SetIFBW(IF)
        self.vna.SetContinuous(False);self.vna.SetAvgOn();self.vna.SetAvgCle();self.vna.SetAvgCount(Navg)

    def S21Meas(Save = True, Note = True, Visualization = True,  **kwargs):

     	Navg = self.vna.GetAvgCount()

        if self.aux_sweeper = None:
            for in range(Navg):
                self.vna.Trigger()

            time.sleep((1.1/IF*self.vna.GetPoints()+0.1)*self.vna.GetAvgCount())
            yyre, yyim = self.vna.GetData()
         	self.vna.PowerOff()

            measurement_result                = {}
            measurement_result['freq']        = self.vna.GetFrequency()
            measurement_result['S21 re']      = yyre
            measurement_result['S21 Im']      = yyim

        else:

        measurement_condition                = {}
        measurement_condition['Type']        = 'VNA_S21_measurement'
        measurement_condition['Power']       = self.vna.GetPower()
        measurement_condition['IFBW']        = self.vna.GetIFBW()
        measurement_condition['Avg']         = self.vna.GetAvgCount()
        measurement_condition['temperature'] = self.temperature

        if 'memo' in kwargs.key:
                measurement_condition['memo']  = kwargs['memo']
        else:
                measurement_condition['memo']  = None

        if save == True:
            now    = datetime.now()
            prefix = now.strftime('%Y%m%d_%H%M%S')
            title   = '{}_{}_{}_GHz_{}_dBm_'.format(prefix, np.round(self.vna.GetStart(),5), np.round(self.vna.GetEnd(),5), np.round(self.vna.GetPower(),3))

            outfile = open(self.filepath + prefix + title + memo +'.dat', 'wb'); pickle.dump(measurement_result, outfile)
            outfile.close()

            outfile = open(self.filepath + prefix + title + memo +'.pickle', 'wb'); pickle.dump(measurement_condition, outfile)
            outfile.close()


        if Visualization == True:
            fig,axs = plt.subplots(2,1)
            plt.subplots_adjust(hspace = 0.4)
            axs[0].plot(freq/1e9,20*np.log10(amp)); axs[0].set_xlabel('Frequency (GHz)'); axs[0].set_ylabel('S21 (dB)'); 
            axs[1].plot(freq/1e9,np.unwrap(2*angle)/2); axs[1].set_xlabel('Frequency (GHz)'); axs[1].set_ylabel('S21 angle (rad)')
            plt.savefig(prefix + title + memo +'.png', dpi = 300)

        if Note == True:

            measurement_condition['Type']        = 'VNA_S21_measurement'
            measurement_condition['Power']       = self.vna.GetPower()
            measurement_condition['IFBW']        = self.vna.GetIFBW()
            measurement_condition['Avg']         = self.vna.GetAvgCount()
            measurement_condition['temperature'] = self.temperature

            outfile = open(self.filepath + prefix + title + memo +'.dat', 'wb'); pickle.dump(measurement_result, outfile)
            outfile.close()

       return measurement_result

    def save

