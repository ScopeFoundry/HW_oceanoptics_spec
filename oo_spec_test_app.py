from ScopeFoundry import BaseMicroscopeApp

class OOSpecTestApp(BaseMicroscopeApp):
    
    name = 'oospec_test_app'
    
    def setup(self):
        #from ScopeFoundryHW.oceanoptics_spec import OceanOpticsSpectrometerHW
        #hw = self.add_hardware(OceanOpticsSpectrometerHW(self))
        #hw.settings['port'] = 'COM5'
        from ScopeFoundryHW.oceanoptics_spec.oo_spec_odirect_hw import OceanOpticsSpectrometerODirectHW
        hw = self.add_hardware(OceanOpticsSpectrometerODirectHW)
        
        from ScopeFoundryHW.oceanoptics_spec import OOSpecLive
        self.add_measurement(OOSpecLive(self))
                
if __name__ == '__main__':
    import sys
    app = OOSpecTestApp(sys.argv)
    app.exec_()