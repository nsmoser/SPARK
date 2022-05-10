# SPARK
Semiconductor Parameter Analyzer Replacement Kit

Goal is to replace the B1500A with benchtop equipment, lab kit parts, and a python script.

Should be able to measure MOSFET drain current across a sweep of drain-source voltages with different gate-source voltages when complete.

Test setup is an inverting feedback op amp where input current is MOSFET under test. This should create a transimpedance amplifier.

![SPARK_test_setup](https://user-images.githubusercontent.com/43865671/167732784-cd54be0c-01a8-43ab-a453-be0a004aab2c.png)

In this case, I_in is I_d of the MOSFET under test.

Output voltage is measured using multimeter, and is a function of drain current and feedback resistor.

v_out = -i_d\*r_f -> i_d = -v_out/r_f

There is some error, as always, but for the purposes of EE330 this is more than sufficient to isolate MOSFET square law parameters.
The largest source of error is mismeasurement of feedback resistance or the waveform generator to MOSFET impedance.
If the op amp is poor quality or is not sufficiently powered, it can contribute error as well.
With the version 1.2 update, measurement error can be more easily isolated with a v_ds difference metric being returned.

### Version 1.2 Update
- Changed output waveform on waveform generator from 1uhz square wave to DC source
- Added recursive algorithm to adjust waveform generator output to accomodate output impedance and reduce measurement error
- Added v_ds difference metric to text output to help isolate any v_ds measurement accuracy errors

#### How does the v_ds adjustment algorithm work?
As there is an impedance between the waveform generator and the MOSFET drain, the voltage set as v_ds at the waveform generator is not the actual v_ds value.
This was found to be the largest source of error in version 1.0 and version 1.1. However, as only one node voltage can be measured with the multimeter, 
there is no direct method to measure v_ds. Therefore, a v_ds correction method was needed to make measurements more accurate.
This algorithm follows a three-step process:
- Take the measured drain current and find the voltage drop from the waveform generator to MOSFET drain
- Find the actual v_ds of the MOSFET, and compare it to the voltage set at the waveform generator
- If the difference between the two voltages is beyond a certain measurement accuracy tolerance, increase voltage set at waveform generator by the difference in measured voltages

These three steps are repeated recursively until the difference between voltages are at a certain tolerance.
For this algorithm to work, values for output impedance and measurement accuracy tolerance must be set in the get_reading() function.
Output impedance is the measured impedance in ohms from the waveform generator to MOSFET drain.
Measurement accuracy tolerance is the acceptable deviation of the measured v_ds from the voltage set at the waveform generator in volts.
Depending on the measurement accuracy tolerance, this can add significant measurement time.
##### How to set output impedance and v_ds measurement accuracy tolerance 
- enter the get_reading() function within SPARK.py
- set adapter_impedance to measured impedance between waveform generator and MOSFET drain
    - Usually a 50 ohm bnc-to-banana adapter plus any impedance in wires
- set meas_tol to desired measurement accuracy tolerance.
    - Default is 5mV, usually tolerance within one measurement step is best.

### Equipment used:
- Keysight EDU32212A Waveform Generator
    - Channel one drives MOSFET drain
    - Channel two drives MOSFET gate
- Keysight 34470A Multimeter
- MOSFET to test
- Breadboard or other prototyping platform
- Operational amplifier (LM324, TL082 tested)
- Feedback resistor (3.3kohm worked well in testing with op amp Vdd/Vss = +/-10V)
- Assorted jumper wires as needed
                
### Software Needed:
- Python 3.10 (Any version of Python 3 is probably fine)

- pyvisa Library (python -m pip install pyvisa)

- matplotlib Library (python -m pip install matplotlib)

- Keysight IOLibrary Suite (https://www.keysight.com/us/en/lib/software-detail/computer-software/io-libraries-suite-downloads-2175637.html)
                 
### Good References:
- PyVISA Reference (https://pyvisa.readthedocs.io/en/latest/)

- SCPI Waveform Generator Reference (https://cdn.teledynelecroy.com/files/manuals/t3awg3kseries-afg-pm.pdf)

    - Note: The keysight reference for waveform generators sucks. This isn't a keysight device, but is much more readable and applicable

- SCPI Multimeter Reference (https://rfmw.em.keysight.com/bihelpfiles/Truevolt/WebHelp/US/Content/_Home_Page/SCPI%20%20Welcome.htm)

Any debugging for this script can usually be traced back to an issue with PyVISA. 

Python and PyVISA offer pretty good debugging information, so that is a good place to start. 

Additionally, the script prints relevant debugging information if it encounters a known issue. 


