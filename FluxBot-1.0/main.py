# main.py -- put your code here!
'''
from machine import I2C, PWM, Pin, WDT
from bme280 import BME280, BME280_OSAMPLE_16
from actuator import Actuator
from Co2Sensor import Co2Sensor
from dataWriter2 import DataWriter
import constants as CONSTANTS
from indicatorLight import IndicatorLight
from scheduler import Scheduler
import pycom
import time

#Scheduler()
#Scheduler.run()


while True:
    ppm = Co2Sensor.update()
    DataWriter.write(ppm,bme.temperature,bme.pressure,bme.humidity,Actuator.actuatorPosition())
    print("loop")
    print("Temperature: " + bme.temperature)
    print("Humidity: " + bme.humidity)
    print("Pressure: " + bme.pressure)
    print("C02: " + str(ppm))
    time.sleep(1)

'''
