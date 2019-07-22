import pycom
from machine import Timer


class IndicatorLight:
    'Used to change the color of the lopy light'

    heartbeat = True
    BLUE =   0x0000ff
    RED =    0xff0000
    GREEN =  0x00ff00
    PURPLE = 0xff00ff
    YELLOW = 0xffff00
    ORANGE = 0xFF4500
    CYAN = 0x42f4ee
    WHITE = 0xFFFFFF


    def __init__(self, color, delay, duration):
        pycom.heartbeat(False)
        self.rgb = color
        self.delay = delay #in s
        self.pulseDuration =duration
        self.chrono = Timer.Chrono()
        self.chrono.start()
        self.lastPulse = self.chrono.read()
        self.isOn = False


    def setLightColor(self,color):
        self.rgb = color

    #Set delay to 0 to have a solid light
    def setDelay(self, seconds):
        self.delay = seconds


    def setPulseDuration(self,seconds):
        self.pulseDuration = seconds

    def stop(self):
        self.pulseDuration = 0


    def pulse(self):

        if not self.isOn and self.lastPulse + self.delay <= self.chrono.read():
            pycom.rgbled(self.rgb)
            self.isOn = True
        if self.isOn and self.lastPulse + self.delay +  self.pulseDuration <= self.chrono.read():
            self.lastPulse = self.chrono.read()
            self.isOn = False
            pycom.rgbled(0x0)

    @staticmethod
    def beating(beating):
        pycom.heartbeat(beating)
