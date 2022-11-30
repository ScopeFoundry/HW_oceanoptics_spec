from ScopeFoundry import HardwareComponent
import numpy as np

class OceanOpticsSpectrometerODirectHW(HardwareComponent):

    name = 'ocean_optics_spec'
    
    def setup(self):
        S = self.settings
        # Create logged quantities
        S.New(name="int_time", dtype=float, ro=False, vmin=0.0001, vmax=1000, unit='s', initial=0.1,spinbox_decimals=4)
        #S.New('dev_id', dtype=int, initial=-1)
        S.New('serial_num', dtype=str, initial='auto', ro=False)
        
        
    def connect(self):
        
        from .oceandirect.OceanDirectAPI import OceanDirectAPI, OceanDirectError, FeatureID

        S = self.settings
        
        od = OceanDirectAPI()
        dev_count = od.find_usb_devices()
        dev_ids = od.get_device_ids()

        S.serial_num.change_readonly(True)
        
        if S['serial_num'] == 'auto':
            self.dev = dev = od.open_device(dev_ids[0])
            S['serial_num'] = self.dev.get_serial_number()
        elif S['serial_num'][0:5] == 'devid':
            dev_id = int(S['serial_num'][5:])
            self.dev = dev = od.open_device(dev_ids[dev_id])
            S['serial_num'] = self.dev.get_serial_number()
        else:
            for dev_id in dev_ids:
                self.dev = dev = od.open_device(dev_id)
                sn = od.get_serial_number(dev_id)
                if sn == S['serial_num']:
                    break
                else:
                    self.dev.close_device()
        
        self.wls = self.wavelengths = dev.get_wavelengths()
        self.dark_indicies = dev.get_electric_dark_pixel_indices()
        
        S.int_time.connect_to_hardware(
            read_func=self.read_int_time,
            write_func=self.write_int_time)
        S.int_time.read_from_hardware()
        
        
    def disconnect(self):
        #disconnect logged quantities from hardware
        self.settings.disconnect_all_from_hardware()
        self.settings.serial_num.change_readonly(False)

        if hasattr(self, 'dev'):
            #disconnect hardware
            self.dev.close()

            # clean up hardware object
            del self.dev
        
        
    def read_int_time(self):
        return self.dev.get_integration_time()*1e-6
        
    def write_int_time(self, t):
        self.dev.set_integration_time(int(1e6*t))
        
    def acquire_spectrum(self):
        self.spectrum = self.dev.get_formatted_spectrum()

    def get_spectrum(self):
        return np.array(self.spectrum)

    def get_dark_indices(self):
        return self.dark_indicies