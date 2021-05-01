from gpiozero import Servo
from time import sleep
import time

def threeFour(num_clicks,tempo_int,myServo,myServo1,myServo2):
    count=0

    while count!=num_clicks:
        #3/4 pattern
        sleep(tempo_int)
        myServo.value=0
        myServo1.value=0
        myServo2.value=0
        sleep(tempo_int)
        myServo.value=0.5   
        myServo1.value=-0.5
        myServo2.value=0
        count+=1
        sleep(tempo_int)
        myServo2.value=0.5
        #myServo.value=0
        #myServo1.value=0
        count+=1
        sleep(tempo_int)
        myServo.value=0 
        myServo1.value=0
        myServo2.value=0
        count+=1
        sleep(tempo_int)

    return True

def twoFour(num_clicks,tempo_int,myServo,myServo1,myServo2):
    count=0 

    while count!=num_clicks:
        #2/4 pattern
        sleep(tempo_int)
        myServo.value=0
        myServo1.value=0
        myServo2.value=0
        sleep(tempo_int)
        myServo.value=0.5
        myServo1.value=-0.5
        count+=1
        sleep(tempo_int)
        myServo.value=-0.025
        myServo1.value=0.025
        myServo2.value=0.5
        sleep(tempo_int)
        myServo.value=0.5
        myServo1.value=-0.5
        myServo2.value=0
        count+=1
        sleep(tempo_int)
        myServo.value=0
        myServo1.value=0
        myServo2.value=0
        sleep(tempo_int)

    return True

def fourFour(num_clicks,tempo_int,myServo,myServo1,myServo2):
    count=0

    while count!=num_clicks:
        #4/4 pattern
        sleep(tempo_int)
        myServo.value=0
        myServo1.value=0
        myServo2.value=0
        sleep(tempo_int)
        myServo.value=0.5
        myServo1.value=-0.5
        sleep(tempo_int)
        myServo.value=-0.025
        myServo1.value=0.025
        myServo2.value=0.5
        sleep(tempo_int)
        myServo.value=0.5
        myServo1.value=-0.5
        myServo2.value=0
        sleep(tempo_int)
        myServo.value=0
        myServo1.value=0
        myServo2.value=0
        sleep(tempo_int)

    return True

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
myServo=Servo(27,min_pulse_width=minPW,max_pulse_width=maxPW)
# motor connected to right of robot moves arm forward
myServo1=Servo(22,min_pulse_width=minPW,max_pulse_width=maxPW)
# motor connected to base of robot moves arm left and right
myServo2=Servo(17,min_pulse_width=minPW,max_pulse_width=maxPW)

time_sig=input("Pick a time signature of 2/4, 3/4, or 4/4 (enter as 3/4 for example): ")

tempo=input("Enter tempo in BPM: ")

click_interval=60/int(tempo)

beats=int(input("Pick how many beats you want (enter 18 if you wants 18 beats total for example): "))

if time_sig=="2/4":
    twoFour(beats,click_interval,myServo,myServo1,myServo2)
elif time_sig=="3/4":
    threeFour(beats,click_interval,myServo,myServo1,myServo2)
elif time_sig=="4/4":
    fourFour(beats,click_interval,myServo,myServo1,myServo2)