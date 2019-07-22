#rpi serial communication
#Python app to run a COZIR Sensor
#Uses UART to communicate
from machine import UART
import time
from machine import Timer

class Co2Sensor:
    SPI_MODE = 1
    UART_MODE = 2
    communicationMode = 2
    recentRawData = -1
    recentFilterData = -1
    errorCount = 0
    chrono = Timer.Chrono()
    errorTimeoutTime = .5


    def __init__(self, communicationMode = 2):
        Co2Sensor.chrono.start()
        if communicationMode == Co2Sensor.SPI_MODE:
            Co2Sensor.communicationMode = Co2Sensor.SPI_MODE
            print("SPI MODE NOT IMPLEMENTED")
            raise Exception("SPI Communication Mode not implemented.\nUse Communication Mode 2(UART) instead")

        elif communicationMode == Co2Sensor.UART_MODE:
            Co2Sensor.communicationMode = Co2Sensor.UART_MODE
            Co2Sensor.uart = UART(1, 9600, pins = ('P21','P22'))                         # init with given baudrate
            Co2Sensor.uart.init(9600, bits=8, parity=None, stop=1, pins = ('P21','P22')) # init with given parameters
            Co2Sensor.uart.write('K 1\r\n')
            print("LoPy to Cozir via UART\n")
            Co2Sensor.update2()
            time.sleep(.3)
            Co2Sensor.update2()


    '''
    @staticmethod
    def update():
        if Co2Sensor.communicationMode == Co2Sensor.UART_MODE:
            #Co2Sensor.uart.write('z\r\n')
            Co2Sensor.dataArr = Co2Sensor.uart.readline()
            if Co2Sensor.dataArr is not None:
                Co2Sensor.recentData = int(Co2Sensor.dataArr[3:].decode('UTF-8').rstrip())
            return Co2Sensor.recentData
        else:
            raise Exception("SPI Communication Mode update not implemented.\nUse Communication Mode 2(UART) instead")
    '''
    @staticmethod
    def update2():
        if Co2Sensor.communicationMode == Co2Sensor.UART_MODE:
            Co2Sensor.dataArr = Co2Sensor.uart.readall()
            if Co2Sensor.dataArr is not None:
                Co2Sensor.dataArr = Co2Sensor.dataArr.decode('UTF-8')
                Co2Sensor.dataArr = Co2Sensor.dataArr[len(Co2Sensor.dataArr)-17:].rstrip()
                if Co2Sensor.dataArr.find('Z') == 0:
                    Co2Sensor.recentFilterData = int(Co2Sensor.dataArr[2:7])
                    firstGood = True
                else:
                    firstGood = False
                if Co2Sensor.dataArr.find('z') == 8:
                    Co2Sensor.recentRawData = int(Co2Sensor.dataArr[10:])
                    if firstGood:
                        Co2Sensor.chrono.reset()
                        Co2Sensor.chrono.start()

                return Co2Sensor.recentRawData
            else:
                return -1
        else:
            raise Exception("SPI Communication Mode update not implemented.\nUse Communication Mode 2(UART) instead")



    @staticmethod
    def returnRaw():
        if Co2Sensor.communicationMode == Co2Sensor.UART_MODE:
            Co2Sensor.uart.write('z\r\n')
            Co2Sensor.dataArr = Co2Sensor.uart.readline()
            if Co2Sensor.dataArr is not None:
               Co2Sensor.recentData = int(Co2Sensor.dataArr[3:].decode('UTF-8').rstrip())
               return Co2Sensor.recentData
            else:
                return -1
        else:
            raise Exception("SPI Communication Mode update not implemented.\nUse Communication Mode 2(UART) instead")

    @staticmethod
    def test():
        while True:
            Co2Sensor.update2()
            print(Co2Sensor.recentRawData)
            print(Co2Sensor.recentFilterData)
            time.sleep(.25)
