# SPARK
Semiconductor Parameter Analyzer Replacement Kit

Tested and functional in Coover 2046

Goal is to replace the B1500A with benchtop equipment and a python script for purposes of EE330.

Should be able to measure MOSFET drain current across a sweep of drain-source
voltages with different gate-source voltages when complete.

Test setup is an inverting feedback op amp where input resistor is MOSFET under test. This should create a transimpedance amplifier.

![TIA_simple](https://user-images.githubusercontent.com/43865671/163257864-dc657ff9-3cc3-4a45-93ec-551beeb1d63d.svg)

Source: Wikipedia

In this case, I_in is I_d of the MOSFET under test.

Output voltage is measured using multimeter, and is a function of drain current and feedback resistor.

v_out = i_d\*r_f -> i_d = v_out/r_f

Equipment used:
- Keysight EDU32212A Waveform Generator
    - Channel one drives MOSFET drain
    - Channel two drives MOSFET gate
- Keysight 34470A Multimeter
- MOSFET to test
- Breadboard or other prototyping platform
- Op amp limited to +-10V output (LM324, TL082)
- Feedback resistor (3.3kohm worked well in testing)
- Assorted jumper wires as needed
                
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

Any debugging for this script can usually be traced back to an issue with PyVISA. 

Python and PyVISA offer pretty good debugging information, so that is a good place to start. 

Additionally, the script prints relevant debugging information if it encounters a known issue. 
