import time
from datetime import datetime
import numpy as np
import stlab
from stlab.devices.Keysight_N5183B import Keysight_N5183B
from stlab.devices.Keysight_E8257D import Keysight_E8257D
from stlab.devices.Keysight_N9010B import Keysight_N9010B
from Metafile_generator import metafile_generator

filename = 'SA_IQ_res_drive_PTon'

f_res    = 6.570145e9        #6.5214575e9  #6.383e9      #6.24088e9
f_mem    = 0.9791351e6       #0.9790654e6  #1.0030345e6  #1.010703e6
detuning = 100e3
offset   = 20

# Spectrum analyser parameters
freq_center = f_res - f_mem - detuning - offset
t_sweep     = 100
t_total     = 100                             # for now let's keep t_total/t_sweep an integer
sample_rate_digitize = 10e3
IFBW        = 80
nr_tr       = 1
nr_avg      = 1

# Generator parameters
gen_inst    = 'MXG'
freq_gen    = f_res - detuning
powers_gen  = [16]

# Generator
gen1 = Keysight_N5183B(addr='TCPIP::172.19.20.14::INSTR', reset=True)          # MXG
gen1.EXTref()
if gen_inst == 'MXG':
	gen1.setCWfrequency(freq_gen)
	gen1.setCWpower(powers_gen[0])
	gen1.RFon()
elif gen_inst == 'PSG':
	gen2 = Keysight_E8257D(addr='TCPIP::172.19.20.15::INSTR', reset=True)      # PSG
	gen2.EXTref()
	gen2.setCWfrequency(freq_gen)
	gen2.setCWpower(powers_gen[0])
	gen2.RFon()
time.sleep(2)

for i, p in enumerate(powers_gen):
	print(datetime.now())
	print('power: ' + str(p))

	if gen_inst == 'MXG':
		gen1.setCWpower(p)
		gen1.RFon()
	elif gen_inst == 'PSG':
		gen2.setCWpower(p)
		gen2.RFon()

	# Spectrum analyser
	sa = Keysight_N9010B(addr='USB0::0x2A8D::0x1C0B::MY56080582::0::INSTR', reset=True)
	sa.SetMode('BASIC')
	sa.SetReference('INT')

	sa.SetCenter(freq_center)
	sa.SetIQSweepTime(t_sweep) 
	sa.SetSampleRate(sample_rate_digitize)
	sa.SetDigitalIFBW(IFBW)

	# sa.SetAverages(nr_avg)
	# if nr_avg > 1:
	# 	sa.write(':AVER:TYPE RMS')		# Averaging type Logarithmic power (LOG), Power (RMS) or Voltage (SCALar)
	# 	sa.write(':AVER ON')

	# This is a first version of a list of all important parameters
	parameters = []
	if gen_inst == 'MXG':
		parameters.append('generator: \t'            + 'MXG')
	elif gen_inst == 'PSG':
		parameters.append('generator: \t'            + 'PSG')
	parameters.append('generator freq: \t'           + str(freq_gen))
	parameters.append('generator power: \t'          + str(p))
	parameters.append('SA freq center: \t'           + str(freq_center))
	parameters.append('SA time sweep: \t'            + str(t_sweep))
	parameters.append('SA time total: \t'            + str(t_total))
	parameters.append('SA sample rate digitizer: \t' + str(sample_rate_digitize))
	parameters.append('SA IFBW: \t'                  + str(IFBW))
	parameters.append('SA number of traces: \t'      + str(nr_tr))
	parameters.append('SA number of averages: \t'    + str(nr_avg))
	parameters.append('temperature: \t'            + '50 mK')
	parameters.append('Lake Shore P gain: \t'      + '2.0')
	parameters.append('Lake Shore I gain: \t'      + '20 sec')
	parameters.append('Lake Shore D gain: \t'      + '10 sec')

	# Measure
	Data    = {}
	t_start = datetime.now()
	print('time start: ', t_start)

	for j in range(int(t_total/t_sweep)):
		print('trace: ' + str(j))
		output = sa.MeasureIQ()

		Data['Time (s)']    = output['Time (s)'].tolist()
		Data['I (V)']       = output['I (V)'].tolist()
		Data['Q (V)']       = output['Q (V)'].tolist()

		if j == 0:
			# Info for data explorer
			parameters_dexplore = {}
			parameters_dexplore['measurement_type'] = 'IQ'
			parameters_dexplore['t_start']          = 0
			parameters_dexplore['t_stop']           = Data['Time (s)'][-1]
			parameters_dexplore['nr_sp']            = len(Data['I (V)']) * int(t_total/t_sweep)
			parameters_dexplore['nr_traces']        = nr_tr

			myfile = stlab.newfile('', filename, Data.keys())
		stlab.savedict(myfile, Data)

	t_stop = datetime.now()
	parameters.append('time start: \t' + str(t_start))
	parameters.append('time stop: \t'  + str(t_stop))
	metafile_generator(myfile, parameters, parameters_dexplore, Data)


	if gen_inst == 'MXG':
		gen1.RFoff()
	elif gen_inst == 'PSG':
		gen2.RFoff()
	sa.close()
	myfile.close()
	# time.sleep(60)

gen1.close()
if gen_inst == 'PSG':
	gen2.close()

