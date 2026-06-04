#!/usr/bin/python3
# GPIO26を出力としてLEDに給電（+3.3V）する

import RPi.GPIO as GPIO
from time import sleep


PORT = 26

GPIO.setmode(GPIO.BCM)
GPIO.setup(PORT, GPIO.OUT, initial=GPIO.LOW)

try:
    while True:
        GPIO.output(PORT, GPIO.HIGH)
        sleep(1.0)
        GPIO.output(PORT, GPIO.LOW)
        sleep(1.0)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
