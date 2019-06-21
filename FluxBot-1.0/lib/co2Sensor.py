#rpi serial communication
#Python app to run a COZIR Sensor
#Uses UART to communicate
from machine import UART
import time

class Co2Sensor:
    SPI_MODE = 1
    UART_MODE = 2
    communicationMode = 2
    minimumUpdateTime = 0.5
    readyToBeRead = False


    def __init__(self, communicationMode = 2):
        if communicationMode == Co2Sensor.SPI_MODE:
            Co2Sensor.communicationMode = Co2Sensor.SPI_MODE
            print("SPI MODE NOT IMPLEMENTED")
            raise Exception("SPI Communication Mode not implemented.\nUse Communication Mode 2(UART) instead")

        elif communicationMode == Co2Sensor.UART_MODE:
            Co2Sensor.communicationMode = Co2Sensor.UART_MODE
            Co2Sensor.uart = UART(1, 9600, pins = ('P21','P22'))                         # init with given baudrate
            Co2Sensor.uart.init(9600, bits=8, parity=None, stop=1, pins = ('P21','P22')) # init with given parameters
            Co2Sensor.dataArr = b''
            Co2Sensor.lastWriteTime = time.time() - Co2Sensor.minimumUpdateTime
            print("AN-137: LoPy to Cozir via UART\n")
            time.sleep(.3)
    
    @staticmethod
    def update():
        if Co2Sensor.communicationMode == Co2Sensor.UART_MODE:
            Co2Sensor.uart.write('z\r\n')
            Co2Sensor.dataArr = Co2Sensor.uart.readline()
            if Co2Sensor.dataArr is not None:
                return Co2Sensor.dataArr[3:].decode('UTF-8').rstrip()
            else:
                return -1
        else:
            raise Exception("SPI Communication Mode update not implemented.\nUse Communication Mode 2(UART) instead")
      

    
  
