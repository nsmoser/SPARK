# SPARK
Semiconductor Parameter Analyzer Replacement Kit

Goal is to replace the super expensive, super scary B1500A with benchtop equipment and a python script for purposes of EE330.

Should be able to measure MOSFET drain current across a sweep of drain-source
voltages with different gate-source voltages when complete.

Test setup is an inverting feedback op amp where input resistor is MOSFET under test.

Output voltage is measured using multimeter, and is a function of drain current and feedback resistor.

v_out = i_d\*r_f -> i_d = v_out/r_f

Equipment used:
- Keysight EDU32212A Waveform Generator
    - Channel one drives MOSFET drain
    - Channel two drives MOSFET gate
- Keysight 34470A Multimeter
                
Software Needed:
- Python 3.10

- pyvisa Library (python -m pip install pyvisa)

- matplotlib Library (python -m pip install matplotlib)

- Keysight IOLibrary Suite (https://www.keysight.com/us/en/lib/software-detail/computer-software/io-libraries-suite-downloads-2175637.html)
                 
Good References:
- PyVISA Reference (https://pyvisa.readthedocs.io/en/latest/)

- SCPI Waveform Generator Reference (https://cdn.teledynelecroy.com/files/manuals/t3awg3kseries-afg-pm.pdf)

    - Note: The keysight reference for waveform generators sucks. This isn't a keysight device, but is much more readable and applicable

- SCPI Multimeter Reference (https://rfmw.em.keysight.com/bihelpfiles/Truevolt/WebHelp/US/Content/_Home_Page/SCPI%20%20Welcome.htm)
