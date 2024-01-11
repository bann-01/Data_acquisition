import pyvisa
import serial
import time
import numpy as np
from bitstring import BitArray,BitStream
import json 
import requests
import pickle
from datetime import datetime
import re

def numtostr(mystr):
    return '%20.15e' % mystr

class BF_thermometer:
    
    def __init__(self, ip = '192.168.0.2' , url='/channel/measurement/latest', timeout = 10):
        self.device_ip = ip
        self.url       = url
        self.timeout = timeout

    def read_latest(self):
        
        DEVICE_IP = self.device_ip; TIMEOUT = self.timeout
        url = 'http://{}'.format(DEVICE_IP) + self.url
        req = requests.get(url,timeout=TIMEOUT)
        data = req.json(); ch = data['channel_nr']; t = data['timestamp']; T = data['temperature']
        return (ch,t,T)
    
    def read_history(self, start_time, stop_time, ch_nr = 6):
        
        DEVICE_IP = self.device_ip; TIMEOUT = self.timeout
        url = 'http://{}'.format(DEVICE_IP) + self.url
        data = {'channel_nr': ch_nr,
                'start_time': start_time,
                'stop_time': stop_time,
                'fields': ['temperature']}
    
        req = requests.post(url, json=data, timeout = TIMEOUT)
        data = req.json(); T = data['measurements']['temperature']
        t = data['measurements']['timestamp']
        return [t,T]
    
    def read_heater(self, h_nr = 4):
        
        DEVICE_IP = self.device_ip; TIMEOUT = self.timeout
        url = 'http://{}'.format(DEVICE_IP) + self.url
        data = {'heater_nr':h_nr}
        req = requests.post(url,json=data,timeout=TIMEOUT)
        return req.json()
        
    def target_T(self, setpoint):
        
        DEVICE_IP = self.device_ip; TIMEOUT = self.timeout
        url = 'http://{}'.format(DEVICE_IP) + self.url
        data = {'heater_nr':4,'setpoint':setpoint}
        req = requests.post(url,json=data,timeout=TIMEOUT)
    
    
    def set_PID(self, P = 0.05, I = 250, D = 0):
        
        DEVICE_IP = self.device_ip; TIMEOUT = self.timeout
        url = 'http://{}'.format(DEVICE_IP) + self.url
        data = {'heater_nr':4,'control_algorithm_settings':
                {'proportional': P,'integral': I,'derivative': D}}
    
        req=requests.post(url, json=data, timeout=TIMEOUT)
        
    def set_maxpw(self, pw):
        
        DEVICE_IP = self.device_ip; TIMEOUT = self.timeout
        url = 'http://{}'.format(DEVICE_IP) + self.url
        data = {'heater_nr':4,'max_power':pw}
        req = requests.post(url, json=data, timeout=TIMEOUT)

    def temperature_log(self, sensor_number = 6, sleep_time = 1):
        CurrentT = self.read_latest()
        SN       = CurrentT[0]
        if SN == sensor_number:
            T = CurrentT[2]
        else:
            time.sleep(sleep_time)
            SN       = CurrentT[0]
            while SN != sensor_number:
                time.sleep(sleep_time)
                CurrentT = self.read_latest()
                SN       = CurrentT[0]
                T        = CurrentT[2]
        return T