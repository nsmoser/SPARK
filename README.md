# SPARK
Semiconductor Parameter Analyzer Replacement Kit

Goal is to replace the B1500A with benchtop equipment, lab kit parts, and a python script.

Prompts user for v_ds and v_gs sweep range and sweep step via command line (example: v_ds start at 0.0v, end at 2.5v step at 0.05v).
Prompts user for value, in ohms, of feedback resistor used in test setup via command line.

Measures MOSFET drain current across a sweep of drain-source voltages with different gate-source voltages. Collects i_d/v_ds data, outputs data to 
text file, and plots curves. Text file output can be found in python file run directory. Plot appears automatically and can be saved.
Data collected can be used to derive square law model parameters for MOSFET under test.

The speed of the program is determined by the speed at which lab equipment can take measurements and the measurement tolerance for 
the MOSFET's v_ds. Average execution time in testing was found to be within the 1 to 5 minute range.

Test setup is an inverting feedback op amp where input current comes from MOSFET under test. This should create a transresistance amplifier.

![SPARK_test_setup](https://user-images.githubusercontent.com/43865671/167732784-cd54be0c-01a8-43ab-a453-be0a004aab2c.png)

In this case, input current is i_d of the MOSFET under test in series with the output impedance of the waveform generator.

Output voltage is measured using multimeter, and is a function of drain current and feedback resistor.

v_out = -i_d\*r_f -> i_d = -v_out/r_f

For best results, measure value of r_f with a multimeter instead of using its listed value. An incorrect r_f value will ruin both the current measurement and
the algorithm used to adjust v_ds.

There is some error, as always, but this software is more than accurate enough to isolate MOSFET square law parameters given a proper r_f value is provided.
The largest deviation in drain current from the B1500A measurements in testing was in the 10uA range. 
The largest source of error is mismeasurement of feedback resistance or the waveform generator to MOSFET impedance.
If the op amp is poor quality, damaged, or is not sufficiently powered, it can contribute error as well.
With the version 1.2 update, measurement error can be more easily isolated with a v_ds difference metric being returned. This metric is the difference between the 
v_ds set at the waveform generator and actual v_ds.

## Version 1.2 Update
- Changed output waveform on waveform generator from 1uhz square wave to DC source
- Added recursive algorithm to adjust waveform generator output to accomodate output impedance and reduce measurement error
- Added v_ds difference metric to text output to help isolate any v_ds measurement accuracy errors

### How does the v_ds adjustment algorithm work?
As there is an impedance between the waveform generator and the MOSFET drain, the voltage set as v_ds at the waveform generator is not the actual v_ds value.
This was found to be the largest source of error in versions 1.0 and 1.1 of SPARK. However, as only one node voltage can be measured with the multimeter, 
there is no direct method to measure v_ds. Therefore, a v_ds correction method was needed to make measurements more accurate.
This algorithm follows a three-step process:
- Take the measured drain current and find the voltage drop across the impedance from the waveform generator to MOSFET drain
- Find the actual v_ds of the MOSFET, and compare it to the voltage set at the waveform generator
- If the difference between the two voltages is beyond a certain measurement accuracy tolerance, increase voltage set at waveform generator by the difference in measured voltages

These three steps are repeated recursively until the difference between voltages are at a certain tolerance.
For this algorithm to work, values for output impedance and measurement accuracy tolerance must be set in the get_reading() function.
Output impedance is the measured impedance in ohms from the waveform generator to MOSFET drain.
Measurement accuracy tolerance is the acceptable deviation of the measured v_ds from the voltage set at the waveform generator in volts.
Depending on the measurement accuracy tolerance, this can add significant measurement time.
#### How to set output impedance and v_ds measurement accuracy tolerance 
- enter the get_reading() function within SPARK.py
- set adapter_impedance to measured impedance between waveform generator and MOSFET drain
    - Default is 50 ohms, but could be measured more accurately. Small enough that 50 ohms is good enough
- set meas_tol to desired measurement accuracy tolerance.
    - Default is 5mV, usually tolerance within 10% of one measurement step is best balance of accuracy and required run time.

## Equipment used:
- Keysight EDU32212A Waveform Generator
    - Channel one drives MOSFET drain
    - Channel two drives MOSFET gate
- Keysight 34470A Multimeter
- MOSFET to test
- Breadboard or other prototyping platform
- Operational amplifier (LM324 and TL082 tested)
- Benchtop power supply
    - Set Vdd/Vss of operational amplifier
    - Run additional tests by setting MOSFET bulk voltage
- Feedback resistor (3.3kohm worked well in testing with op amp Vdd/Vss = +/-10V)
- Assorted jumper wires as needed
                
## Software Needed:
- Python 3.10 (Any version of Python 3 is probably fine)

- pyvisa Library (python -m pip install pyvisa)

- matplotlib Library (python -m pip install matplotlib)

- Keysight IOLibrary Suite (https://www.keysight.com/us/en/lib/software-detail/computer-software/io-libraries-suite-downloads-2175637.html)
    - Should be pre-installed on all ISU lab computers
                 
## Good References:
- PyVISA Reference (https://pyvisa.readthedocs.io/en/latest/)

- SCPI Waveform Generator Reference (https://cdn.teledynelecroy.com/files/manuals/t3awg3kseries-afg-pm.pdf)

    - Note: The Keysight reference for waveform generators isn't great. This isn't a keysight device, but is much more readable. Since SCPI is a standard, they are applicable.

- SCPI Multimeter Reference (https://rfmw.em.keysight.com/bihelpfiles/Truevolt/WebHelp/US/Content/_Home_Page/SCPI%20%20Welcome.htm)

## Debugging Info
Any debugging for this script can usually be traced back to an issue with PyVISA. The script prints relevant debugging information as it operates and if it encounters a known issue. If any unknown or new issues are encountered, please reach out at nickolasmoser0@gmail.com.


