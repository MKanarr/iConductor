from gpiozero import Servo
from time import sleep
import time

myGPIO=17
# Min and Max pulse widths converted into milliseconds
# To increase range of movement:
#   increase maxPW from default of 2.0
#   decrease minPW from default of 1.0
# Change myCorrection using increments of 0.05 and
# check the value works with your servo.
myCorrection=0.45
maxPW=(2.0+myCorrection)/1000
minPW=(1.0-myCorrection)/1000

# left and right x axis
myServo = Servo(27,min_pulse_width=minPW,max_pulse_width=maxPW)
# up and down y axis
myServo1 = Servo(22,min_pulse_width=minPW,max_pulse_width=maxPW)

#tempo = input("Enter tempo in BPM: ")

#click_interval = 60 / int(tempo)

#now = time.time()
#next_click = now + click_interval

while True:
    #now = time.time()
    
    #if now >= next_clik:


    #myServo.value=(0.7)
    myServo.value=0
    myServo1.value=1
    sleep(2)
    #myServo.value=(-0.7)
    myServo.value=-1
    myServo1.value=1
    sleep(2)
    myServo.value=-1
    myServo1.value=-1
    sleep(4)
