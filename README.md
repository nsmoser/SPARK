# SPARK
Semiconductor Parameter Analyzer Replacement Kit

Currently a work in progress; still needs:
- Method to handle more than two identifiable devices
- Take measurements across v_gs and v_ds sweep values
- Dump measurement values to txt file or other file
- Plot measurement values

Goal is to replace the super expensive, super scary B1500A
with benchtop equipment and a python script for purposes of EE330.

Should be able to measure MOSFET drain current across a sweep of drain-source
voltages with different gate-source voltages when complete.

Equipment used:
- Keysight EDU32212A Waveform Generator
- Keysight 34470A Multimeter
                
Software Needed:
- Python 3.10

- PyVISA Library (python3 -m pip install pyvisa)

- Keysight IOLibrary Suite (https://www.keysight.com/us/en/lib/software-detail/computer-software/io-libraries-suite-downloads-2175637.html)
                 
Good References:
- PyVISA Reference (https://pyvisa.readthedocs.io/en/latest/)

- SCPI Waveform Generator Reference (https://cdn.teledynelecroy.com/files/manuals/t3awg3kseries-afg-pm.pdf)

- Note: The keysight reference for waveform generators sucks. This isn't a keysight device, but is much more readable and applicable

- SCPI Multimeter Reference (https://rfmw.em.keysight.com/bihelpfiles/Truevolt/WebHelp/US/Content/_Home_Page/SCPI%20%20Welcome.htm)
