# RvS RTO2024 oscilloscope.

install_directory = 'Z:\\ann\\'

import sys
if install_directory not in sys.path:
        sys.path.append(install_directory)

from Data_acquisition.devices.base_instrument import instrument

def numtostr(mystr):
    return '%20.15e' % mystr


class RTO2024(instrument):
    def __init__(self,
        addr='TCPIP::192.168.1.43::hislip0::INSTR',
        reset=True,
        verb=True,
        read_termination='\n',
        timeout):
        super().__init__(addr, reset, verb)
        self.timeout(timeout)
        
    def __del__(self):
        self.close()

    def idn(self):
        return(self.query('*IDN?'))

    def set_avg(self, num_avg):
        self.write('ACQuire:COUNt ' + str(num_avg))

    def single_trace(self):
        self.write('SINGle')

    def get_x_trace(self, channel_num = 1):
        self.write(':FORM ASC')
        data_export = self.query(':CHANnel'+ str(channel_num) +':DATA:HEAD?')
        self.query('*OPC?')
        return data_export

    def get_y_trace(self, channel_num = 1):
        self.write(':FORM ASC')
        data_export = self.query(':CHANnel'+ str(channel_num) +':DATA:VALues?')
        self.query('*OPC?')
        return data_export