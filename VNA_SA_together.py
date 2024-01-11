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

# print('SCRIPT STARTED')
# print(datetime.now())
# time.sleep(1800)
# print('START MEASURING')
# print(datetime.now())

##########################################################
# MEASUREMENT 0 - WIDE SPAN
##########################################################

print('MEASUREMENT 0 - WIDE SPAN')

filename = 'VNA_wide_span_PTon'

f_res    = 6.570145e9        #6.5214575e9  #6.383e9      #6.24088e9
f_mem    = 0.9791351e6       #0.9790654e6  #1.0030345e6  #1.010703e6

# VNA parameters
freq_center = f_res
span        = 8e9
freq_start  = freq_center - span/2
freq_stop   = freq_center + span/2

power_vna   = 0
ifbw        = 100
nr_sp       = 10001
nr_tr       = 1
nr_avg      = 1

# Generator parameters
# gen_inst    = 'PSG'
# freq_gen    = f_res - f_mem
# power_gen   = -18

parameters = []
parameters.append('MEASUREMENT 0 - WIDE SPAN')
# if gen_inst == 'MXG':
#     parameters.append('generator: \t'          + 'MXG')
# elif gen_inst == 'PSG':
#     parameters.append('generator: \t'          + 'PSG')
# parameters.append('generator freq: \t'         + str(freq_gen))
# parameters.append('generator power: \t'        + str(power_gen))
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
# sa = Keysight_N9010B(addr='USB0::0x2A8D::0x1C0B::MY56080582::0::INSTR', reset=True)
# sa.SetMode('BASIC')
# sa.SetReference('EXT')
# time.sleep(.5)

# Generator
# gen1 = Keysight_N5183B(addr='TCPIP::172.19.20.14::INSTR', reset=True)          # MXG
# gen1.EXTref()
# if gen_inst == 'MXG':
#     gen1.setCWfrequency(freq_gen)
#     gen1.setCWpower(power_gen)
#     gen1.RFon()
# elif gen_inst == 'PSG':
#     gen2 = Keysight_E8257D(addr='TCPIP::172.19.20.15::INSTR', reset=True)      # PSG
#     gen2.EXTref()
#     gen2.setCWfrequency(freq_gen)
#     gen2.setCWpower(power_gen)
#     gen2.RFon()
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
# sa.close()
# gen1.RFoff()
# gen1.close()
# if gen_inst == 'PSG':
#   gen2.RFoff()
#   gen2.close()
myfile.close()

time.sleep(30)

##########################################################
# MEASUREMENT 1 - WIDE SPAN
##########################################################

print('MEASUREMENT 1 - WIDE SPAN')

filename = 'VNA_wide_span_PTon'

f_res    = 6.570145e9        #6.5214575e9  #6.383e9      #6.24088e9
f_mem    = 0.9791351e6       #0.9790654e6  #1.0030345e6  #1.010703e6

# VNA parameters
freq_center = f_res
span        = 2e9
freq_start  = freq_center - span/2
freq_stop   = freq_center + span/2

power_vna   = 0
ifbw        = 100
nr_sp       = 10001
nr_tr       = 1
nr_avg      = 1

# Generator parameters
# gen_inst    = 'PSG'
# freq_gen    = f_res - f_mem
# power_gen   = -18

parameters = []
parameters.append('MEASUREMENT 1 - WIDE SPAN')
# if gen_inst == 'MXG':
#     parameters.append('generator: \t'          + 'MXG')
# elif gen_inst == 'PSG':
#     parameters.append('generator: \t'          + 'PSG')
# parameters.append('generator freq: \t'         + str(freq_gen))
# parameters.append('generator power: \t'        + str(power_gen))
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
# sa = Keysight_N9010B(addr='USB0::0x2A8D::0x1C0B::MY56080582::0::INSTR', reset=True)
# sa.SetMode('BASIC')
# sa.SetReference('EXT')
# time.sleep(.5)

# Generator
# gen1 = Keysight_N5183B(addr='TCPIP::172.19.20.14::INSTR', reset=True)          # MXG
# gen1.EXTref()
# if gen_inst == 'MXG':
#     gen1.setCWfrequency(freq_gen)
#     gen1.setCWpower(power_gen)
#     gen1.RFon()
# elif gen_inst == 'PSG':
#     gen2 = Keysight_E8257D(addr='TCPIP::172.19.20.15::INSTR', reset=True)      # PSG
#     gen2.EXTref()
#     gen2.setCWfrequency(freq_gen)
#     gen2.setCWpower(power_gen)
#     gen2.RFon()
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
# sa.close()
# gen1.RFoff()
# gen1.close()
# if gen_inst == 'PSG':
#   gen2.RFoff()
#   gen2.close()
myfile.close()

time.sleep(30)

##########################################################
# MEASUREMENT 2 - CAVITY
##########################################################

print('MEASUREMENT 2 - CAVITY')

filename = 'VNA_cavity_PTon'

f_res    = 6.570145e9        #6.5214575e9  #6.383e9      #6.24088e9
f_mem    = 0.9791351e6       #0.9790654e6  #1.0030345e6  #1.010703e6

# VNA parameters
freq_center = f_res
span        = 10e6
freq_start  = freq_center - span/2
freq_stop   = freq_center + span/2

power_vna   = 0
ifbw        = 10000
nr_sp       = 1001
nr_tr       = 100
nr_avg      = 1

# Generator parameters
# gen_inst    = 'PSG'
# freq_gen    = f_res - f_mem
# power_gen   = -18

parameters = []
parameters.append('MEASUREMENT 2 - CAVITY')
# if gen_inst == 'MXG':
#     parameters.append('generator: \t'          + 'MXG')
# elif gen_inst == 'PSG':
#     parameters.append('generator: \t'          + 'PSG')
# parameters.append('generator freq: \t'         + str(freq_gen))
# parameters.append('generator power: \t'        + str(power_gen))
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
# sa = Keysight_N9010B(addr='USB0::0x2A8D::0x1C0B::MY56080582::0::INSTR', reset=True)
# sa.SetMode('BASIC')
# sa.SetReference('EXT')
# time.sleep(.5)

# Generator
# gen1 = Keysight_N5183B(addr='TCPIP::172.19.20.14::INSTR', reset=True)          # MXG
# gen1.EXTref()
# if gen_inst == 'MXG':
#     gen1.setCWfrequency(freq_gen)
#     gen1.setCWpower(power_gen)
#     gen1.RFon()
# elif gen_inst == 'PSG':
#     gen2 = Keysight_E8257D(addr='TCPIP::172.19.20.15::INSTR', reset=True)      # PSG
#     gen2.EXTref()
#     gen2.setCWfrequency(freq_gen)
#     gen2.setCWpower(power_gen)
#     gen2.RFon()
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
# sa.close()
# gen1.RFoff()
# gen1.close()
# if gen_inst == 'PSG':
#   gen2.RFoff()
#   gen2.close()
myfile.close()

time.sleep(30)

##########################################################
# MEASUREMENT 3 - CAVITY
##########################################################

print('MEASUREMENT 3 - CAVITY')

filename = 'VNA_cavity_PTon'

f_res    = 6.570145e9        #6.5214575e9  #6.383e9      #6.24088e9
f_mem    = 0.9791351e6       #0.9790654e6  #1.0030345e6  #1.010703e6

# VNA parameters
freq_center = f_res
span        = 10e6
freq_start  = freq_center - span/2
freq_stop   = freq_center + span/2

power_vna   = 0
ifbw        = 5000
nr_sp       = 1001
nr_tr       = 100
nr_avg      = 1

# Generator parameters
# gen_inst    = 'PSG'
# freq_gen    = f_res - f_mem
# power_gen   = -18

parameters = []
parameters.append('MEASUREMENT 3 - CAVITY')
# if gen_inst == 'MXG':
#     parameters.append('generator: \t'          + 'MXG')
# elif gen_inst == 'PSG':
#     parameters.append('generator: \t'          + 'PSG')
# parameters.append('generator freq: \t'         + str(freq_gen))
# parameters.append('generator power: \t'        + str(power_gen))
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
# sa = Keysight_N9010B(addr='USB0::0x2A8D::0x1C0B::MY56080582::0::INSTR', reset=True)
# sa.SetMode('BASIC')
# sa.SetReference('EXT')
# time.sleep(.5)

# Generator
# gen1 = Keysight_N5183B(addr='TCPIP::172.19.20.14::INSTR', reset=True)          # MXG
# gen1.EXTref()
# if gen_inst == 'MXG':
#     gen1.setCWfrequency(freq_gen)
#     gen1.setCWpower(power_gen)
#     gen1.RFon()
# elif gen_inst == 'PSG':
#     gen2 = Keysight_E8257D(addr='TCPIP::172.19.20.15::INSTR', reset=True)      # PSG
#     gen2.EXTref()
#     gen2.setCWfrequency(freq_gen)
#     gen2.setCWpower(power_gen)
#     gen2.RFon()
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
# sa.close()
# gen1.RFoff()
# gen1.close()
# if gen_inst == 'PSG':
#   gen2.RFoff()
#   gen2.close()
myfile.close()

time.sleep(30)

##########################################################
# MEASUREMENT 4 - CAVITY
##########################################################

print('MEASUREMENT 4 - CAVITY')

filename = 'VNA_cavity_PTon'

f_res    = 6.570145e9        #6.5214575e9  #6.383e9      #6.24088e9
f_mem    = 0.9791351e6       #0.9790654e6  #1.0030345e6  #1.010703e6

# VNA parameters
freq_center = f_res
span        = 1.2e6
freq_start  = freq_center - span/2
freq_stop   = freq_center + span/2

power_vna   = 0
ifbw        = 10000
nr_sp       = 401
nr_tr       = 100
nr_avg      = 1

# Generator parameters
# gen_inst    = 'PSG'
# freq_gen    = f_res - f_mem
# power_gen   = -18

parameters = []
parameters.append('MEASUREMENT 4 - CAVITY')
# if gen_inst == 'MXG':
#     parameters.append('generator: \t'          + 'MXG')
# elif gen_inst == 'PSG':
#     parameters.append('generator: \t'          + 'PSG')
# parameters.append('generator freq: \t'         + str(freq_gen))
# parameters.append('generator power: \t'        + str(power_gen))
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
# sa = Keysight_N9010B(addr='USB0::0x2A8D::0x1C0B::MY56080582::0::INSTR', reset=True)
# sa.SetMode('BASIC')
# sa.SetReference('EXT')
# time.sleep(.5)

# Generator
# gen1 = Keysight_N5183B(addr='TCPIP::172.19.20.14::INSTR', reset=True)          # MXG
# gen1.EXTref()
# if gen_inst == 'MXG':
#     gen1.setCWfrequency(freq_gen)
#     gen1.setCWpower(power_gen)
#     gen1.RFon()
# elif gen_inst == 'PSG':
#     gen2 = Keysight_E8257D(addr='TCPIP::172.19.20.15::INSTR', reset=True)      # PSG
#     gen2.EXTref()
#     gen2.setCWfrequency(freq_gen)
#     gen2.setCWpower(power_gen)
#     gen2.RFon()
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
# sa.close()
# gen1.RFoff()
# gen1.close()
# if gen_inst == 'PSG':
#   gen2.RFoff()
#   gen2.close()
myfile.close()

time.sleep(30)

##########################################################
# MEASUREMENT 5 - CAVITY
##########################################################

print('MEASUREMENT 5 - CAVITY')

filename = 'VNA_cavity_PTon'

f_res    = 6.570145e9        #6.5214575e9  #6.383e9      #6.24088e9
f_mem    = 0.9791351e6       #0.9790654e6  #1.0030345e6  #1.010703e6

# VNA parameters
freq_center = f_res
span        = 2.5e6
freq_start  = freq_center - span/2
freq_stop   = freq_center + span/2

power_vna   = 0
ifbw        = 10000
nr_sp       = 1001
nr_tr       = 100
nr_avg      = 1

# Generator parameters
# gen_inst    = 'PSG'
# freq_gen    = f_res - f_mem
# power_gen   = -18

parameters = []
parameters.append('MEASUREMENT 5 - CAVITY')
# if gen_inst == 'MXG':
#     parameters.append('generator: \t'          + 'MXG')
# elif gen_inst == 'PSG':
#     parameters.append('generator: \t'          + 'PSG')
# parameters.append('generator freq: \t'         + str(freq_gen))
# parameters.append('generator power: \t'        + str(power_gen))
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
# sa = Keysight_N9010B(addr='USB0::0x2A8D::0x1C0B::MY56080582::0::INSTR', reset=True)
# sa.SetMode('BASIC')
# sa.SetReference('EXT')
# time.sleep(.5)

# Generator
# gen1 = Keysight_N5183B(addr='TCPIP::172.19.20.14::INSTR', reset=True)          # MXG
# gen1.EXTref()
# if gen_inst == 'MXG':
#     gen1.setCWfrequency(freq_gen)
#     gen1.setCWpower(power_gen)
#     gen1.RFon()
# elif gen_inst == 'PSG':
#     gen2 = Keysight_E8257D(addr='TCPIP::172.19.20.15::INSTR', reset=True)      # PSG
#     gen2.EXTref()
#     gen2.setCWfrequency(freq_gen)
#     gen2.setCWpower(power_gen)
#     gen2.RFon()
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
# sa.close()
# gen1.RFoff()
# gen1.close()
# if gen_inst == 'PSG':
#   gen2.RFoff()
#   gen2.close()
myfile.close()

# time.sleep(30)

# ##########################################################
# # MEASUREMENT 6 - SA IQ
# ##########################################################

# print('MEASUREMENT 6 - SA IQ')

# filename = 'SA_IQ_res_drive_PTon'

# f_res    = 6.570145e9        #6.5214575e9  #6.383e9      #6.24088e9
# f_mem    = 0.9791351e6       #0.9790654e6  #1.0030345e6  #1.010703e6
# detuning = 100e3
# offset   = 20

# # Spectrum analyser parameters
# freq_center = f_res - f_mem - detuning - offset
# t_sweep     = 100
# t_total     = 3600                             # for now let's keep t_total/t_sweep an integer
# sample_rate_digitize = 10e3
# IFBW        = 80
# nr_tr       = 1
# nr_avg      = 1

# # Generator parameters
# gen_inst    = 'MXG'
# freq_gen    = f_res - detuning
# powers_gen  = [0]

# # Generator
# gen1 = Keysight_N5183B(addr='TCPIP::172.19.20.14::INSTR', reset=True)          # MXG
# gen1.EXTref()
# if gen_inst == 'MXG':
#     gen1.setCWfrequency(freq_gen)
#     gen1.setCWpower(powers_gen[0])
#     gen1.RFon()
# elif gen_inst == 'PSG':
#     gen2 = Keysight_E8257D(addr='TCPIP::172.19.20.15::INSTR', reset=True)      # PSG
#     gen2.EXTref()
#     gen2.setCWfrequency(freq_gen)
#     gen2.setCWpower(powers_gen[0])
#     gen2.RFon()
# time.sleep(2)

# for i, p in enumerate(powers_gen):
#     print(datetime.now())
#     print('power: ' + str(p))

#     if gen_inst == 'MXG':
#         gen1.setCWpower(p)
#         gen1.RFon()
#     elif gen_inst == 'PSG':
#         gen2.setCWpower(p)
#         gen2.RFon()

#     # Spectrum analyser
#     sa = Keysight_N9010B(addr='USB0::0x2A8D::0x1C0B::MY56080582::0::INSTR', reset=True)
#     sa.SetMode('BASIC')
#     sa.SetReference('INT')

#     sa.SetCenter(freq_center)
#     sa.SetIQSweepTime(t_sweep) 
#     sa.SetSampleRate(sample_rate_digitize)
#     sa.SetDigitalIFBW(IFBW)

#     # sa.SetAverages(nr_avg)
#     # if nr_avg > 1:
#     #   sa.write(':AVER:TYPE RMS')      # Averaging type Logarithmic power (LOG), Power (RMS) or Voltage (SCALar)
#     #   sa.write(':AVER ON')

#     # This is a first version of a list of all important parameters
#     parameters = []
#     parameters.append('MEASUREMENT 6 - SA IQ')
#     if gen_inst == 'MXG':
#         parameters.append('generator: \t'            + 'MXG')
#     elif gen_inst == 'PSG':
#         parameters.append('generator: \t'            + 'PSG')
#     parameters.append('generator freq: \t'           + str(freq_gen))
#     parameters.append('generator power: \t'          + str(p))
#     parameters.append('SA freq center: \t'           + str(freq_center))
#     parameters.append('SA time sweep: \t'            + str(t_sweep))
#     parameters.append('SA time total: \t'            + str(t_total))
#     parameters.append('SA sample rate digitizer: \t' + str(sample_rate_digitize))
#     parameters.append('SA IFBW: \t'                  + str(IFBW))
#     parameters.append('SA number of traces: \t'      + str(nr_tr))
#     parameters.append('SA number of averages: \t'    + str(nr_avg))
#     parameters.append('temperature: \t'            + '50 mK')
#     parameters.append('Lake Shore P gain: \t'      + '2.0')
#     parameters.append('Lake Shore I gain: \t'      + '20 sec')
#     parameters.append('Lake Shore D gain: \t'      + '10 sec')

#     # Measure
#     Data    = {}
#     t_start = datetime.now()
#     print('time start: ', t_start)

#     for j in range(int(t_total/t_sweep)):
#         print('trace: ' + str(j))
#         output = sa.MeasureIQ()

#         Data['Time (s)']    = output['Time (s)'].tolist()
#         Data['I (V)']       = output['I (V)'].tolist()
#         Data['Q (V)']       = output['Q (V)'].tolist()

#         if j == 0:
#             # Info for data explorer
#             parameters_dexplore = {}
#             parameters_dexplore['measurement_type'] = 'IQ'
#             parameters_dexplore['t_start']          = 0
#             parameters_dexplore['t_stop']           = Data['Time (s)'][-1]
#             parameters_dexplore['nr_sp']            = len(Data['I (V)']) * int(t_total/t_sweep)
#             parameters_dexplore['nr_traces']        = nr_tr

#             myfile = stlab.newfile('', filename, Data.keys())
#         stlab.savedict(myfile, Data)

#     t_stop = datetime.now()
#     parameters.append('time start: \t' + str(t_start))
#     parameters.append('time stop: \t'  + str(t_stop))
#     metafile_generator(myfile, parameters, parameters_dexplore, Data)


#     if gen_inst == 'MXG':
#         gen1.RFoff()
#     elif gen_inst == 'PSG':
#         gen2.RFoff()
#     sa.close()
#     myfile.close()
#     # time.sleep(60)
    
# gen1.close()
# if gen_inst == 'PSG':
#     gen2.close()

























