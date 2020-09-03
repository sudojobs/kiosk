import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(23,GPIO.IN) #GPGPIO 14 -> IR sensor as input
GPIO.setup(24,GPIO.IN) #GPGPIO 14 -> IR sensor as input

while 1:
    if(GPIO.input(24)==False):
      print("Point 1 is Object detected")
    else:
      print("Point 1 is Object not detected")
         
    if(GPIO.input(23)==False): 
      print("Point 2 is Object detected")
    else:
      print("Point 2 is Object not detected")
