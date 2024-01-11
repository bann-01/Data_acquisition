import time
from datetime import datetime
import numpy as np
import stlab
from stlab.devices import autodetect_instrument
from stlab.devices.Keysight_E5080A import Keysight_E5080A
from stlab.devices.Keysight_N9010B import Keysight_N9010B
from stlab.devices.Keysight_N5183B import Keysight_N5183B
from stlab.devices.Keysight_E8257D import Keysight_E8257D
from Metafile_generator import metafile_generator

filename = 'VNA_OMIT_PTon'

f_res    = 6.570145e9        #6.5214575e9  #6.383e9      #6.24088e9
f_mem    = 0.9791351e6 + 16.5e3       #0.9790654e6  #1.0030345e6  #1.010703e6

# VNA parameters
freq_center = f_res
span        = 200
freq_start  = freq_center - span/2
freq_stop   = freq_center + span/2

power_vna   = 0
ifbw        = 10
nr_sp       = 1001
nr_tr       = 1
nr_avg      = 1

# Generator parameters
gen_inst    = 'PSG'
freq_gen    = f_res - f_mem
power_gen   = 15

parameters = []
if gen_inst == 'MXG':
    parameters.append('generator: \t'          + 'MXG')
elif gen_inst == 'PSG':
    parameters.append('generator: \t'          + 'PSG')
parameters.append('generator freq: \t'         + str(freq_gen))
parameters.append('generator power: \t'        + str(power_gen))
parameters.append('VNA freq center: \t'        + str(freq_center))
parameters.append('VNA span: \t'               + str(span))
parameters.append('VNA power: \t'              + str(power_vna))
parameters.append('VNA IFBW: \t'               + str(ifbw))
parameters.append('VNA number of points: \t'   + str(nr_sp))
parameters.append('VNA number of traces: \t'   + str(nr_tr))
parameters.append('VNA number of averages: \t' + str(nr_avg))
parameters.append('temperature: \t'            + '50 mK')
parameters.append('Lake Shore P gain: \t'      + '2.0')
parameters.append('Lake Shore I gain: \t'      + '20 sec')
parameters.append('Lake Shore D gain: \t'      + '10 sec')

# Info for data explorer
parameters_dexplore = {}
parameters_dexplore['measurement_type'] = 'traces'
parameters_dexplore['freq_start']       = freq_start
parameters_dexplore['freq_stop']        = freq_stop
parameters_dexplore['nr_sp']            = nr_sp
parameters_dexplore['nr_traces']        = nr_tr

# VNA
vna = Keysight_E5080A(addr='TCPIP::172.19.20.5::5025::SOCKET', reset=True, verb=True)
vna.ClearAll()
vna.AddTraces('S21')
vna.SetContinuous(False)
vna.SetRange(freq_start, freq_stop)
vna.SetPower(power_vna)
vna.SetIFBW(ifbw)
vna.SetPoints(nr_sp)
vna.SetPowerOn()
time.sleep(.5)

# Spectrum analyser
sa = Keysight_N9010B(addr='USB0::0x2A8D::0x1C0B::MY56080582::0::INSTR', reset=True)
sa.SetMode('BASIC')
sa.SetReference('EXT')
time.sleep(.5)

# Generator
gen1 = Keysight_N5183B(addr='TCPIP::172.19.20.14::INSTR', reset=True)          # MXG
gen1.EXTref()
if gen_inst == 'MXG':
    gen1.setCWfrequency(freq_gen)
    gen1.setCWpower(power_gen)
    gen1.RFon()
elif gen_inst == 'PSG':
    gen2 = Keysight_E8257D(addr='TCPIP::172.19.20.15::INSTR', reset=True)      # PSG
    gen2.EXTref()
    gen2.setCWfrequency(freq_gen)
    gen2.setCWpower(power_gen)
    gen2.RFon()
time.sleep(2)

# Measure
Data    = {}
t_start = datetime.now()

for i in range(nr_tr):
    print('trace: ' + str(i))
    output = vna.MeasureScreen(N_averages=nr_avg)
    vna.AutoScaleAll()

    Data['Frequency (Hz)']     = output['Frequency (Hz)'].tolist()
    Data['S21 Re ()']          = output['S21re ()'].tolist()
    Data['S21 Im ()']          = output['S21im ()'].tolist()
    Data['S21 power (dB)']     = output['S21dB (dB)'].tolist()
    Data['S21 phase (rad)']    = output['S21Ph (rad)'].tolist()

    if i == 0:
        myfile = stlab.newfile('', filename, Data.keys())
    stlab.savedict(myfile, Data, f='%.15e')

t_stop = datetime.now()
parameters.append('time start: \t' + str(t_start))
parameters.append('time stop: \t'  + str(t_stop))
metafile_generator(myfile, parameters, parameters_dexplore, Data)

vna.SetPowerOff()
vna.close()
sa.close()
gen1.RFoff()
gen1.close()
if gen_inst == 'PSG':
  gen2.RFoff()
  gen2.close()
myfile.close()


