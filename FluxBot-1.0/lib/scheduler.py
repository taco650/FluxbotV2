from indicatorLight import IndicatorLight 
from bme280 import *
from machine import I2C
from actuator import Actuator
from Co2Sensor import Co2Sensor
from dataWriter2 import DataWriter
from machine import WDT
import constants as CONSTANTS
import time



class Scheduler:
    running = True


    def __init__(self):
        Scheduler.wdt = WDT(timeout=CONSTANTS.WATCHDOG_TIMEOUT)
        Actuator()
        Co2Sensor()
        Actuator.setPosition(CONSTANTS.ACTUATION_EXTENSION_POSITION)
        Co2Sensor.update()
        DataWriter(CONSTANTS.DEVICE_NAME)
        Scheduler.running = True
        Scheduler.duringCycle = False
        Scheduler.loopStartTime = time.time()
        Scheduler.dataWriteLight = IndicatorLight(IndicatorLight.YELLOW, .3, .2)
        Scheduler.closedBoxStateLight = IndicatorLight(IndicatorLight.PURPLE, 5, 1)
        Scheduler.openBoxStateLight = IndicatorLight(IndicatorLight.GREEN, 5, 1)
        Co2Sensor.update()
        i2cNotCreated = True
        while i2cNotCreated:
            i2cNotCreated = Scheduler.createI2C()
            

    @staticmethod
    def createI2C():
        try:
            Scheduler.i2c = I2C(0, I2C.MASTER, baudrate=400000)
            Scheduler.bme = BME280(i2c=Scheduler.i2c, mode=BME280_OSAMPLE_16, address = 119)
            return False
        except Exception as ex:
            print(ex)
            print("Creating i2c object failed")
            return True
    
    #Once ran, continuously runs until running is False(upon error) 
    @staticmethod  
    def run():
        Scheduler.duringCycle = False
        Scheduler.currTime = time.time()
        Scheduler.nextDataRecordTime = time.time()
        Scheduler.nextCycleStartTime = time.time()
        actuatorNotSet = True
        while Scheduler.running:
            Scheduler.update()
            if (Scheduler.nextCycleStartTime <= time.time()):
                if actuatorNotSet:
                    Actuator.setPosition(CONSTANTS.ACTUATION_RETRACTION_POSITION)
                    actuatorNotSet = False
                Scheduler.duringCycle = True
                Scheduler.closedBoxStateLight.pulse()
                if Scheduler.nextDataRecordTime <= time.time():
                    Scheduler.dataWriteLight.pulse()
                    Scheduler.nextDataRecordTime = time.time() + (1/CONSTANTS.MEASUREMENT_CLOSED_BOX_FRQ)
                    DataWriter.write(Co2Sensor.update(),Scheduler.bme.temperature,Scheduler.bme.pressure,Scheduler.bme.humidity,Actuator.actuatorPosition())

                    
                if Scheduler.nextCycleStartTime + CONSTANTS.CYCLE_LENGTH <= time.time():
                    Scheduler.nextCycleStartTime = time.time() + CONSTANTS.CYCLE_PERIOD
            
            elif Scheduler.duringCycle == True:
                Scheduler.duringCycle = False
                actuatorNotSet = True
                Scheduler.nextDataRecordTime = time.time()

            else:#If not during the cycle
                if actuatorNotSet:
                    Actuator.setPosition(CONSTANTS.ACTUATION_EXTENSION_POSITION)
                    actuatorNotSet = False
                Scheduler.openBoxStateLight.pulse()
                if Scheduler.nextDataRecordTime <= time.time():
                    Scheduler.nextDataRecordTime = time.time() + (1/CONSTANTS.MEASUREMENT_OPEN_BOX_FRQ)
                    DataWriter.write(Co2Sensor.update(),Scheduler.bme.temperature,Scheduler.bme.pressure,Scheduler.bme.humidity,Actuator.actuatorPosition()) 





    #Houskeeping functions
    @staticmethod
    def update():
        print("Running")
        Scheduler.wdt.feed()