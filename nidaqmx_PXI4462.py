import nidaqmx
import numpy as np
from nidaqmx.constants import Edge, AcquisitionType, TriggerUsage, Coupling, VoltageUnits, TerminalConfiguration
import datetime
import time
from scipy.io import savemat
import nidaqmx.stream_readers
Active_chan_PXI1Slot4_0 = ("PXI1Slot4/ai0")
Active_chan_PXI1Slot4_1 = ("PXI1Slot4/ai1")
Active_chan_PXI1Slot4_2 = ("PXI1Slot4/ai2")
Active_chan_PXI1Slot4_3 = ("PXI1Slot4/ai3")
#For PXI-4462: Limit for number of samples is Following 
#Maximum Value: 16777215 samples per channel
#Minimum Value: 32 samples samples per channel
#For PXI-4462:  Acquisition Frequency is Following 
#Maximum Value: 204800 Hz
#Minimum Value: 32 Hz
Samples_Per_Sec = 50000 #Acquisition frequency
samps_per_chan=15000000 #Number of samples per channel should be less than or equal to 16777215
samps_per_file=30000000 #Number of samples per channel to be written in a single file
#Following line determines the name of the file you will want to save
#This name will also be followed by the number mentioned by 'i' which can iterate in increment of one
name = 'Acqui_1_'
i=0
#Following line determsines the number of iterations you will want to perform for acquisition of data
#For Ex: If you want 'n' no of iterations you can put 'range(n+1)'===>The loop will stop at 'n'
num_files=5 # For ex: If one file takes 10 mins for data acquisition; you will acquire data for "num_files*10" mins of time
SPC = samps_per_chan # Just a dummy variable to pass on to the function
arr = (samps_per_chan)
for i in range(num_files):
    print("You are in Loop No:",i)
    with nidaqmx.Task() as task:
        #You can change the properties of channel by editing the following lines such as range, units, terminal
        #configuration and couplings of each channel seperately.
        chan0 = task.ai_channels.add_ai_voltage_chan(Active_chan_PXI1Slot4_0,terminal_config=TerminalConfiguration.DIFFERENTIAL,
                                             min_val=-3.16, max_val=3.16,units=VoltageUnits.VOLTS) # For PXI - 4462
        chan0.ai_coupling = Coupling.DC 
        chan1 = task.ai_channels.add_ai_voltage_chan(Active_chan_PXI1Slot4_1,terminal_config=TerminalConfiguration.DIFFERENTIAL,
                                             min_val=-0.316, max_val=0.316,units=VoltageUnits.VOLTS) # For PXI - 4462
        chan1.ai_coupling = Coupling.DC
        chan2 = task.ai_channels.add_ai_voltage_chan(Active_chan_PXI1Slot4_2,terminal_config=TerminalConfiguration.DIFFERENTIAL,
                                             min_val=-1.0, max_val=1.0,units=VoltageUnits.VOLTS) # For PXI - 4462
        chan2.ai_coupling = Coupling.DC
        chan3 = task.ai_channels.add_ai_voltage_chan(Active_chan_PXI1Slot4_3,terminal_config=TerminalConfiguration.DIFFERENTIAL,
                                             min_val=-10.0, max_val=10.0,units=VoltageUnits.VOLTS) # For PXI - 4462
        chan3.ai_coupling = Coupling.DC
        task.timing.cfg_samp_clk_timing(Samples_Per_Sec, source="", 
           active_edge=Edge.RISING,sample_mode=AcquisitionType.CONTINUOUS,samps_per_chan=SPC)
        #Following line is to create a preallocated numpy array of size(active number of channels,samps_per_file)
        #Here RAM is used to preallocated the array in case we wants to acquire continuous data which is more than onboard memory.
        data=np.ndarray((4,samps_per_file),dtype=np.float64)
        #Following line acquires the samples and writes it in the variable we created named "data"
        q=nidaqmx.stream_readers.AnalogMultiChannelReader(task.in_stream).read_many_sample(data,samps_per_file,timeout=nidaqmx.constants.WAIT_INFINITELY)
        #Following line is optional; it is helpful if you use Matlab/Octave for post-processing of data
        #Following line saves the array 'data' which is in 'numpy.ndarray' to '.mat' file in your working directory.
        savemat ("%s%d" % (name,i), {'data': data})  
             
print("Done!")        


                          
