from indicatorLight import IndicatorLight 
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
        Scheduler.light = IndicatorLight(0xFFFF00, 2, 1)
        Co2Sensor.update()
    
    #Once ran, continuously runs until running is False 
    @staticmethod  
    def run():
        while Scheduler.running:
            Scheduler.currTime = time.time()
            if Scheduler.currTime + CONSTANTS.CYCLE_PERIOD >= time.time():
                Scheduler.duringCycle = True


    #Houskeeping functions
    @staticmethod
    def update():
        Scheduler.wdt.feed()
        Scheduler.light.pulse()