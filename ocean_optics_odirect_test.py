# try:
#     import .oceandirect
# except:
#     import sys
#     import os
#     sys.path.insert(0,r"C:\Program Files\Ocean Insight\OceanDirect SDK\Python")
#     os.environ['OCEANDIRECT_HOME'] = r"C:\Program Files\Ocean Insight\OceanDirect SDK\Python\lib"
#     import oceandirect
    
#print(oceandirect)
from ScopeFoundryHW.oceanoptics_spec.oceandirect.OceanDirectAPI import OceanDirectAPI, OceanDirectError, FeatureID
import matplotlib.pyplot as plt


od = OceanDirectAPI()
device_count = od.find_usb_devices()
device_ids = od.get_device_ids()
print(device_count)
print(device_ids)

fig = plt.figure()


for iden in device_ids:
    print(f"Device {iden=}", "="*20)
    s = od.open_device(iden)
    
    #print(f"{s.get_nonlinearity_coeffs()=}")           
    print(f"{s.get_serial_number()=}")
    print(f"{s.get_max_intensity()=}")
    print(f"{s.get_minimum_integration_time()=}")
    print(f"{s.get_maximum_integration_time()=}")
    print(f"{s.get_integration_time()=}") #microseconds
    print(f"{s.get_integration_time_increment()=}") #microseconds
    print(f"{s.get_trigger_mode()=}")
    
    #print(f"{s.get_wavelengths()=}")
    wls = s.get_wavelengths()
    #spec = s.get_formatted_spectrum()
    s.set_integration_time(int(1e6))
    spec = s.get_formatted_spectrum()
    ax = fig.add_subplot(2,2,iden)
    ax.plot(wls, spec)
    
    
    # decode_error(errno)                
    # open_device()                        
    # close_device()                        
    # #use_nonlinearity(nonlinearity_flag)
    # get_formatted_spectrum()            
    # get_wavelengths()                    
    # set_integration_time(int_time)        
    # calculate_auto_integration_time()    
    # take_reference()                    
    # take_dark()                        
    # get_absorbance()                    
    # get_reflectance()                    
    # get_transmittance()                
    # get_number_electric_dark_pixels()    
    # get_electric_dark_pixel_indices()    

    
    
plt.show()