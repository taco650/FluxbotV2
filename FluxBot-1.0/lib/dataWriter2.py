from machine import SD
from machine import RTC
import os
import utime


class DataWriter:
    'Used to write sensor data to the SD card in a csv(Excel) format.'

    deviceID = "Default"
    pathPrefix ='/sd/'



    def __init__(self, deviceID):
        DataWriter.sd = SD()
        DataWriter.rtc =RTC()
        os.mount(DataWriter.sd, '/sd')
        DataWriter.deviceID = deviceID
        now = DataWriter.rtc.now()
        DataWriter.year = now[0]
        DataWriter.month = now[1]
        DataWriter.day = now[2]
        DataWriter.dataFile = str(DataWriter.deviceID) + '_Fluxbot_Data_' + str(DataWriter.month) +'.'+ str(DataWriter.day) +"."+ str(DataWriter.year) + '.csv'
        DataWriter.logFile = str(DataWriter.deviceID)+ '_bootLog.csv'


    @staticmethod
    def writeData(rawCo2, filterCo2, temp, pressure, humidity, actuatorState, log):
        #use 'w' instead of 'a' to create a new file and overwrite the existing
        secondsSinceEpoch = utime.time()
        if not DataWriter.isFileCreated(DataWriter.dataFile):
            args = ["Sec since 2000", "Raw CO2 PPM", "Filter CO2 PPM", "Temp", "Pressure", "Humidity", "ActuatorState", "ERR"]
            DataWriter.writeRow(DataWriter.dataFile, args, -1)

        args = [secondsSinceEpoch, rawCo2, filterCo2, temp, pressure, humidity, actuatorState, log]
        DataWriter.writeRow(DataWriter.dataFile, args, 1)

    @staticmethod
    def writeRow(fileName, args = [], mode = 1):
        openMode = 'a'
        if mode == -1:
            openMode = 'x'#new file
        elif mode == 1:
            openMode = 'a'#append

        with open(str(DataWriter.pathPrefix) + str(fileName), openMode) as csvfile:
                row = ''
                for x in args:
                    if row != '':
                        row = row +', '+ str(x)
                    else:
                        row = str(x)
                csvfile.write(str(row)+'\n')
                csvfile.close()


    @staticmethod
    def isFileCreated(fileName):
        try:
            f = open(str(DataWriter.pathPrefix) + str(fileName),'r')
            return True
        except:
            return False

    @staticmethod
    def logBoot(fileName):
        intRtc = RTC()
        if DataWriter.isFileCreated(fileName):
            openMode = 'a'
        else:
            openMode = 'x'

        with open(str(DataWriter.pathPrefix) + str(fileName), openMode) as csvfile:
                row = ''
                args =intRtc.now()
                for x in args:
                    if row != '':
                        row = row +', '+ str(x)
                    else:
                        row = str(x)
                csvfile.write(str(row)+'\n')
                csvfile.close()


    '''
    def test(self):
        self.write(2,3,4,5,6)
    '''
