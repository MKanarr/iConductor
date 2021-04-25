import pyaudio
import numpy as np
import time
import bisect
import math

pitches = {
	261.6: "C",
	277.2: "C#",
	293.6: "D",
	311.1: "D#",
	329.6: "E",
	349.2: "F",
	370.0: "F#",
	392.0: "G",
	415.3: "Ab",
	440.0: "A",
	466.2: "Bb",
	493.9: "B" 	
}

form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 1 # 1 channel
samp_rate = 44100 # 44.1kHz sampling rate
chunk = 8192 # 2^12 samples for buffer
dev_index = 2 # device index found by p.get_device_info_by_index(ii)

audio = pyaudio.PyAudio() # create pyaudio instantiation

# create pyaudio stream
stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                    input_device_index = dev_index,input = True, \
                    frames_per_buffer=chunk)

# record data chunk 
stream.start_stream()
data = np.fromstring(stream.read(chunk),dtype=np.int16)
stream.stop_stream()

# mic sensitivity correction and bit conversion
mic_sens_dBV = -47.0 # mic sensitivity in dBV + any gain
mic_sens_corr = np.power(10.0,mic_sens_dBV/20.0) # calculate mic sensitivity conversion factor

# (USB=5V, so 15 bits are used (the 16th for negatives)) and the manufacturer microphone sensitivity corrections
data = ((data/np.power(2.0,15))*5.25)*(mic_sens_corr) 


# compute FFT parameters
f_vec = samp_rate*np.arange(chunk/2)/chunk # frequency vector based on window size and sample rate
mic_low_freq = 100 # low frequency response of the mic (mine in this case is 100 Hz)
low_freq_loc = np.argmin(np.abs(f_vec-mic_low_freq))
fft_data = (np.abs(np.fft.fft(data))[0:int(np.floor(chunk/2))])/chunk
fft_data[1:] = 2*fft_data[1:]

max_loc = np.argmax(fft_data[low_freq_loc:])+low_freq_loc

target = f_vec[max_loc]

notes = list(pitches.values())
real_values = np.array(list(pitches.keys()))
target_arr = np.empty(len(real_values), dtype=float)
target_arr.fill(target)
diff = np.subtract(real_values, target_arr)
idx = (diff >= float(-3)) * (diff <= float(3))
index = np.where(idx)

print('Note: ', notes[index[0][0]])
