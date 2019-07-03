from indicatorLight import IndicatorLight 
from bme280 import *
from machine import I2C,RTC
from pcf8523 import PCF8523
from actuator import Actuator
from Co2Sensor import Co2Sensor
from dataWriter2 import DataWriter
from machine import WDT
import constants as CONSTANTS
import time
import utime



class Scheduler:
    running = True


    def __init__(self):
        Scheduler.wdt = WDT(timeout=CONSTANTS.WATCHDOG_TIMEOUT)
        Scheduler.dataWriteLight = IndicatorLight(IndicatorLight.PURPLE, .3, .2)
        Scheduler.mountSDCardLight = IndicatorLight(IndicatorLight.PURPLE, .3, .2)
        Scheduler.co2Light = IndicatorLight(IndicatorLight.RED, .3, .2)
        Scheduler.bmeLight = IndicatorLight(IndicatorLight.YELLOW, .3, .2)
        Scheduler.goodState = IndicatorLight(IndicatorLight.GREEN, 0.3, 0.2)
        Scheduler.closedBoxStateLight = IndicatorLight(IndicatorLight.GREEN, 5, .2)
        Scheduler.openBoxStateLight = IndicatorLight(IndicatorLight.CYAN, 5, .2)
        Actuator()
        Co2Sensor()
        Actuator.setPosition(CONSTANTS.ACTUATION_EXTENSION_POSITION)
        Scheduler.running = True
        Scheduler.duringCycle = False
        Scheduler.loopStartTime = time.time()
        


        deviceNotConnected = True
        #testing if bme can be connected to
        while deviceNotConnected:
            Scheduler.bmeLight.pulse()
            deviceNotConnected = Scheduler.createI2C()

        deviceNotConnected = True
        Scheduler.intRtc = RTC()
        now = Scheduler.extRtc.now()
        Scheduler.intRtc.init((now[0], now[1], now[2], now[3], now[4], now[5], 0))
        print(Scheduler.intRtc.now())
        time.sleep(CONSTANTS.WATCHDOG_TIMEOUT/2/1000)

        #testing if sd card can be mounted
        while deviceNotConnected:
            Scheduler.mountSDCardLight.pulse()
            deviceNotConnected = Scheduler.mountSD()

        deviceNotConnected = True

        #testing if co2 sensor is connected
        while deviceNotConnected:
            Scheduler.co2Light.pulse()
            Co2Sensor.update2()
            deviceNotConnected = Scheduler.co2Disconnected()
        
        goodLightTime = utime.ticks_ms()
        while (goodLightTime + CONSTANTS.ACTUATION_TIME*1000 >= utime.ticks_ms()):
            Scheduler.update()
            Actuator.setPosition(1)
            Scheduler.goodState.pulse()
            print("Actuator Open")

        goodLightTime = utime.ticks_ms()
        while (goodLightTime + CONSTANTS.ACTUATION_TIME*1000 >= utime.ticks_ms()):
            Scheduler.update()
            Actuator.setPosition(0)
            Scheduler.goodState.pulse()
            print("Actuator Closed")

        goodLightTime = utime.ticks_ms()
        while (goodLightTime + CONSTANTS.ACTUATION_TIME*1000 >= utime.ticks_ms()):
            Scheduler.update()
            Actuator.setPosition(1)
            Scheduler.goodState.pulse()
            print("Actuator Open")
        
        
            

    @staticmethod
    def mountSD():
        try:
            DataWriter(CONSTANTS.DEVICE_NAME)
            return False
        except Exception as ex:
            print(ex)
            print("Mounting SD Card failed")
            return True
    
    @staticmethod
    def createI2C():
        try:
            Scheduler.i2c = I2C(0, I2C.MASTER, baudrate=400000)
            Scheduler.bme = BME280(i2c=Scheduler.i2c, mode=BME280_OSAMPLE_16, address = 119)
            Scheduler.extRtc = PCF8523(Scheduler.i2c)
            if Scheduler.extRtc.now()[0]<2019:
                print("RTC ERROR")
                return True
            return False
        except Exception as ex:
            print(ex)
            print("BME or RTC error. Check connections.")
            return True
    
    '''
    #Once ran, continuously runs until running is False(upon error) 
    @staticmethod  
    def runContinuous():
        Scheduler.update()
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
                    if Scheduler.co2Disconnected():
                        log = "ERR"
                    else:
                        log = "NOR"
                    Scheduler.dataWriteLight.pulse()
                    Scheduler.nextDataRecordTime = time.time() + (1/CONSTANTS.MEASUREMENT_CLOSED_BOX_FRQ)
                    DataWriter.write(Co2Sensor.update(),Scheduler.bme.temperature,Scheduler.bme.pressure,Scheduler.bme.humidity,Actuator.actuatorPosition(), log)

                    
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
                    if Scheduler.co2Disconnected():
                        log = "ERR"
                    else:
                        log = "NOR"
                    Scheduler.nextDataRecordTime = time.time() + (1/CONSTANTS.MEASUREMENT_OPEN_BOX_FRQ)
                    DataWriter.write(Co2Sensor.update(),Scheduler.bme.temperature,Scheduler.bme.pressure,Scheduler.bme.humidity,Actuator.actuatorPosition(), log) 
    '''
    @staticmethod
    def runBurst():
        Scheduler.update()
        Scheduler.currTime = time.time()
        Scheduler.nextBurstTime = time.time()
        Scheduler.nextCycleStartTime = time.time()+CONSTANTS.CYCLE_PERIOD
        while Scheduler.running:
            Scheduler.update()  
            Co2Sensor.update2() 
            if Scheduler.nextCycleStartTime <= time.time():
                Scheduler.closedBoxStateLight.pulse()
                Scheduler.dataBurst(CONSTANTS.OPEN_BURST_POINTS, CONSTANTS.OPEN_BURST_DELAY)
                Actuator.setPosition(CONSTANTS.ACTUATION_RETRACTION_POSITION)
                Scheduler.dataBurst(CONSTANTS.CLOSED_BURST_POINTS, CONSTANTS.CLOSED_BURST_DELAY)
                Actuator.setPosition(CONSTANTS.ACTUATION_EXTENSION_POSITION)
                Scheduler.nextCycleStartTime += CONSTANTS.CYCLE_PERIOD
                Scheduler.nextBurstTime = time.time() + CONSTANTS.ACTUATION_TIME + CONSTANTS.BURST_DELAY_AFTER_OPEN
            elif Scheduler.nextBurstTime <= time.time():
                Scheduler.dataBurst(CONSTANTS.OPEN_BURST_POINTS, CONSTANTS.OPEN_BURST_DELAY)
                Scheduler.nextBurstTime += CONSTANTS.BURST_PERIOD
            else:
                Scheduler.openBoxStateLight.pulse()






    #Houskeeping functions
    @staticmethod
    def update():
        print(Scheduler.intRtc.now())
        Scheduler.wdt.feed()

    @staticmethod
    def co2Disconnected():
        if Co2Sensor.lastGoodRead + Co2Sensor.errorTimeoutTime <= utime.ticks_ms():
            return True
        else:
            return False

    @staticmethod
    def dataBurst(numOfPoints, delayBetweenPoints):
        pointsCompleted = 0
        nextPointTime = utime.ticks_ms()
        while pointsCompleted < numOfPoints:
            Scheduler.update()
            Co2Sensor.update2()
            Scheduler.dataWriteLight.pulse()
            if nextPointTime <= utime.ticks_ms():
                if Scheduler.co2Disconnected():
                    log = "1"
                    print("Co2 Read Error")
                else:
                    log = "0"
                pointsCompleted += 1
                nextPointTime = nextPointTime + delayBetweenPoints
                DataWriter.write(Co2Sensor.recentRawData,Co2Sensor.recentFilterData,Scheduler.bme.temperature,Scheduler.bme.pressure,Scheduler.bme.humidity,Actuator.actuatorPosition(), log)


