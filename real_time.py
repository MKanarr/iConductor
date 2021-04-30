from gpiozero import RGBLED, LED, Button, LEDBoard, OutputDeviceError, LEDCollection
import pyaudio
import numpy as np
import time
import math

class SevenSegmentDisplay(LEDBoard):
    """
    Extends :class:`LEDBoard` for a 7 segment LED display 

    7 segment displays have either 7 or 8 pins, 7 pins for the digit display 
    and an optional 8th pin for a decimal point. 7 segment displays 
    typically have either a common anode or common cathode pin, when
    using a common anode display 'active_high' should be set to False.
    Instances of this class can be used to display characters or control 
    individual leds on the display. For example::

        from gpiozero import SevenSegmentDisplay

        seven = SevenSegmentDisplay(1,2,3,4,5,6,7,8,active_high=False)
        seven.display("7")
    
    :param int \*pins:
        Specify the GPIO pins that the 7 segment display is attached to.
        Pins should be in the LED segment order A,B,C,D,E,F,G,decimal_point 
        (the decimal_point is optional).

    :param bool pwm:
        If ``True``, construct :class:`PWMLED` instances for each pin. If
        ``False`` (the default), construct regular :class:`LED` instances. This
        parameter can only be specified as a keyword parameter.

    :param bool active_high:
        If ``True`` (the default), the :meth:`on` method will set all the
        associated pins to HIGH. If ``False``, the :meth:`on` method will set
        all pins to LOW (the :meth:`off` method always does the opposite). This
        parameter can only be specified as a keyword parameter.

    :param bool initial_value:
        If ``False`` (the default), all LEDs will be off initially. If
        ``None``, each device will be left in whatever state the pin is found
        in when configured for output (warning: this can be on). If ``True``,
        the device will be switched on initially. This parameter can only be
        specified as a keyword parameter.    
    
    """
    def __init__(self, *pins, **kwargs):
        # 7 segment displays must have 7 or 8 pins
        if len(pins) < 7 or len(pins) > 8:
            raise ValueError('SevenSegmentDisplay must have 7 or 8 pins')
        # Don't allow 7 segments to contain collections
        for pin in pins:
            assert not isinstance(pin, LEDCollection)
        pwm = kwargs.pop('pwm', False)
        active_high = kwargs.pop('active_high', True)
        initial_value = kwargs.pop('initial_value', False)
        if kwargs:
            raise TypeError('unexpected keyword argument: %s' % kwargs.popitem()[0])
            
        self._layouts = {
            '1': (False, True, True, False, False, False, False),
            '2': (True, True, False, True, True, False, True),
            '3': (True, True, True, True, False, False, True),
            '4': (False, True, True, False, False, True, True),
            '5': (True, False, True, True, False, True, True),
            '6': (True, False, True, True, True, True, True),
            '7': (True, True, True, False, False, False, False),
            '8': (True, True, True, True, True, True, True),
            '9': (True, True, True, True, False, True, True),
            '0': (True, True, True, True, True, True, False),
            'A': (True, True, True, False, True, True, True),
            'B': (False, False, True, True, True, True, True),
            'C': (True, False, False, True, True, True, False),
            'D': (False, True, True, True, True, False, True),
            'E': (True, False, False, True, True, True, True),
            'F': (True, False, False, False, True, True, True),
            'G': (True, False, True, True, True, True, False),
            'H': (False, True, True, False, True, True, True),
            'I': (False, False, False, False, True, True, False),
            'J': (False, True, True, True, True, False, False),
            'K': (True, False, True, False, True, True, True),
            'L': (False, False, False, True, True, True, False),
            'M': (True, False, True, False, True, False, False),
            'N': (True, True, True, False, True, True, False),
            'O': (True, True, True, True, True, True, False),
            'P': (True, True, False, False, True, True, True),
            'Q': (True, True, False, True, False, True, True),
            'R': (True, True, False, False, True, True, False),
            'S': (True, False, True, True, False, True, True),
            'T': (False, False, False, True, True, True, True),
            'U': (False, False, True, True, True, False, False),
            'V': (False, True, True, True, True, True, False),
            'W': (False, True, False, True, False, True, False),
            'X': (False, True, True, False, True, True, True),
            'Y': (False, True, True, True, False, True, True),
            'Z': (True, True, False, True, True, False, True),
            '-': (False, False, False, False, False, False, True),
            ' ': (False, False, False, False, False, False, False),
            '=': (False, False, False, True, False, False, True)
        }
        
        super(SevenSegmentDisplay, self).__init__(*pins, pwm=pwm, active_high=active_high, initial_value=initial_value)
    
    def display(self, char):
        """
        Display a character on the 7 segment display

        :param string char:
            A single character to be displayed 
        """
        char = str(char).upper()
        if len(char) > 1:
            raise ValueError('only a single character can be displayed')
        if char not in self._layouts:
            raise ValueError('there is no layout for character - %s' % char)
        layout = self._layouts[char]
        for led in range(7):
            self[led].value = layout[led]
            
    def display_hex(self, hexnumber):
        """
        Display a hex number (0-F) on the 7 segment display

        :param int hexnumber:
            The number to be displayed in hex 
        """
        self.display(hex(hexnumber)[2:])

    @property
    def decimal_point(self):
        """
        Represents the status of the decimal point led
        """
        # does the 7seg display have a decimal point (i.e pin 8)
        if len(self) > 7:
            return self[7].value 
        else:
            raise OutputDeviceError('there is no 8th pin for the decimal point')
    
    @decimal_point.setter
    def decimal_point(self, value):
        """
        Sets the status of the decimal point led
        """
        if len(self) > 7:
            self[7].value = value
        else:
            raise OutputDeviceError('there is no 8th pin for the decimal point')    
    
    def set_char_layout(self, char, layout):
        """
        Create or update a custom character layout, which can be used with the 
        `display` method.

        :param string char:
            A single character to be displayed 
            
        :param tuple layout:
            A 7 bool tuple of LED values in the segment order A, B, C, D, E, F, G
        """
        char = str(char).upper()
        if len(char) != 1:
            raise ValueError('only a single character can be used in a layout')
        if len(layout) != 7:
            raise ValueError('a character layout must have 7 segments')
        self._layouts[char] = layout

# sevsegdisp = SevenSegmentDisplay(5, 6, 13, 19, 26, 12, 20)
# sevsegdisp2 = SevenSegmentDisplay(4, 17, 27, 22, 18, 23, 24)
# sevsegdisp.display(notes[index[0][0]])
# sevsegdisp2.display(notes[index[0][0]])
# time.sleep(15)
# sevsegdisp.display(" ")
# sevsegdisp2.display(" ")

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

# top 
sevsegdisp = SevenSegmentDisplay(5, 6, 13, 19, 26, 12, 20)
# bot
sevsegdisp2 = SevenSegmentDisplay(4, 17, 27, 22, 18, 23, 24)

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
note = notes[index[0][0]]

if "#" in note:
    print("sharp")
    sevsegdisp.display(note[0])
    sevsegdisp2.display("=")
elif "b" in note:
    print("flat")
    sevsegdisp.display(note[0])
    sevsegdisp2.display("-")
else:
    sevsegdisp.display(note[0])
    sevsegdisp2.display(" ")

print('Note: ', note)

time.sleep(10)
sevsegdisp.display(" ")
sevsegdisp2.display(" ")