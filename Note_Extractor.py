import numpy as np
import math
from scipy.io.wavfile import read
from scipy.io.wavfile import write
from PIL import Image
import scipy.misc
import random
import time
import scipy.misc
import cmath
import Normalizer
    

def extract_notes(file,timestep,spectrum_bounds,tolerance):
   """Extracts notes from wav file. Currently in beta stage :
       only returnes the list of all notes and intensities at each time in a table
       in the format : (time,(note,intensity))
       Takes the following arguments :
       -file (string) : name of the file
       -timestep, the length of the atoms of time over which the notes are extracted
       -spectrum_bounds ([lower_frequency,higher_frequency]) : is the range of frequency (minimum 1 Hz) which are to be included in analysis.
       It is advised to cut around 1000 Hz (unless fundamentals are higher) to avoid the inclusion of harmonics in the list of notes.
       -tolerance (float) : indicates under what intensity a frequency is just dropped (in proportion to maximum intensity). By default, choose 0.25."""
    beg=int(timestep*spectrum_bounds[0]/44100)
    end=int(timestep*spectrum_bounds[1]/44100)
    sound=read(file)[1]
    if(len(file)%(timestep/2)==0):
        padding=0
    else:
        padding=int(((1+(len(file)//(timestep/2)))*timestep/2)-len(file))
    sound=np.concatenate((sound,list([0]*padding)))
    ##Here, we look for maximum intensity frequency in order to choose which ones to keep or discard.
    Max=0
    i=0.0
    output_sound=list([0]*len(sound))
    while(i+timestep<len(sound)):
        #Prints progression of the algorithm. This is just done in order to see it's progression during execution.
        if(i%(timestep*100)==0):
            print(i,len(sound))
        I=int(i)
        atom=sound[I:I+timestep]
        atom_spectrum=np.fft.fft(atom)
        M=np.max(np.abs(atom_spectrum[beg:end]))
        if(M>Max):
            Max=M
        i=i+timestep
    i=0.0
    note_list=[]
    #updates the list of notes after finding them. A note is in format (note,intensity)
    while(i+timestep<len(sound)):
        I=int(i)
        atom=sound[I:I+timestep]
        atom_spectrum=np.fft.fft(atom)
        spectrum_modified=[]
        x=0
        notes=[]
        for j in range(1,len(atom_spectrum)-1):
            if(abs(atom_spectrum[j])>abs(atom_spectrum[j-1]) and abs(atom_spectrum[j])>abs(atom_spectrum[j+1]) and j>beg and j<end):
                a=(atom_spectrum[j])
                if(abs(a)>=tolerance*Max):
                    a=(atom_spectrum[j])
                    notes.append((int(12*math.log(j)/math.log(2)),int(127*abs(atom_spectrum[j])/Max)))
                else:
                    a=0
                spectrum_modified.append(a)
            else:
                spectrum_modified.append(0.0) 
        note_list.append((i,notes))
        #Prints progression of the algorithm. This is just done in order to see it's progression during execution.
        if(i%(timestep*100)==0):
            print(i,len(sound))
        atom_modified=np.fft.ifft(spectrum_modified)
        for j in range(len(atom_modified)):
            output_sound[I+j]=(atom_modified[j].real)
        i=i+timestep
    return note_list


Normalizer.normalize('impact.wav')
#normalize sound before execution to avoid silent parts in resulting output due to discarding intensities under the threshold).
cc=compress('impact_optimized.wav',5133,[1,1000],0.25)
#prints the list of notes. For debugging purposes. Will eventually be used to create midi notes.
for i in range(len(cc)):
    print(cc[i])
