"""
- Semiconductor Parameter Analyzer Replacement Kit (SPARK)
- by Nickolas Moser
- For use in EE330 - Integrated Electronics
- Uses lab equipment SCPI commandset to measure 
  MOSFET drain current as a function of drain-source
  voltage across multiple gate-source voltages.
  Test setup uses MOSFET as input current in transresistance amp
  configuration with operational amplifier.
  Plots output and dumps to .txt file
- Necesary equipment: Keysight EDU32212A Waveform Generator
                      Keysight 34470A Multimeter
  NOTE: the software uses these device P/Ns to identify which device is which.
        if it is desired to use other devices, change P/Ns in identify_device function.
        also, double check that the device supports usb connectivity and SCPI commandset.
- Necessary software: Python 3.10 (any version of python 3 will probably work)
                      pyvisa Library (install via pip)
                      matplotlib library (install via pip)
                      Keysight IO Libraries Suite (download from keysight)
- Version 1.1 update:
  Added recursive algorithm to accomodate resistance between voltage source and MOSFET drain.
  Outputs difference between voltage set at voltage source and actual V_DS.
  Finds actual V_DS value based on measured resistance between voltage source and MOSFET drain,
  then readjusts voltage source to get actual V_DS value within a measurement accuracy tolerance.
  Changes within get_reading() function.
"""
import pyvisa                       #needed to communicate with lab equipment 
import matplotlib.pyplot as plotter #needed to plot measurements
from time import sleep              #sleep used to slow down certain processes

#AVOID EDITING THIS UNLESS YOU KNOW WHAT YOU ARE DOING
#finds available devices, then creates device object list
#returns list of device objects
def acquire_devices():
    print("Device Search Beginning...")
    sleep(1)
    available_devices = []                  #create array for relocating devices for assignment
    #get list of all devices available to the computer. Populates as tuple
    available_devices_temp = resource_manager.list_resources()
    print("Devices Found:",len(available_devices_temp)) #gives quantity of available devices
    if(len(available_devices_temp)) < 2:                #if less than two devices are available
        print("Not Enough Devices!")
        print("Check that Multimeter and Waveform Generator are connected")
        exit()                                          #give error, exit
    print("Device IDs:", available_devices_temp)        #gives device ids
    sleep(1)
   
    for i in available_devices_temp:                    #for every available device
        available_devices.append(str(i))                #populate relocation list
        device.append(i)                                #populate device object list
    
    for i in range(len(available_devices)):             #for every available device
        #move available device tuple to list with devices as strings
        #for some reason, the open_resource() function won't take strings from tuples
        #but will take strings from a list. ¯\_(ツ)_/¯
        available_devices[i] = available_devices_temp[i]
        #create device objects and place them within the device object list
        device[i] = resource_manager.open_resource(available_devices[i])
        print("Connected to device", i)
    
    print("Device Search Complete")
    sleep(1)
    return device               #return device object list

#AVOID EDITING THIS UNLESS YOU KNOW WHAT YOU ARE DOING
#gives device identifier within device object list
#identifies devices by returned P/N
#returns device identifier
def identify_device(device,i):
    sleep(1)
    device_temp = str(device[i])
    if device_temp.find("USB") != -1:                   #checks if device is a usb device as all test equipment used is usb
        device_info = device[i].query("*IDN?")          #query which returns device info
        if device_info.find("EDU33212A") != -1:         #if waveform generator P/N is returned
            device_id = "Waveform Generator"            #device is waveform generator
            print("Waveform Generator is device", i)
        elif device_info.find("34470A") != -1:          #if multimeter P/N is returned
            device_id = "Multimeter"                    #device is multimeter
            print("Multimeter is device", i)
        else:                                           #if device isn't necessary for this
            device_id = "idfk"                          #return mystery device
            print("Device %d is a mystery device" % i)
        sleep(1)
    else:
        print("Device %d is a mystery device" % i)      #if device is not a usb device
        device_id = "idfk"                              #return mystery device
    return device_id                                    #return device id

#sets up waveform generator.
#sets waveform parameters to good starting values
#sets all relevant and non-relevant parameters for experiment
def wg_setup(device,waveform_generator):
    print("Waveform Generator Setup in progress...")
    sleep(1)
    freq = 0.000001                 #frequency: 1uHz
    offset = 0                      #offset: 0V
    amplitude = 0                   #dc amplitude: 0
    phase = 0                       #phase: 0 degrees
    shape = "DC"                    #waveform shape: dc
    state = 1                       #output state: on
    #clears any present waveform generator errors
    device[waveform_generator].write("*CLS")  
    #sets waveform shape
    device[waveform_generator].write("SOUR1:FUNC:SHAP ", shape)
    device[waveform_generator].write("SOUR2:FUNC:SHAP ", shape)
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
    #turns on both outputs
    device[waveform_generator].write("OUTP1:STAT ", str(state))
    device[waveform_generator].write("OUTP2:STAT ", str(state))
    print("Waveform Generator Setup Complete\r\n\r\n")
    sleep(1)

#gets user input to generate vgs_sweep list
#returns vgs_sweep
#pretty straight-forward
def vgs_setup():
    #gets vgs start value
    print("Enter desired V_GS start value (in volts)")
    vgs_start = float(input())
    #gets vgs end value
    print("Enter desired V_GS end value (in volts)")
    vgs_end = float(input())
    #get vgs step size
    print("Enter desired V_GS increment (in volts)")
    vgs_incr = float(input())
    #find how many steps need to be taken
    vgs_step = (vgs_end-vgs_start)/vgs_incr
    #populate vgs_sweep list with test points
    for i in range(int(vgs_step+1)):
        vgs_sweep.append(round(vgs_start+(vgs_incr*(i)),2))
    return vgs_sweep    #return vgs_sweep list

#gets user input to generate vds_sweep list
#returns vds_sweep
#works the same as vgs_sweep
def vds_setup():
    #get vds start value
    print("Enter desired V_DS start value (in volts)")
    vds_start = float(input())
    #get vds end value
    print("Enter desired V_DS end value (in volts)")
    vds_end = float(input())
    #get vds step size
    print("Enter desired V_DS increment (in volts)")
    vds_incr = float(input())
    #find how many steps need to be taken
    vds_step = (vds_end-vds_start)/vds_incr
    #populate vds_sweep list with test points
    for i in range(int(vds_step+1)):
        vds_sweep.append(round(vds_start+(vds_incr*(i)),2))
    return vds_sweep

#gets reading from multimeter
#returns measured drain current plus associated vds and vgs
#needs vds and vgs at which measurement is being taken
#needs resistor value of feedback network
#set bnc-to-banana impedance and measurement accuracy tolerance here
#if accuracy tolerance is high, measurements will take a while
def get_reading(device,multimeter,waveform_generator,vds,new_vds,vgs,res):
    #set bnc-to-banana adapter impedance here
    adapter_impedance = 50
    #set measurement accuracy tolerance in volts here
    meas_tol = 0.005
    #clear any residual errors
    device[multimeter].write("*CLS")        
    #get reading from multimeter, returns as string
    multimeter_reading = device[multimeter].query("MEAS:VOLT:DC? 10")
    #split reading string into coefficient and exponent
    reading_split = multimeter_reading.split('E')
    #turn coefficient into an actual number
    reading_coeff = float(reading_split[0])
    #turn exponent into an actual number
    reading_exp = float(reading_split[1])
    #take coefficient and exponent to calculate reading
    reading = reading_coeff * (10 ** reading_exp)
    #convert multimeter reading into drain current
    id = abs(reading/res)
    #find the actual vds by subtracting drop across bnc-to-banana adapter from estimated vds
    vds_actual = new_vds - (id*adapter_impedance)
    #get difference between estimated and actual vds
    vds_diff = vds - vds_actual
    #estimate new output value to get vds within tolerance
    new_vds = new_vds + vds_diff
    #if the actual vds is not within the measurement tolerance
    if vds_diff > meas_tol:
        #set vds to estimated value to get vds within tolerance
        set_vds(device,waveform_generator,new_vds)
        #recursively call measurement function to repeat until within vds tolerance
        data = get_reading(device,multimeter,waveform_generator,vds,new_vds,vgs,res)
    #if actual vds is within tolerance
    else:
        #return measurements
        data = [vgs,vds,id,vds_diff]
    return data

#sets vgs of test MOSFET
#adjusts desired vgs to accomodate 50ohm output mode
#vgs is on channel 2 of the waveform generator
def set_vgs(device,waveform_generator,vgs):
    #adjust to accomodate 50ohm output mode
    adjusted_vgs = round(vgs/2,3)
    #set voltage
    device[waveform_generator].write("SOUR2:VOLT:LEV:IMM:OFFS ",str(adjusted_vgs))

#sets vds og test MOSFET
#adjusts desired vds to accomodate 50ohm output mode
#vds is on channel 1 of the waveform generator    
def set_vds(device,waveform_generator,vds):
    #adjust to accomodate 50ohm output mode
    adjusted_vds = round(vds/2,4)
    #set voltage
    device[waveform_generator].write("SOUR1:VOLT:LEV:IMM:OFFS ",str(adjusted_vds))

#formats measurements for readability and outputs to .txt file
#just one line of code, but makes main code more readable
def write_output(id_reading,output_file):
    output_file.write("%.2f           %.2f          %.8f      %.4f\r" % (id_reading[0], id_reading[1], id_reading[2], id_reading[3]))

#turns off waveform generator channels and closes connections
#still doesn't seem to actually close connections
#power cycling devices really closes connections
def device_exit(device,waveform_generator,multimeter):
    print("Closing devices...")
    sleep(1)
    #turn off waveform generator outputs
    device[waveform_generator].write("OUTP1:STAT 0")
    device[waveform_generator].write("OUTP2:STAT 0")
    #close out device connections
    device[waveform_generator].close()
    device[multimeter].close()
    print("Devices closed")
    sleep(1)

#plots id vs vds curves with multiple vgs values
#everything is on the same plot for comparison purposes
def id_vds_curve_plotter(id_reading,vgs_sweep,vds_sweep):
    print("Plotting ID VS VDS Curves")
    sleep(1)
    #create list for y values
    id_plot = []    
    #since every measurement is in one big list, it needs to be
    #broken apart for different tests with different vgs values.
    #creates one plot line for every vgs value tested
    #outer iteration goes through possible vgs values
    #inner iteration goes through possible vds values
    for i in range(len(vgs_sweep)):
        for j in range(len(vds_sweep)):
            #keep absolute location within big ol list
            data = (i*len(vds_sweep))+j
            #if this is the first iteration through the list
            if i == 0:
                #populate y value array with drain current readings
                id_plot.append(id_reading[j][2])
            #if this isnt the first iteration through the list
            else:
                #reassign y value array with correct drain current readings for associated vgs
                id_plot[j] = id_reading[data][2]
        #when every vds value for a given vgs is assigned
        #create a new plot line for the given vgs value
        plotter.plot(vds_sweep,id_plot, label = "V_GS: %.2f" % (vgs_sweep[i]), linewidth = '1')
    #give plot some data for readability
    plotter.title("Measured ID VS. VDS Curve")
    plotter.xlabel("VDS (V)")
    plotter.ylabel("ID (A)")
    plotter.legend()
    #actually show the plot
    plotter.show()
    print("Plotting Complete")

#PROGRAM STARTS HERE
#creates resource manager object. it's supposed to just find
#the resource manager file, so no need for an argument
resource_manager = pyvisa.ResourceManager()

#necessary global variables can be found here
device = []                             #device object list, used for benchtop instruments
device_count = 0                        #keeps count of usb devices found
vgs_sweep = []                          #vgs_sweep values list
vds_sweep = []                          #vds_sweep values list
res = 0                                 #feedback resistor in test setup
id_reading = []                         #list with drain current reading and associated voltages
output_file = open("ID_VDS_MEASUREMENTS.txt", "w")  #dump file for measurements

#find devices and populate device object list
device = acquire_devices()

#identify devices in device object list
print("Device Identification in progress...")
for i in range(len(device)):                        #for all devices
    temp_device = identify_device(device,i)         #use device object identifier function
    if temp_device.find("Waveform Generator") != -1:#if waveform generator is identified device
        waveform_generator = i                      #waveform generator is device object i
        device_count = device_count + 1             #increment device count
    elif temp_device.find("Multimeter") != -1:      #if multimeter is identified object
        multimeter = i                              #multimeter is device object i
        device_count = device_count + 1             #increment device count
    else:                                           #if it is a mystery device
        continue                                    #this iteration doesn't matter
if device_count < 2:                                #close program if there aren't enough devices
    print("One or more devices missing. Consult previous output to identify which is missing")
    exit()
print("Device Identification Complete")
sleep(1)

#set up vgs_sweep list for measurements
vgs_sweep = vgs_setup()

#set up vds_sweep list for measurements
vds_sweep = vds_setup()

#get feedback resistor value
print("Enter measured value of feedback resistor (in ohms)")
res = float(input())

#set up waveform generator before measurements are performed
wg_setup(device,waveform_generator)

#actually take measurements of drain current
#not broken into a function because it would require a lot of arguments
#line below gives output file a header which identifies data
output_file.write("V_GS (V)       V_DS (V)      I_D (A)         V_DS difference(V)\r")
#below code runs through sweep
#outer iteration sweeps gate->source voltage
#inner iteration sweeps drain->source voltage
print("Now measuring. This may take some time.")
print("If measurement tolerance is high, this will take longer.")
print("Devices should be making clicking noises.")
print("If devices are beeping or giving error messages, check that setup ran correctly.")
for i in range(len(vgs_sweep)):
    #set vgs for following vds sweep
    set_vgs(device,waveform_generator,vgs_sweep[i])
    sleep(0.1)
    for j in range(len(vds_sweep)):
        #set vds
        set_vds(device,waveform_generator,vds_sweep[j])
        #gets i_d reading, returns i_d and associated voltages to list
        #sends vds_sweep twice due to recursive algorithm used to get reading
        #this gives the algorithm a comparison point to decide whether to reiterate
        id_reading.append(get_reading(device,multimeter,waveform_generator,vds_sweep[j],vds_sweep[j],vgs_sweep[i],res))
        #prints formatted output to output file
        #math in id_reading index keeps track of absolute position within list
        write_output(id_reading[(i*len(vds_sweep))+j],output_file)
print("Measurements complete")

#close out devices and files once they aren't needed
device_exit(device,waveform_generator,multimeter)
output_file.close()

#plot the measured output
id_vds_curve_plotter(id_reading,vgs_sweep,vds_sweep)
