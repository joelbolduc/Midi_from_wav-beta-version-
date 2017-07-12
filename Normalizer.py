import numpy as np
import math
from scipy.io.wavfile import read
from scipy.io.wavfile import write
from PIL import Image
import scipy.misc
import random
import time
import matplotlib.pyplot as plt
import scipy.misc
import cmath


def intensity(s):
#Computes the intensity, a.k.a the absolute value of the point of the wave furthest away from 0.
    M=0
    for i in range(len(s)):
        if(abs(float(s[i]))>M):
            M=abs(float(s[i]))
    return M
        
        

def normalize(file,noise_threshold=-80):
#Normalizes the total sound wave so that amplitude is equal throughout the sound wave.
    name=file[:len(file)-4]
    noise_threshold=pow(10.0,(-6+noise_threshold)/20.0)
    #convert the decibel threshold to linear representation.
    #-6 decibels are added because the average section of the chunk is multiplied by 0.5 when the chunks are pieced back together.
    sound_wave=read(file)[1]
    padding=list([0]*689)
    sound_wave=np.concatenate((list(padding),sound_wave,list(padding)))
    outsound=list([0]*(len(sound_wave)))
    #outsound is initialized to a array of 0s.
    i=0
    current_chunk_intensity=0
    maximum_intensity=0
    #maximum intensity of all chunks is calculated.
    while(i+1378<len(sound_wave)):
        current_chunk_intensity=intensity(sound_wave[i:i+1378])
        if(current_chunk_intensity>maximum_intensity):
            maximum_intensity=current_chunk_intensity
        i=i+689
    i=0
    #all chunks brought back to the same intensity
    print('Normalization of submitted wav file :')
    while(i+1378<len(sound_wave)):
        if(i%137800==0):
            print(str(i//689)+'/'+str(len(sound_wave)//689)+' chunks normalized.')
        last_chunk_intensity=current_chunk_intensity
        current_chunk_intensity=intensity(sound_wave[i:i+1378])
        for j in range(1378):
            if(0.5*(last_chunk_intensity+current_chunk_intensity)<maximum_intensity*noise_threshold):
                pass
            else:
                outsound[i+j]+=float(((0.5-0.5*math.cos(2*math.pi*j/1378))*float(sound_wave[i+j]))/(last_chunk_intensity+current_chunk_intensity))
        i=i+689
    outsound_scaled=outsound/np.max(np.abs(outsound))
    #scaled up so that the point of the wave with biggest absolute value is at 1 or -1.
    outsound_cropped=[]
    #when scaled up this way, a few points are quite far from the area that contains most of the wave.
    #There extreme values are cropped out by multiplying the wave by 4/3 and clipping whatever outside of [-1,1].
    for i in range(len(outsound_scaled)):
        s=(4/3)*outsound_scaled[i]
        if(s>1):
            s=1
        elif(s<-1):
            s=-1
        else:
            pass
        outsound_cropped.append(s)
    write(name+'_optimized.wav',44100,np.asarray(outsound_cropped))
