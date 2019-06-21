# main.py -- put your code here!
from machine import I2C, PWM, Pin, WDT

from bme280 import BME280, BME280_OSAMPLE_16
from actuator import Actuator
from scheduler import Scheduler
from Co2Sensor import Co2Sensor
from dataWriter2 import DataWriter
import pycom
import time

i2c = I2C(0, I2C.MASTER, baudrate=400000)
bme = BME280(i2c=i2c, mode=BME280_OSAMPLE_16, address = i2c.scan()[0])


'''while True:
    print("Temp: " + bme.temperature + ", Pressure: " + bme.pressure +", Humidity: " + bme.humidity)
    time.sleep(2)
'''
#Scheduler()
#Scheduler.run()
#Actuator()
Co2Sensor()
DataWriter('Test')
pycom.heartbeat(False)
#wdt = WDT(timeout=7000)
while True:
    ppm = Co2Sensor.update()
    DataWriter.write(ppm,bme.temperature,bme.pressure,bme.humidity,Actuator.actuatorPosition())
    print("loop")
    print("Temperature: " + bme.temperature)
    print("Humidity: " + bme.humidity)
    print("Pressure: " + bme.pressure)
    print("C02: " + str(ppm))
    #wdt.feed()
    #Actuator.setPosition(0)
    #pycom.rgbled(0xFF00)
    #time.sleep(5)
    #wdt.feed()
    #Actuator.setPosition(0.5)
    #pycom.rgbled(0xFF00FF)
    #time.sleep(5)
    #cwdt.feed()
    #pycom.rgbled(0x00FFFF)
    #Actuator.setPosition(1)
    #print(Co2Sensor.update())
    time.sleep(1)
  
