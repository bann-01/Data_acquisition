import sys
sys.path.append('Z:\\ann\\')


class pri_sweep:
        '''
        in preparation.
        '''
    def __init__(self):
        self.numswp  = 0
        self.vari_list = []
        self.range_list = []
    def add_aux_sweep(self, sweep_device, sweep_range):
        self.numswp = self.numswp + 1
        self.vari_list.append(sweep_vari)
        self.range_list.append(sweep_range)


class pri_constant:
        '''
        in preparation.
        '''
    def __init__(self):
        self.numconst  = 0
        self.const_list = []
        self.value_list = []
    def add_aux_sweep(self, const_device, const_value):
        self.numswp = self.numswp + 1
        self.const_list.append(const_device)
        self.value_list.append(const_value)


class aux_sweep:
        '''
        in preparation.
        '''
    def __init__(self):
        self.numswp  = 0
        self.vari_list = []
        self.range_list = []
    def add_aux_sweep(self, sweep_device, sweep_range):
        self.numswp = self.numswp + 1
        self.vari_list.append(sweep_vari)
        self.range_list.append(sweep_range)


class aux_constant:
        '''
        in preparation.
        '''
    def __init__(self):
        self.numconst  = 0
        self.const_list = []
        self.value_list = []
    def add_aux_sweep(self, const_device, const_value):
        self.numswp = self.numswp + 1
        self.const_list.append(const_list)
        self.value_list.append(const_value)



