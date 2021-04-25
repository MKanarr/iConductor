import pyaudio
import matplotlib.pyplot as plt
import numpy as np
import time

form_1 = pyaudio.paInt16
chans = 1
samp_rate = 44100
chunk = 8192
dev_index = 2

audio = pyaudio.PyAudio()

stream = audio.open(format = form_1, rate = samp_rate, channels = chans, input_device_index = dev_index, input = True, frames_per_buffer = chunk)

stream.start_stream()
data = np.fromstring(stream.read(chunk), dtype=np.int16)
stream.stop_stream()

mic_sens_dBV = -47.0
mic_sens_corr = np.power(10.0, mic_sens_dBV / 20.0)

data = ((data / np.power(2.0, 15)) * 5.25) * (mic_sens_corr)

 plt.xlabel('Frequency [Hz]')
plt.ylabel('Amplitude [Pa]')
ax.set_xscale('log')
plt.grid(True)

plt.annotate(r'$\Delta f_{max}$: %2.1f Hz' % (samp_rate / (2 * chunk)), xy = (0.7, 0.92), xycoords = 'figure fraction')

annot = ax.annotate('Freq: %2.1f' % (f_vec[max_loc]), xy = (f_vec[max_loc], fft_data[max_loc]), xycoords = 'data', xytext = (0,30), textcoords = 'offset points', arrowprops = dict(arrowstyle = "->"), ha = 'center', va = 'bottom')

plt.savefig('fft_1kHz_signal.png', dpi = 300, facecolor = '#FCFCFC')
plt.show()