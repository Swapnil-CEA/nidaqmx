# nidaqmx
Data acquisition using "nidaqmx" python module for National Instruments PXI cards. 
Following are the specifications of the system on which this code has been tested.
Chassis: NI PXIe-1071; Controller:NI PXIe-8820; Data Acquisition Card: NI PXI-4462.
This python script is basically written to acquire data for a typical hot wire experiment
in the field of Turbulence. But, neverthless it can be modified as per the requirements of the user.
This python script uses the preallocated memory using the "nidaqmx.stream_readers" module in order to
acquire the CONTINUOUS data which is typically more than the onboard memory of the PXI card.
