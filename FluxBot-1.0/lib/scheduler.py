from indicatorLight import IndicatorLight
from bme280 import *
from machine import I2C,RTC
from pcf8523 import PCF8523
from actuator import Actuator
from Co2Sensor import Co2Sensor
from dataWriter2 import DataWriter
from machine import WDT
from machine import SD
from machine import Pin
import gc
import os
import constants as CONSTANTS
import time
from machine import Timer
import gc



class Scheduler:
    running = True
    chrono = Timer.Chrono()
    state = -1

    def __init__(self):

        Scheduler.wdt = WDT(timeout=CONSTANTS.WATCHDOG_TIMEOUT)
        Scheduler.dataWriteLight = IndicatorLight([IndicatorLight.PURPLE], .3, .2)
        Scheduler.mountSDCardLight = IndicatorLight([IndicatorLight.PURPLE], .5, .2)
        Scheduler.co2Light = IndicatorLight([IndicatorLight.RED], .3, .2)
        Scheduler.bmeLight = IndicatorLight([IndicatorLight.YELLOW], .3, .2)
        Scheduler.goodState = IndicatorLight([IndicatorLight.GREEN], 0.3, 0.2)
        Scheduler.closedBoxStateLight = IndicatorLight([IndicatorLight.GREEN], 5, .2)
        Scheduler.openBoxStateLight = IndicatorLight([IndicatorLight.CYAN], 5, .2)
        Scheduler.waitingForDetonationLight = IndicatorLight([IndicatorLight.WHITE], 5, .2)

        Scheduler.unmountGreenLight = IndicatorLight([IndicatorLight.PURPLE, IndicatorLight.GREEN, IndicatorLight.PURPLE],2,.2)
        Scheduler.unmountYellowLight = IndicatorLight([IndicatorLight.PURPLE, IndicatorLight.YELLOW, IndicatorLight.PURPLE],1,.2)
        Scheduler.unmountRedLight = IndicatorLight([IndicatorLight.PURPLE, IndicatorLight.RED, IndicatorLight.PURPLE],.3,.2)

        Scheduler.flushLight = IndicatorLight([IndicatorLight.PURPLE], 0, 3)
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


        print("Checking for SD card")
        #testing if sd card can be mounted
        while deviceNotConnected:
            Scheduler.mountSDCardLight.pulse()
            deviceNotConnected = Scheduler.mountSD()

        deviceNotConnected = True
        DataWriter.writeHeaders()


        #testing if co2 sensor is connected
        while deviceNotConnected:
            Scheduler.co2Light.pulse()
            print("Co2 Connection Error")
            Co2Sensor.update2()
            deviceNotConnected = Scheduler.co2Disconnected()


        '''
        Scheduler.chrono.start()
        while (CONSTANTS.ACTUATION_TIME >= Scheduler.chrono.read()):
            Scheduler.update()
            Actuator.setPosition(CONSTANTS.ACTUATION_EXTENSION_POSITION)
            Scheduler.goodState.pulse()
            print("Actuator Open")

        Scheduler.chrono.reset()
        Scheduler.chrono.start()
        while (CONSTANTS.ACTUATION_TIME >= Scheduler.chrono.read()):
            Scheduler.update()
            Actuator.setPosition(CONSTANTS.ACTUATION_RETRACTION_POSITION)
            Scheduler.goodState.pulse()
            print("Actuator Closed")

        Scheduler.chrono.reset()
        Scheduler.chrono.start()
        while (CONSTANTS.ACTUATION_TIME >= Scheduler.chrono.read()):
            Scheduler.update()
            Actuator.setPosition(CONSTANTS.ACTUATION_EXTENSION_POSITION)
            Scheduler.goodState.pulse()
            print("Actuator Open")
        Scheduler.chrono.stop()
        '''


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
        DataWriter.logBoot(DataWriter.logFile)
        Scheduler.update()
        Scheduler.currTime = time.time()
        Scheduler.nextBurstTime = time.time()
        #Scheduler.nextCycleStartTime = time.time() + CONSTANTS.CYCLE_PERIOD - (CONSTANTS.OPEN_BURST_POINTS * CONSTANTS.OPEN_BURST_DELAY/1000)
        Scheduler.nextCycleStartTime = time.time() + 1 + CONSTANTS.CYCLE_PERIOD - int((CONSTANTS.OPEN_BURST_POINTS * CONSTANTS.OPEN_BURST_DELAY)/1000)

        while Scheduler.running:
            Scheduler.update()

            Co2Sensor.update2()
            if Scheduler.nextCycleStartTime <= time.time():
                print("Mounting")

                if not DataWriter.isMounted:
                    DataWriter.sd = SD()
                    os.mount(DataWriter.sd, '/sd')
                    DataWriter.isMounted = True
                    Scheduler.state = -1


                Scheduler.closedBoxStateLight.pulse()
                Scheduler.dataBurst(CONSTANTS.OPEN_BURST_POINTS, CONSTANTS.OPEN_BURST_DELAY)
                Actuator.setPosition(CONSTANTS.ACTUATION_RETRACTION_POSITION)
                Scheduler.dataBurst(CONSTANTS.CLOSED_BURST_POINTS, CONSTANTS.CLOSED_BURST_DELAY)
                Actuator.setPosition(CONSTANTS.ACTUATION_EXTENSION_POSITION)
                #Scheduler.nextCycleStartTime = time.time() + CONSTANTS.CYCLE_PERIOD - (CONSTANTS.OPEN_BURST_POINTS * CONSTANTS.OPEN_BURST_DELAY/1000.0)
                Scheduler.nextCycleStartTime += 3600

                Scheduler.nextBurstTime = time.time() + 1
            elif Scheduler.nextBurstTime <= time.time():
                Scheduler.state += 1
                Scheduler.nextBurstTime += CONSTANTS.BURST_PERIOD
                Scheduler.dataBurst(CONSTANTS.OPEN_BURST_POINTS, CONSTANTS.OPEN_BURST_DELAY)
                if Scheduler.state == 0:
                    if DataWriter.isMounted:
                        DataWriter.isMounted = False
                        print("Unmounting")
                        os.unmount('/sd')

                elif Scheduler.state == 3:
                    print("Mounting soon")

            else:
                gc.collect()
                if Scheduler.state == 0 or Scheduler.state == 1:
                    Scheduler.unmountGreenLight.pulse()

                elif Scheduler.state == 2:
                    Scheduler.unmountYellowLight.pulse()

                else:
                    Scheduler.unmountRedLight.pulse()







    @staticmethod
    def runBurstTest():
        DataWriter.logBoot(DataWriter.logFile)
        Scheduler.update()
        Scheduler.currTime = time.time()
        Scheduler.nextBurstTime = time.time()
        #Scheduler.nextCycleStartTime = time.time() + CONSTANTS.CYCLE_PERIOD - (CONSTANTS.OPEN_BURST_POINTS * CONSTANTS.OPEN_BURST_DELAY/1000)
        Scheduler.nextCycleStartTime = time.time() + 6 - int((CONSTANTS.OPEN_BURST_POINTS * CONSTANTS.OPEN_BURST_DELAY)/1000)

        while Scheduler.running:
            Scheduler.update()

            Co2Sensor.update2()
            if Scheduler.nextCycleStartTime <= time.time():
                Scheduler.closedBoxStateLight.pulse()
                Scheduler.dataBurst(CONSTANTS.OPEN_BURST_POINTS, CONSTANTS.OPEN_BURST_DELAY)
                Actuator.setPosition(CONSTANTS.ACTUATION_RETRACTION_POSITION)
                Scheduler.dataBurst(CONSTANTS.CLOSED_BURST_POINTS, CONSTANTS.CLOSED_BURST_DELAY)
                Actuator.setPosition(CONSTANTS.ACTUATION_EXTENSION_POSITION)
                #Scheduler.nextCycleStartTime = time.time() + CONSTANTS.CYCLE_PERIOD - (CONSTANTS.OPEN_BURST_POINTS * CONSTANTS.OPEN_BURST_DELAY/1000.0)
                Scheduler.running = False
            elif Scheduler.nextBurstTime <= time.time():
                Scheduler.nextBurstTime += CONSTANTS.BURST_PERIOD
                Scheduler.dataBurst(CONSTANTS.OPEN_BURST_POINTS, CONSTANTS.OPEN_BURST_DELAY)
            else:
                Scheduler.openBoxStateLight.pulse()

        while True:
            Scheduler.update()



    #Houskeeping functions
    @staticmethod
    def update():
        print("External Time " + str(Scheduler.extRtc.now()))
        print("Internal Time " + str(Scheduler.intRtc.now()))
        print("Cycle state " + str(Scheduler.state))
        print("Is Mounted " + str(DataWriter.isMounted))
        print("Memory allocated " + str(gc.mem_alloc()))
        Scheduler.wdt.feed()


    @staticmethod
    def co2Disconnected():
        if Co2Sensor.chrono.read() >= Co2Sensor.errorTimeoutTime:
            return True
        else:
            return False

    @staticmethod
    def waitForDetonation():
        while True:
            Scheduler.update()
            Scheduler.waitingForDetonationLight.pulse()
            #instant start
            if CONSTANTS.DETONATION_HOUR == -1:
                return
            #check for bootLog File
            #If present, wait until "on the hour"
            if DataWriter.isFileCreated(str(CONSTANTS.DEVICE_NAME) + '_bootLog.csv'):
                while True:
                    Scheduler.update()
                    Scheduler.waitingForDetonationLight.pulse()
                    if Scheduler.intRtc.now()[4] == 0:
                        return

            if Scheduler.intRtc.now()[3] == CONSTANTS.DETONATION_HOUR:
                return




    @staticmethod
    def dataBurst(numOfPoints, delayBetweenPoints):
        chrono = Timer.Chrono()
        pointsCompleted = 0
        nextPointTime = 0
        chrono.start()
        print("Start data burst")
        while pointsCompleted < numOfPoints:
            print("Data burst")
            Scheduler.update()
            Co2Sensor.update2()
            Scheduler.dataWriteLight.pulse()
            if nextPointTime <= chrono.read_ms():
                if Scheduler.co2Disconnected():
                    log = "1"
                    print("Co2 Read Error")
                else:
                    log = "0"
                pointsCompleted += 1
                nextPointTime += delayBetweenPoints
                DataWriter.writeData(Co2Sensor.recentRawData,Co2Sensor.recentFilterData,Scheduler.bme.temperature,Scheduler.bme.pressure,Scheduler.bme.humidity,Actuator.actuatorPosition(), log)
                Scheduler.flushBuffer()
        print("End data burst")

    @staticmethod
    def flushBuffer():
        '''
        #while len(DataWriter.dataBuffer) > 0 and SD card is mounted, pop from buffer and write to SD card
        try:
            DataWriter.sd = SD()
            DataWriter.sdPresent = True
        except Exception as ex1:
            DataWriter.sdPresent = False
            print(ex1)
            Scheduler.mountSDCardLight.pulse()
            Scheduler.co2Light.pulse()
        '''
        '''
        if not DataWriter.sdPresent and DataWriter.isMounted:
            DataWriter.isMounted = False
            os.unmount('/sd')

        elif DataWriter.sdPresent and not DataWriter.isMounted:
            DataWriter.isMounted = True
            os.mount(DataWriter.sd, '/sd')
        '''
        '''
        if DataWriter.sdPresent and len(DataWriter.dataBuffer) > 0:
            if DataWriter.sdPresent and not DataWriter.isMounted:
                DataWriter.isMounted = True
                try:
                    os.mount(DataWriter.sd, '/sd')
                except Exception as ex1:
                    print(ex1)

            while len(DataWriter.dataBuffer) > 0:

                print('In data writer')
                Scheduler.update()
                Scheduler.flushLight.pulse()
                try:
                    DataWriter.writeRow(DataWriter.dataFile, DataWriter.dataBuffer.pop(0), 1)
                except:
                    print("Failed write")
            try:
                os.unmount('/sd')
            except Exception as ex2:
                print(ex2)
            DataWriter.isMounted = False


        Scheduler.dataWriteLight.endPulse()
        '''

        while len(DataWriter.dataBuffer) > 0 and DataWriter.isMounted:
            print('Flushing data')
            Scheduler.update()
            Scheduler.flushLight.pulse()
            DataWriter.writeRow(DataWriter.dataFile, DataWriter.dataBuffer.pop(0), 1)

        Scheduler.flushLight.endPulse()


    @staticmethod
    def testWrite():
        print('Test Write start')
        button = Pin("G17",  mode=Pin.IN,  pull=Pin.PULL_UP)
        DataWriter.isMounted = True
        isToggled = False
        chrono = Timer.Chrono()
        chrono.start()
        nextPointTime = 0
        unMountTime = False
        while True:
            Scheduler.lightTest.pulse()
            print(DataWriter.isMounted)
            print(DataWriter.sdPresent)
            if DataWriter.isMounted:
                Scheduler.flushBuffer()
            Scheduler.update()
            print(button.value())
            if not button.value() and not isToggled:
                isToggled = True
                if DataWriter.isMounted:
                    os.unmount('/sd')
                    DataWriter.isMounted = False
                else:
                    DataWriter.sd = SD()
                    os.mount(DataWriter.sd, '/sd')
                    DataWriter.isMounted = True
            elif button.value() and isToggled:
                isToggled = False

            if nextPointTime <= chrono.read_ms():
                DataWriter.writeData(0,0,0,0,0,0, "Test")
                nextPointTime += 5000
