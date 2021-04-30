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

# motor connected to left of robot moves arm up and down
myServo = Servo(27,min_pulse_width=minPW,max_pulse_width=maxPW)
# motor connected to right of robot moves arm forward
myServo1 = Servo(22,min_pulse_width=minPW,max_pulse_width=maxPW)
# motor connected to base of robot moves arm left and right
myServo2 = Servo(17,min_pulse_width=minPW,max_pulse_width=maxPW)

#tempo = input("Enter tempo in BPM: ")

#click_interval=60/int(tempo)

#2/4 pattern
sleep(0.5)
myServo.value=0
myServo1.value=0
myServo2.value=0
sleep(0.5)
myServo.value=0.5
myServo1.value=-0.5
sleep(0.5)
myServo.value=-0.025
myServo1.value=0.025
myServo2.value=0.5
sleep(0.5)
myServo.value=0.5
myServo1.value=-0.5
myServo2.value=0
sleep(0.5)
myServo.value=0
myServo1.value=0
myServo2.value=0
sleep(0.5)
#3/4 pattern
'''
while True: 
    #print("debugging servo") 
    #print("0")
    sleep(0.5)
    myServo.value=0
    myServo1.value=0
    myServo2.value=0
    sleep(0.5)
    #print("0.5")
    myServo.value=0.5   
    myServo1.value=-0.5
    myServo2.value=0
    sleep(0.5)
    #print("0")
    myServo2.value=0.5
    #myServo.value=0
    #myServo1.value=0
    sleep(0.5)
    myServo.value=0 
    myServo1.value=0
    myServo2.value=0
    sleep(0.5)
'''
