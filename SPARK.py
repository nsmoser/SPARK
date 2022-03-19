"""
- Semiconductor Parameter Analyzer Replacement Kit (SPARK)
- by Nickolas Moser
- For use in EE330 - Integrated Electronics
- Uses lab equipment SCPI commandset to measure 
  MOSFET drain current as a function of drain-source
  voltage across multiple gate-source voltages.
  Plots output and dumps to something (not done yet)
- Necesary equipment: Keysight EDU32212A Waveform Generator
                      Keysight 34470A Multimeter
- Necessary software: Python 3.10 (duh)
                      Pyvisa Library (install via pip)
                      Keysight IO Libraries Suite (download from keysight)
- Setup process is complete. Creates and sets up benchtop tools.
  Creates sweep value lists for v_ds and v_gs
- WIP: Still needs to take measurements,
  output to .txt file or other method, and plot outputs
  possibly find way to put waveform generator in high-z mode
  build handling for more than two device objects
"""
import pyvisa                       #neeced to communicate with lab equipment     
from time import sleep              #sleep used to slow down certain processes

#AVOID EDITING THIS UNLESS YOU KNOW WHAT YOU ARE DOING
#finds available devices, then creates device object list
#returns list of device objects
#only anticipates two device objects: multimeter and waveform generator
def acquire_devices():
    print("Device Search Beginning")
    #sleep(1)
    available_devices = []                  #create array for relocating devices for assignment
    #below gets list of all devices available to the computer. Populates as tuple
    available_devices_temp = resource_manager.list_resources()
    print("Devices Found:",len(available_devices_temp)) #gives quantity of available devices
    if(len(available_devices_temp)) < 2:                #if less than two devices are available
        print("Not Enough Devices!")
        print("Check that Multimeter and Waveform Generator are connected")
        exit()                                          #give error, exit
    print("Device IDs:", available_devices_temp)        #gives device ids
    #sleep(1)
   
    for i in available_devices_temp:                    #for every available device
        available_devices.append(str(i))                #populate relocation list
        device.append(i)                                #populate device object list
    
    for i in range(len(available_devices)):             #for every available device
        #below code moves available device tuple to list with devices as strings
        #for some reason, the open_resource() function won't take strings from tuples
        #but will take strings from a list. ¯\_(ツ)_/¯
        available_devices[i] = available_devices_temp[i]
        #below code creates device objects and places them within the device object list
        device[i] = resource_manager.open_resource(available_devices[i])
        print("Connected to device", i)
    
    print("Device Search Complete")
    #sleep(1)
    return device               #return device object list

#AVOID EDITING THIS UNLESS YOU KNOW WHAT YOU ARE DOING
#gives device identifier within device object list
#only needs to differentiate between multimeter and waveform generator
#returns device identifier
#WIP: handle identifying devices that aren't multimeter and waveform generator
#an if-elseif-else structure would work well here
def identify_device(device,i):
    #sleep(1)
    device_info = device[i].query("*IDN?")          #query which returns device info
    if device_info.find("EDU33212A") != -1:         #if waveform generator P/N is returned
        device_id = "Waveform Generator"            #device is waveform generator
        print("Waveform Generator is device", i)
    if device_info.find("34470A") != -1:            #if multimeter P/N is returned
        device_id = "Multimeter"                    #device is multimeter
        print("Multimeter is device", i)
    return device_id                                #return the device id

#sets up waveform generator.
#sets waveform parameters to good starting values
#sets all relevant and non-relevant parameters for experiment
def wg_setup(device,waveform_generator,amplitude):
    print("Waveform Generator Setup in progress...")
    freq = 0.000001                 #frequency: 1uHz
    offset = 0                      #offset: 0V
    phase = 0                       #phase: 0 degrees
    shape = "SQU"                   #waveform shape: square
    state = 1                       #output state: on
    #clears any present waveform generator errors
    device[waveform_generator].write("*CLS")  
    #sets waveform frequency
    device[waveform_generator].write("SOUR1:FREQ ", str(freq))
    device[waveform_generator].write("SOUR2:FREQ ", str(freq))
    #sets waveform amplitude
    device[waveform_generator].write("SOUR1:VOLT:LEV:IMM:AMPL ", str(amplitude))
    device[waveform_generator].write("SOUR2:VOLT:LEV:IMM:AMPL ", str(amplitude))
    #sets waveform offset
    device[waveform_generator].write("SOUR1:VOLT:LEV:IMM:OFFS ", str(offset))
    device[waveform_generator].write("SOUR2:VOLT:LEV:IMM:OFFS ", str(offset))
    #sets waveform phase
    device[waveform_generator].write("SOUR1:PHAS ", str(phase))
    device[waveform_generator].write("SOUR2:PHAS ", str(phase))
    #sets waveform shape
    device[waveform_generator].write("SOUR1:FUNC:SHAP ", shape)
    device[waveform_generator].write("SOUR2:FUNC:SHAP ", shape)
    #turns on both outputs
    device[waveform_generator].write("OUTP1:STAT ", str(state))
    device[waveform_generator].write("OUTP2:STAT ", str(state))
    sleep(1)
    print("Waveform Generator Setup Complete")

#gets user input to generate vgs_sweep list
#returns vgs_sweep
#pretty straight-forward
def vgs_setup():
    #gets vgs start value
    print("Enter desired V_GS start value (in volts)")
    vgs_start = int(input())
    #gets vgs end value
    print("Enter desired V_GS end value (in volts)")
    vgs_end = int(input())
    #get vgs step size
    print("Enter desired V_GS increment (in volts)")
    vgs_incr = float(input())
    #find how many steps need to be taken
    vgs_step = (vgs_end-vgs_start)/vgs_incr
    #populate vgs_sweep list with test points
    for i in range(int(vgs_step+1)):
        vgs_sweep.append(vgs_start+(vgs_incr*(i)))
    return vgs_sweep    #return vgs_sweep list

#gets user input to generate vds_sweep list
#returns vds_sweep
#works the same as vgs_sweep
def vds_setup():
    #get vds start value
    print("Enter desired V_DS start value (in volts)")
    vds_start = int(input())
    #get vds end value
    print("Enter desired V_DS end value (in volts)")
    vds_end = int(input())
    #get vds step size
    print("Enter desired V_DS increment (in volts)")
    vds_incr = float(input())
    #find how many steps need to be taken
    vds_step = (vds_end-vds_start)/vds_incr
    #populate vds_sweep list with test points
    for i in range(int(vds_step+1)):
        vds_sweep.append(vds_start+(vds_incr*(i)))
    return vds_sweep


#PROGRAM STARTS HERE
#creates resource manager object. it's supposed to just find
#the resource manager file, so no need for an argument
resource_manager = pyvisa.ResourceManager()

#necessary global variables can be found here
device = []                             #device object list, used for benchtop instruments
waveform_generator = 0                  #default value
multimeter = 0                          #default value
input_wave_amplitude = 0.001            #minimum amplitude of wave in waveform generator
vgs_sweep = []                          #vgs_sweep values list
vds_sweep = []                          #vds_sweep values list

#populate device object list
device = acquire_devices()

#identify devices in device object list
print("Device Identification in progress...")
for i in range(len(device)):                        #for all devices
    temp_device = identify_device(device,i)         #use device object identifier function
    if temp_device.find("Waveform Generator") != -1:#if waveform generator is identified device
        waveform_generator = i                      #waveform generator is device object i
    if temp_device.find("Multimeter") != -1:        #if multimeter is identified object
        multimeter = i                              #multimeter is device object i
print("Device Identification Complete")
#sleep(1)

#set up waveform generator before measurements are performed
wg_setup(device,waveform_generator,input_wave_amplitude)

#set up vgs_sweep list for measurements
vgs_sweep = vgs_setup()

#set up vds_sweep list for measurements
vds_sweep = vds_setup()